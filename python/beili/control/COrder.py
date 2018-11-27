# *- coding:utf8 *-
import re
import sys
import os
import uuid
import random
import shutil
import xlrd
import xlwt
from flask import request
# import logging
import threading
from config.response import PARAMS_MISS, SYSTEM_ERROR, PARAMS_ERROR, TOKEN_ERROR, AUTHORITY_ERROR, STOCK_NOT_ENOUGH,\
        NO_ENOUGH_MOUNT, NO_BAIL, NO_ADDRESS, NOT_FOUND_ORDER, PRODUCT_OFFLINE, SKU_WRONG, CANNOT_CANCEL
from config.setting import QRCODEHOSTNAME
from common.token_required import verify_token_decorator, usid_to_token, is_tourist, is_admin
from common.import_status import import_status
from common.timeformat import get_db_time_str
from common.get_model_return_list import get_model_return_list, get_model_return_dict
from service.SUser import SUser
from service.SMessage import SMessage
from service.SOrder import SOrder
from service.SGoods import SGoods
from service.SMyCenter import SMyCenter
from service.DBSession import db_session
from service.SAccount import SAccount
import platform
from configparser import ConfigParser
from common.beili_error import stockerror, dberror
from datetime import datetime
from common.timeformat import format_for_db, get_random_str, get_random_int
from models.model import User, AgentMessage, Performance, Amount, Reward, MoneyRecord, OrderSkuInfo, ShoppingCart\
    , ProductSku, OrderInfo
sys.path.append(os.path.dirname(os.getcwd()))


class COrder():

    def __init__(self):
        self.suser = SUser()
        self.sorder = SOrder()
        self.sgoods = SGoods()
        self.smycenter = SMyCenter()
        self.smessage = SMessage()
        self.saccount = SAccount()
        self.conf = ConfigParser()
        self.conf.read('config/setting.ini')

    @verify_token_decorator
    def create_order(self):
        if is_tourist():
            return TOKEN_ERROR
        data = request.json
        if not data:
            return PARAMS_MISS
        params_list = ["UAid", "product_list", "OInote", "PRlogisticsfee", "totalprice"]
        for param in params_list:
            if param not in data:
                response = {}
                response['message'] = u"参数缺失"
                response['paramname'] = param
                response['status'] = 405
                return response
        try:
            UAid = data['UAid']
            OInote = data['OInote']
            product_list = data['product_list']
            PRlogisticsfee = float(data['PRlogisticsfee'])
            totalprice = float(data['totalprice'])
        except:
            return PARAMS_ERROR
        real_PRlogisticsfee = 0
        if len(product_list) == 1 and len(product_list[0]['skulist']) == 1 and int(product_list[0]['skulist'][0]['number']) == 1:
            real_PRlogisticsfee = get_model_return_dict(self.sgoods.get_product_details(product_list[0]['PRid']))[
                'PRlogisticsfee']
        user_info = get_model_return_dict(self.smycenter.get_user_basicinfo(request.user.id))
        if not user_info:
            return SYSTEM_ERROR
        if user_info['USbail'] < float(self.conf.get('account', 'bail')):
            return NO_BAIL
        mount = 0
        new_list = []
        all_psid = []
        discountnum = 0
        product_num = 0
        try:
            for product in product_list:
                check_product = get_model_return_dict(self.sgoods.get_product_info(product['PRid']))
                if not check_product:
                    return PRODUCT_OFFLINE
                for sku in product['skulist']:
                    sku_info = get_model_return_dict(self.sgoods.get_sku_status(sku['psid']))
                    if not sku_info:
                        return SKU_WRONG
                    if sku['number'] > sku_info['PSstock']:
                        return STOCK_NOT_ENOUGH
                    mount = mount + sku['number'] * check_product['PRprice']
                    product_num = product_num + sku['number']
                    discountnum = discountnum + sku['number'] * check_product['PAdiscountnum']
                    all_psid.append(sku['psid'])
                product['PRprice'] = check_product['PRprice']
                new_list.append(product)
            if totalprice != mount + real_PRlogisticsfee or real_PRlogisticsfee != PRlogisticsfee:
                response = {}
                response['status'] = 200
                response['success'] = False
                response['data'] = new_list
                response['PRlogisticsfee'] = real_PRlogisticsfee
                response['totalprice'] = mount + real_PRlogisticsfee
                return response
            if user_info['USmount'] < mount + PRlogisticsfee:
                return NO_ENOUGH_MOUNT
        except Exception as e:
            print e
            return SYSTEM_ERROR
        session = db_session()
        try:
            OIid = str(uuid.uuid4())
            OIsn = datetime.strftime(datetime.now(), format_for_db) + get_random_int()
            OIcreatetime = datetime.strftime(datetime.now(), format_for_db)
            address = get_model_return_dict(self.smycenter.get_other_address(request.user.id, UAid))
            if not address:
                return NO_ADDRESS
            area = get_model_return_dict(self.smycenter.get_area_by_areaid(address['areaid']))
            from common.timeformat import get_web_time_str
            if area:
                city = get_model_return_dict(self.smycenter.get_city_by_cityid(area['cityid']))
                province = get_model_return_dict(self.smycenter.get_province_by_provinceid(city['provinceid']))
                provincename = province['provincename']
                cityname = city['cityname']
                areaname = area['areaname']
                details = address['UAdetails']
                username = address['UAname']
                userphonenum = address['UAphonenum']
            else:
                city = get_model_return_dict(self.smycenter.get_city_by_cityid(address['cityid']))
                province = get_model_return_dict(self.smycenter.get_province_by_provinceid(city['provinceid']))
                provincename = province['provincename']
                cityname = city['cityname']
                areaname = None
                details = address['UAdetails']
                username = address['UAname']
                userphonenum = address['UAphonenum']


            result = self.sorder.add_order(session, OIid, OIsn, request.user.id, OInote, mount, UAid, OIcreatetime,
                PRlogisticsfee, provincename, cityname, areaname, details, username, userphonenum, product_num, discountnum)
            if not result:
                raise dberror

            # 插入订单商品详情表
            for product in new_list:
                OPIid = str(uuid.uuid4())
                PRid = product['PRid']
                PRname = product['PRname']
                PRimage = get_model_return_dict(self.sgoods.get_product(PRid))['PRpic']
                PRprice = product['PRprice']
                result = self.sorder.add_orderproductinfo(session, OPIid, OIid, PRid, PRname, PRprice, PRimage)
                if not result:
                    raise dberror
                # 插入订单sku详情表
                for sku in product['skulist']:
                    orderskuinfo = OrderSkuInfo()
                    orderskuinfo.OSIid = str(uuid.uuid4())
                    orderskuinfo.OPIid = OPIid
                    orderskuinfo.number = sku['number']
                    orderskuinfo.sizename = sku['sizename']
                    orderskuinfo.colorname = sku['colorname']
                    session.add(orderskuinfo)
                    sku_info = get_model_return_dict(self.sgoods.get_sku_status(sku['psid']))
                    session.query(ProductSku).filter(ProductSku.PSid == sku['psid'])\
                        .update({"PSstock": sku_info['PSstock'] - sku['number']})

            # 更改用户购物车商品状态
            for psid in all_psid:
                session.query(ShoppingCart).filter(ShoppingCart.USid == request.user.id).filter(ShoppingCart.PSid == psid)\
                    .update({"SCstatus": 0})
            # 插入代理消息
            user = {}
            user['USmount'] = user_info['USmount'] - mount - real_PRlogisticsfee
            session.query(User).filter_by(USid=request.user.id).update(user)
            agentmessage = AgentMessage()
            agentmessage.AMid = str(uuid.uuid4())
            agentmessage.USid = request.user.id
            agentmessage.AMdate = OIcreatetime
            agentmessage.AMtype = 0
            agentmessage.AMcontent = u'您的订单创建成功，订单号为' + ' ' + str(OIsn)
            session.add(agentmessage)

            performance = Performance()   # 插入业绩表
            performance.USid = request.user.id
            performance.REmonth = datetime.strftime(datetime.now(), format_for_db)[0:6]
            performance.PEid = str(uuid.uuid4())
            performance.PEdiscountnum = discountnum
            performance.PEcreatetime = datetime.strftime(datetime.now(), format_for_db)
            session.add(performance)

            moneyrecord = MoneyRecord()  # 插入收支记录表
            moneyrecord.MRid = str(uuid.uuid4())
            moneyrecord.MRtype = 1
            moneyrecord.OIid = OIsn
            moneyrecord.MRamount = -(mount + real_PRlogisticsfee)
            moneyrecord.MRcreatetime = datetime.strftime(datetime.now(), format_for_db)
            moneyrecord.USid = request.user.id
            session.add(moneyrecord)
            session.commit()
        except stockerror as e:
            session.rollback()
            return STOCK_NOT_ENOUGH
        except Exception as e2:
            session.rollback()
            print e2.message
            return SYSTEM_ERROR
        finally:
            session.close()
        response = import_status("create_order_success", "OK")
        response['success'] = True
        return response

    @verify_token_decorator
    def get_order_list(self):
        if is_tourist():
            return TOKEN_ERROR
        data = request.json
        if not data:
            return PARAMS_MISS
        try:
            type = int(data.get('type'))
            page = int(data.get('page'))
            count = int(data.get('count'))
        except:
            return PARAMS_ERROR
        order_return_list = []
        if type == 0:
            order_list = get_model_return_list(self.sorder.get_allorder_list(request.user.id, page, count))
            state0 = int(self.sorder.get_total_order_num(request.user.id)) if self.sorder.get_total_order_num(
                request.user.id) else 0
            state1 = int(self.sorder.get_order_num(request.user.id, 1)) if self.sorder.get_order_num(
                request.user.id, 1) else 0
            state2 = int(self.sorder.get_order_num(request.user.id, 2)) if self.sorder.get_order_num(
                request.user.id, 2) else 0
            state3 = int(self.sorder.get_order_num(request.user.id, 3)) if self.sorder.get_order_num(
                request.user.id, 3) else 0
            state4 = int(self.sorder.get_order_num(request.user.id, 4)) if self.sorder.get_order_num(
                request.user.id, 4) else 0
            state1 = state1 + state4
            for order in order_list:
                product_list = get_model_return_list(self.sorder.get_product_list(order['OIid']))
                for product in product_list:
                    product['PRnum'] = 0
                    sku_list = get_model_return_list(self.sorder.get_sku_list_by_opiid(product['OPIid']))
                    for sku in sku_list:
                        product['PRnum'] = product['PRnum'] + sku['number']
                    product['skulist'] = sku_list
                order['product_list'] = product_list
                from common.timeformat import get_web_time_str
                order['OIcreatetime'] = get_web_time_str(order['OIcreatetime'])
                order_return_list.append(order)
            response = import_status("get_orderlist_success", "OK")
            response['data'] = order_return_list
            response['state0_num'] = state0
            response['state1_num'] = state1
            response['state2_num'] = state2
            response['state3_num'] = state3
            return response
        else:
            order_list = get_model_return_list(self.sorder.get_order_list(request.user.id, type, page, count))
            if type == 1:
                order_list = order_list + get_model_return_list(self.sorder.get_order_list(request.user.id, 4, page, count))
                new_list = sorted(order_list, key=lambda order: order['OIcreatetime'], reverse=True)
                order_list = new_list
            if not order_list:
                response = import_status("get_orderlist_success", "OK")
                response['data'] = order_return_list
                return response
            for order in order_list:
                product_list = get_model_return_list(self.sorder.get_product_list(order['OIid']))
                for product in product_list:
                    product['PRnum'] = 0
                    sku_list = get_model_return_list(self.sorder.get_sku_list_by_opiid(product['OPIid']))
                    for sku in sku_list:
                        product['PRnum'] = product['PRnum'] + sku['number']
                    product['skulist'] = sku_list
                order['product_list'] = product_list
                from common.timeformat import get_web_time_str
                order['OIcreatetime'] = get_web_time_str(order['OIcreatetime'])
                order_return_list.append(order)
            response = import_status("get_orderlist_success", "OK")
            response['data'] = order_return_list
            return response

    @verify_token_decorator
    def get_order_details(self):
        if is_tourist():
            return TOKEN_ERROR
        data = request.json
        if not data:
            return PARAMS_MISS
        try:
            OIsn = int(data.get('OIsn'))
        except:
            return PARAMS_ERROR
        detail = get_model_return_dict(self.sorder.get_order_details(OIsn))
        from common.timeformat import get_web_time_str
        detail['createtime'] = get_web_time_str(detail['OIcreatetime'])
        product_list = get_model_return_list(self.sorder.get_product_list(detail['OIid']))
        for product in product_list:
            product['PRnum'] = 0
            sku_list = get_model_return_list(self.sorder.get_sku_list_by_opiid(product['OPIid']))
            for sku in sku_list:
                product['PRnum'] = product['PRnum'] + sku['number']
            product['skulist'] = sku_list
        detail['product_list'] = product_list
        response = import_status("get_orderdetails_success", "OK")
        response['data'] = detail
        return response

    @verify_token_decorator
    def get_all_order(self):
        if not is_admin():
            return AUTHORITY_ERROR
        params = ['page_size', 'page_num', 'oisn', 'starttime', 'endtime', 'status', 'username', 'userphonenum', 'productname']
        try:
            data = request.json
            for param in params:
                if param not in data:
                    response = {}
                    response['message'] = u"参数缺失"
                    response['paramname'] = param
                    response['status'] = 405
                    return response
        except:
            return PARAMS_ERROR
        page_size = data.get('page_size')
        page_num = data.get('page_num')
        oisn = data.get('oisn')
        starttime = str(data.get('starttime')) + '000000' if data.get('starttime') else None
        endtime = data.get('endtime') + '000000' if data.get('endtime') else None
        status = data.get('status')
        username = data.get('username')
        userphonenum = data.get('userphonenum')
        productname = data.get('productname')
        all_order = get_model_return_list(self.sorder.get_all_order(oisn, starttime, endtime, status, username, userphonenum))
        return_list = []
        for order in all_order:
            detail = get_model_return_dict(self.sorder.get_order_details(order['OIsn']))
            from common.timeformat import get_web_time_str
            order['OIcreatetime'] = get_web_time_str(order['OIcreatetime'])
            product_list = get_model_return_list(self.sorder.get_product_list(detail['OIid']))
            for product in product_list:
                product['PRnum'] = 0
                sku_list = get_model_return_list(self.sorder.get_sku_list_by_opiid(product['OPIid']))
                for sku in sku_list:
                    product['PRnum'] = product['PRnum'] + sku['number']
                product['skulist'] = sku_list
            order['product_list'] = product_list
            if productname:
                for product in product_list:
                    if productname in product['PRname']:
                        return_list.append(order)
                        break
            else:
                return_list.append(order)

        mount = len(return_list)
        page = mount / page_size
        if page == 0 or page == 1 and mount % page_size == 0:
            real_return_list = return_list[0:]
        else:
            if ((mount - (page_num - 1) * page_size) / page_size) >= 1 and \
                    (mount - (page_num  * page_size)) > 0:
                real_return_list = return_list[((page_num - 1) * page_size):(page_num * page_size)]
            else:
                real_return_list = return_list[((page_num - 1) * page_size):]

        response = import_status("get_allorder_success", "OK")
        response['data'] = real_return_list
        response['mount'] = mount
        return response

    @verify_token_decorator
    def update_order(self):
        if not is_admin():
            return AUTHORITY_ERROR
        try:
            data = request.json
            oisn = data.get('oisn')
            expressname = data.get('expressname')
            expressnum = data.get('expressnum')
        except:
            return PARAMS_ERROR
        detail = get_model_return_dict(self.sorder.get_order_details(oisn))
        if not detail:
            return NOT_FOUND_ORDER
        session = db_session()
        try:
            update = {}
            update['OIstatus'] = 2
            update['expressname'] = expressname
            update['expressnum'] = expressnum
            session.query(OrderInfo).filter(OrderInfo.OIsn == oisn).update(update)
            monthnow = datetime.strftime(datetime.now(), format_for_db)[0:6]
            amount_data = self.saccount.get_user_date(detail['USid'], monthnow)
            order = get_model_return_dict(self.sorder.get_order_details(oisn))
            user = self.smycenter.get_user_basicinfo(detail['USid'])  # 插入销售表，有数据就更新
            if not user:
                raise dberror
            user = get_model_return_dict(user)
            if not order:
                raise dberror
            if amount_data:
                amount_data = get_model_return_dict(amount_data)
                new_data = {}
                new_data['performance'] = amount_data['performance'] + order['discountnum']
                try:
                    session.query(Amount).filter(Amount.USid == detail['USid']).filter(Amount.AMmonth == monthnow).update(new_data)
                except:
                    raise dberror
            else:
                amount = Amount()
                amount.USid = detail['USid']
                amount.AMid = str(uuid.uuid4())
                amount.USagentid = user['USagentid']
                amount.performance = order['discountnum']
                amount.USname = user['USname']
                amount.AMstatus = 1
                amount.USheadimg = user['USheadimg']
                amount.AMcreattime = datetime.strftime(datetime.now(), format_for_db)
                amount.AMmonth = monthnow
                session.add(amount)
            session.commit()
        except Exception as e:
            print e
            session.rollback()
            return SYSTEM_ERROR
        finally:
            session.close()
        reponse = import_status("update_order_success", "OK")
        detail = get_model_return_dict(self.sorder.get_order_details(oisn))
        from common.timeformat import get_web_time_str
        detail['OIcreatetime'] = get_web_time_str(detail['OIcreatetime'])
        product_list = get_model_return_list(self.sorder.get_product_list(detail['OIid']))
        detail['product_list'] = product_list
        reponse['data'] = detail
        return reponse

    @verify_token_decorator
    def get_willsend_products(self):
        if not is_admin():
            return TOKEN_ERROR
        # workbook = xlrd.open_workbook(r'/Users/fx/Desktop/项目相关/1.xls')
        # print (workbook.sheet_names())
        # sheet = workbook.sheet_names()[0]
        # sheet_data = workbook.sheet_by_name(sheet)
        # print(sheet_data)
        # print (sheet_data.name, sheet_data.nrows, sheet_data.ncols)
        # rows = sheet_data.row_values(0)  # 获取第一行内容
        # cols = sheet_data.col_values(0)  # 获取第一列内容
        # print (rows)
        try:
            data = request.json
            oisnlist = data.get('oisnlist')
        except:
            return PARAMS_ERROR
        new_oisn_list = []
        for oisn in oisnlist:
            order = get_model_return_dict(self.sorder.get_order_details(str(oisn)))
            if order['OIstatus'] == 1:
                new_oisn_list.append(order)
        style = xlwt.XFStyle()
        font = xlwt.Font()
        font.name = u'宋体'
        font.bold = True
        style.font = font
        time_now = datetime.strftime(datetime.now(), format_for_db)
        workbook = xlwt.Workbook(encoding='utf-8')
        worksheet = workbook.add_sheet('sheet1')
        # worksheet.write_merge()
        worksheet.write(0, 0, label='订单号', style=style)
        worksheet.write(0, 1, label='收货地址', style=style)
        worksheet.write(0, 2, label='卖家备注', style=style)
        worksheet.write(0, 3, label='发件人姓名', style=style)
        worksheet.write(0, 4, label='发件人电话', style=style)
        worksheet.write(0, 5, label='发件人地址', style=style)
        worksheet.write(0, 6, label='发货商品', style=style)
        font = xlwt.Font()
        font.name = u'宋体'
        font.bold = False
        style.font = font
        url = ''
        session = db_session()
        try:
            if new_oisn_list:
                for i, order in enumerate(new_oisn_list):
                    oisn = order['OIsn']
                    username = order['username']
                    phone = order['userphonenum']
                    provincename = order['provincename']
                    cityname = order['cityname']
                    areaname = order['areaname'] if order['areaname'] else ''
                    details = order['details']
                    address = username + ' ' + phone + ' ' + provincename + cityname + areaname + details
                    OInote = order['OInote']
                    product_list = get_model_return_list(self.sorder.get_product_list(order['OIid']))
                    productname = self.get_product_name(product_list)
                    worksheet.write(i+1, 0, label=oisn, style=style)
                    worksheet.write(i+1, 1, label=address, style=style)
                    worksheet.write(i+1, 2, label=OInote, style=style)
                    worksheet.write(i+1, 3, label=self.conf.get('account', 'sendname'), style=style)
                    worksheet.write(i+1, 4, label=self.conf.get('account', 'sendphone'), style=style)
                    worksheet.write(i+1, 5, label=self.conf.get('account', 'sendaddress'), style=style)
                    session.query(OrderInfo).filter(OrderInfo.OIsn == oisn).update({"OIstatus": 4})
                    worksheet.write(i+1, 6, label=productname, style=style)
            if platform.system() == "Windows":
                rootdir = "D:/task"
            else:
                rootdir = "/opt/beili/file/"
            if not os.path.isdir(rootdir):
                os.makedirs(rootdir)
            filename = get_db_time_str() + "." + 'xls'
            filepath = os.path.join(rootdir, filename)
            print(filepath)
            workbook.save(filepath)
            url = QRCODEHOSTNAME + "/file/" + filename
        except Exception as e:
            print e
            session.rollback()
            return SYSTEM_ERROR
        finally:
            session.commit()
        response = import_status("get_willsend_products_success", "OK")
        response['data'] = url
        return response

    def get_product_name(self, list):
        name = ''
        for product in list:
            name = name + '' + product['PRname']
        return name

    @verify_token_decorator
    def cancel_order(self):
        if is_tourist():
            return TOKEN_ERROR
        try:
            data = request.json
            oisn = data.get('oisn')
        except:
            return PARAMS_ERROR
        order = get_model_return_dict(self.sorder.get_order_details(oisn))
        if not order:
            print order
            return SYSTEM_ERROR
        if int(order['OIstatus']) != 1:
            return CANNOT_CANCEL
        session = db_session()
        try:
            session.query(OrderInfo).filter(OrderInfo.OIsn == oisn).update({"OIstatus": 5})
            user = self.smycenter.get_user_basicinfo(request.user.id)
            if not user:
                raise dberror
            user = get_model_return_dict(user)
            session.query(User).filter(User.USid == request.user.id).update({"USmount": user['USmount'] + order['OImount']})
            moneyrecord = MoneyRecord()  # 插入收支记录表
            moneyrecord.MRid = str(uuid.uuid4())
            moneyrecord.MRtype = 8
            moneyrecord.OIid = oisn
            moneyrecord.MRamount = order['OImount']
            moneyrecord.MRcreatetime = datetime.strftime(datetime.now(), format_for_db)
            moneyrecord.USid = request.user.id
            session.add(moneyrecord)
            session.commit()
        except Exception as e:
            print e
            session.rollback()
            return SYSTEM_ERROR
        finally:
            session.close()
        response = import_status("cancel_order_success", "OK")
        return response



    def timer_fun(self):  # 定时器
        global TIMER
        print "start timer_fun !"
        import datetime
        time_now = datetime.datetime.strftime(datetime.datetime.now(), '%Y%m%d')
        print time_now
        order_list = get_model_return_list(self.sorder.get_all_order(None, None, None, 2, None, None))
        if order_list:
            for order in order_list:
                time = datetime.datetime.strptime(order['OIcreatetime'][0:8], '%Y%m%d')
                print 'time', time
                days_10 = (time + datetime.timedelta(days=10)).strftime("%Y%m%d")
                print 'days_10', days_10
                if time_now > days_10:
                    self.sorder.update_order(order['OIsn'], {"OIstatus": 3})
        # 继续添加定时器，周期执行，否则只会执行一次
        TIMER = threading.Timer(3600 * 24, self.timer_fun)
        TIMER.start()

