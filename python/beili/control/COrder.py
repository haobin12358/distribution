# *- coding:utf8 *-
import re
import sys
import os
import uuid
import random
from flask import request
# import logging
from config.response import PARAMS_MISS, SYSTEM_ERROR, PARAMS_ERROR, TOKEN_ERROR, AUTHORITY_ERROR, STOCK_NOT_ENOUGH,\
        NO_ENOUGH_MOUNT, NO_BAIL, NO_ADDRESS, NOT_FOUND_ORDER
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
from common.timeformat import format_for_db, get_random_str
from models.model import User, AgentMessage, Performance, Amount, Reward, MoneyRecord
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
        for params in params_list:
            if params not in data:
                return PARAMS_MISS
        try:
            UAid = data['UAid']
            OInote = data['OInote']
            product_list = data['product_list']
            PRlogisticsfee = float(data['PRlogisticsfee'])
            totalprice = float(data['totalprice'])
        except:
            return PARAMS_ERROR
        if len(product_list) > 1:
            real_PRlogisticsfee = 0
        else:
            real_PRlogisticsfee = get_model_return_dict(self.sgoods.get_product(product_list[0]['PRid']))['PRlogisticsfee']
            if not real_PRlogisticsfee:
                real_PRlogisticsfee = 0
        user_info = get_model_return_dict(self.smycenter.get_user_basicinfo(request.user.id))
        if not user_info:
            return SYSTEM_ERROR
        if user_info['USbail'] < float(self.conf.get('account', 'bail')):
            return NO_BAIL
        mount = 0
        new_list = []
        discountnum = 0
        product_num = 0
        try:
            for product in product_list:
                num = product['PRnum']
                if num > 1:
                    real_PRlogisticsfee = 0
                check_product = get_model_return_dict(self.sgoods.get_product(product['PRid']))
                mount = mount + num * check_product['PRprice']
                product['PRprice'] = check_product['PRprice']
                product_num = product_num + num
                discountnum = discountnum + num * check_product['PAdiscountnum']
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
            OIsn = datetime.strftime(datetime.now(), format_for_db) + get_random_str()
            OIcreatetime = datetime.strftime(datetime.now(), format_for_db)
            result = self.sorder.check_stock(new_list)
            if not result:
                raise dberror

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
                                           PRlogisticsfee, provincename, cityname, areaname, details, username, userphonenum, product_num)
            if not result:
                raise dberror
            for product in new_list:
                OPIid = str(uuid.uuid4())
                PRid = product['PRid']
                PRnum = product['PRnum']
                PRname = product['PRname']
                PRimage = get_model_return_dict(self.sgoods.get_product(PRid))['PRpic']
                PRprice = product['PRprice']
                result = self.sorder.add_orderproductinfo(session, OPIid, OIid, PRid, PRname, PRprice, PRnum, PRimage)
                if not result:
                    raise dberror

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

            user = self.smycenter.get_user_basicinfo(request.user.id)  # 插入销售表，有数据就更新
            if not user:
                raise dberror
            user = get_model_return_dict(user)
            monthnow = datetime.strftime(datetime.now(), format_for_db)[0:6]
            amount_data = self.saccount.get_user_date(request.user.id, monthnow)
            if amount_data:
                amount_data = get_model_return_dict(amount_data)
                new_data = {}
                new_data['performance'] = amount_data['performance'] + discountnum
                try:
                    session.query(Amount).filter(Amount.USid == request.user.id).update(new_data)
                except:
                    raise dberror
            else:
                amount = Amount()
                amount.USid = request.user.id
                amount.AMid = str(uuid.uuid4())
                amount.USagentid = user['USagentid']
                amount.performance = discountnum
                amount.USname = user['USname']
                amount.AMstatus = 1
                amount.USheadimg = user['USheadimg']
                amount.AMcreattime = datetime.strftime(datetime.now(), format_for_db)
                amount.AMmonth = datetime.strftime(datetime.now(), format_for_db)[0:6]
                session.add(amount)
            moneyrecord = MoneyRecord()
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
            for order in order_list:
                product_list = get_model_return_list(self.sorder.get_product_list(order['OIid']))
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
            if not order_list:
                response = import_status("get_orderlist_success", "OK")
                response['data'] = order_return_list
                return response
            for order in order_list:
                product_list = get_model_return_list(self.sorder.get_product_list(order['OIid']))
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
        update = {}
        update['OIstatus'] = 2
        update['expressname'] = expressname
        update['expressnum'] = expressnum
        result = self.sorder.update_order(oisn, update)
        if not result:
            return SYSTEM_ERROR
        reponse = import_status("update_order_success", "OK")
        detail = get_model_return_dict(self.sorder.get_order_details(oisn))
        from common.timeformat import get_web_time_str
        detail['OIcreatetime'] = get_web_time_str(detail['OIcreatetime'])
        product_list = get_model_return_list(self.sorder.get_product_list(detail['OIid']))
        detail['product_list'] = product_list
        reponse['data'] = detail
        return reponse