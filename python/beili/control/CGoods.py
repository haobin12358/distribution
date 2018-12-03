# *- coding:utf8 *-
import re
import sys
import os
import uuid
from datetime import datetime
from common.timeformat import format_for_db, get_random_str
from flask import request
import copy
# import logging

from service.DBSession import db_session
from config.response import PARAMS_MISS, NO_THIS_CATEGORY, PARAMS_ERROR, PRODUCE_CATEGORY_EXIST, PRODUCE_CATEGORY_NOT_EXIST\
    , AUTHORITY_ERROR, SYSTEM_ERROR, TOKEN_ERROR, PRODUCE_CATEGORY_HAS_PRODUCT, REPERT_COLOR, REPERT_SIZE, STOCK_NOT_ENOUGH\
    , PRODUCT_STATUS_WRONG, HAS_SECOND_CATEGORY, CAN_NOT_CHANGE_LEVEL
from config.setting import QRCODEHOSTNAME
from common.token_required import verify_token_decorator, usid_to_token, is_tourist, is_admin, is_ordirnaryuser,is_superadmin
from common.import_status import import_status
from common.timeformat import get_db_time_str
from common.get_model_return_list import get_model_return_list, get_model_return_dict
from service.SGoods import SGoods
from models.model import ProductSku
from common.timeformat import get_web_time_str
import platform

sys.path.append(os.path.dirname(os.getcwd()))


class CGoods():

    def __init__(self):
        self.sgoods = SGoods()

    def get_product_list(self):
        args = request.args.to_dict()
        try:
            page_num = int(args.get("page_num"))
            page_size = int(args.get("page_size"))
            PRstatus = int(args.get("PRstatus"))
            PRname = args.get("PRname")
            PAid = str(args.get("PAid"))
            PAtype = int(args.get("PAtype"))
            print args
        except:
            return PARAMS_MISS
        product_list = []
        if PAid == '':
            return PARAMS_ERROR
        if PAid == str(0):
            print 'PAid == str(0)'
            product_list = get_model_return_list(self.sgoods.admin_get_product(PRstatus, PRname))
            print product_list
        elif int(PAtype) == 1:
            print 'int(PAtype) == 1'
            paid_list = get_model_return_list(self.sgoods.get_childid(str(PAid)))
            for paid in paid_list:
                product_list = product_list + get_model_return_list(
                    self.sgoods.admin_get_product(PRstatus, PRname, paid['PAid']))
        elif int(PAtype) == 2:
            print 'int(PAtype) == 2'
            product_list = product_list + get_model_return_list(
                self.sgoods.admin_get_product(PRstatus, PRname, PAid))
        for product in product_list:
            print 'for product in product_list'
            category = get_model_return_dict(self.sgoods.get_category_byid(product['PAid']))
            product['firstpaid'] = category['Parentid']
            parent_category = get_model_return_dict(self.sgoods.get_category_byid(category['Parentid']))
            product['firstpaname'] = parent_category['PAname']
            product['categoryname'] = category['PAname']
            product['PRcreatetime'] = get_web_time_str(product['PRcreatetime'])

        mount = len(product_list)
        page = mount / page_size
        if page == 0 or page == 1 and mount % page_size == 0:
            return_list = product_list[0:]
        else:
            if ((mount - (page_num - 1) * page_size) / page_size) >= 1 and \
                    (mount - (page_num * page_size)) > 0:
                return_list = product_list[((page_num - 1) * page_size):(page_num * page_size)]
            else:
                return_list = product_list[((page_num - 1) * page_size):]
        response = import_status("get_product_list_success", "OK")
        response["data"] = return_list
        response['mount'] = mount
        return response

    @verify_token_decorator
    def get_product_details(self):
        if is_tourist():
            return TOKEN_ERROR
        try:
            data = request.json
            prid = data.get('prid')
        except:
            return PARAMS_ERROR
        details = get_model_return_dict(self.sgoods.get_product_details(prid))
        details['sowingmap'] = details['sowingmap'].split(",")
        sku_list = get_model_return_list(self.sgoods.get_sku_by_prid(prid))
        response = import_status("get_product_detail_success", "OK")
        response['data'] = details
        response['data']['skulist'] = sku_list
        return response


    @verify_token_decorator
    def get_product(self):
        self.json_param_miss("get")
        args = request.args.to_dict()
        try:
            PRid = args.get("PRid")
            product = get_model_return_dict(self.sgoods.get_product(PRid))
            from common.timeformat import get_web_time_str
            product['PRcreatetime'] = get_web_time_str(product['PRcreatetime'])
        except Exception as e:
            print(e.message)
            return PARAMS_MISS
        response = import_status("get_product_success", "OK")
        response["data"] = product
        return response

    @verify_token_decorator
    def get_product_category_list(self):
        # 获取商品分类列表
        if is_tourist():
            return TOKEN_ERROR
        first_level = get_model_return_list(self.sgoods.get_first_product_category_status(str(0)))
        options = []
        for parent_category in first_level:
            product_category_list = {}
            parnetid = parent_category['PAid']
            parentname = parent_category['PAname']
            product_category_list['PAid'] = parnetid
            product_category_list['PAname'] = parentname
            child_category = get_model_return_list(self.sgoods.get_first_product_category(parnetid))
            product_category_list['child_category'] = child_category
            options.append(product_category_list)
        response = import_status("get_product_category_list_success", "OK")
        response['data'] = options
        return response

    @verify_token_decorator
    def add_product_category(self):
        #添加商品分类
        #self.json_param_miss("post")
        if not is_admin():
            return AUTHORITY_ERROR
        try:
            data = request.json
            print data, type(data)
            PAid = data.get('PAid')
            PAname = data.get('PAname')
            PAtype = data.get('PAtype')
            Parentid = data.get('Parentid')
        except Exception as e:
            print e.message
            return PARAMS_ERROR
        try:
            get_PAstatus = get_model_return_dict(self.sgoods.get_product_category(PAid))
            if get_PAstatus:
                update_category = {}
                update_category['PAname'] = PAname
                update_category['Parentid'] = Parentid if Parentid else '0'
                print Parentid
                self.sgoods.update_product_category(PAid, update_category)
            else:
                PAid = str(uuid.uuid1())
                Parentid = Parentid if Parentid else '0'
                self.sgoods.add_product_category(PAid, PAname, PAtype, Parentid)

        except Exception as e:
            print e.message
            return PARAMS_MISS
        response = import_status("add_product_category_success", "OK")
        #response["data"] = product_category
        return response

    @verify_token_decorator
    def update_category(self):
        #更新商品分类
        #self.json_param_miss("post")
        if not is_admin():
            return AUTHORITY_ERROR
        try:
            data = request.json
            PAid = data.get('PAid')
            PAname = data.get('PAname')
            PAtype = data.get('PAtype')
            Parentid = data.get('Parentid')
        except:
            return PARAMS_ERROR
        try:
            get_PAstatus = get_model_return_dict(self.sgoods.get_product_category(PAid))
            if not get_PAstatus:
                return PRODUCE_CATEGORY_NOT_EXIST
            if PAtype != get_PAstatus['PAtype']:
                return CAN_NOT_CHANGE_LEVEL
            update_category = {}
            update_category['PAname'] = PAname
            update_category['PAtype'] = PAtype
            update_category['Parentid'] = Parentid
            print Parentid
            self.sgoods.update_product_category(PAid, update_category)
        except Exception as e :
            print Exception
            return PARAMS_MISS
        response = import_status("update_product_category_success", "OK")
        return response

    @verify_token_decorator
    def delete_category(self):
        #删除商品分类
        #self.json_param_miss("post")
        if not is_admin():
            return AUTHORITY_ERROR
        try:
            data = request.json
            PAid = data.get('PAid')

        except:
            return PARAMS_ERROR
        try:
            get_PAstatus = get_model_return_dict(self.sgoods.get_product_category(PAid))
            if not get_PAstatus:
                return PRODUCE_CATEGORY_NOT_EXIST
            # elif get_Parentid == 0:
            #     self.sgoods.add_product_category(PAid, PAname, PAtype)
            if get_PAstatus['PAtype'] == 1:
                categorylist = get_model_return_list(self.sgoods.get_first_product_category_status(PAid))
                if categorylist:
                    return HAS_SECOND_CATEGORY
            if get_PAstatus['PAtype'] == 2:
                product_list = get_model_return_list(self.sgoods.get_product_by_paid(paid=PAid))
                if product_list:
                    return PRODUCE_CATEGORY_HAS_PRODUCT
            delete_category = {}
            delete_category['PAstatus'] = False
            self.sgoods.delete_category(PAid, delete_category)
        except Exception as e:
            print e.message
            return PARAMS_MISS
        response = import_status("delete_product_category_success", "OK")
        return response



    #@verify_token_decorator
    def get_product_category(self):
        args = request.args.to_dict()
        try:
            PAtype = int(args.get("PAtype"))
            if PAtype == 1:
                product_category = (get_model_return_list(self.sgoods.get_first_product_category(str(0))))
            elif PAtype == 2:
                PAid = args.get("PAid")
                product_category = (get_model_return_list(self.sgoods.get_first_product_category(PAid)))
            else:
                return NO_THIS_CATEGORY
        except Exception as e:
            print(e.message)
            return PARAMS_MISS
        response = import_status("get_product_category_success", "OK")
        response["data"] = product_category
        return response

    @verify_token_decorator
    def create_update_product(self):
        if not is_admin():
            return AUTHORITY_ERROR
        params = ['paid', 'prname', 'prpic', 'sowingmap', 'proldprice', 'prprice', 'skulist', 'prlogisticsfee'
            , 'prdiscountnum', 'prstatus']
        data = request.json
        for param in params:
            if param not in data:
                response = {}
                response['message'] = u"参数缺失"
                response['paramname'] = param
                response['status'] = 405
                return response
        paid = data.get('paid')
        prname = data.get('prname')
        prpic = data.get('prpic')
        proldprice = data.get('proldprice')
        prprice = data.get('prprice')
        prlogisticsfee = data.get('prlogisticsfee')
        prdiscountnum = data.get('prdiscountnum')
        prstatus = data.get('prstatus')
        prid = data.get('prid')
        skulist = data.get('skulist')
        sowingmap = ",".join(data.get('sowingmap'))
        session = db_session()
        try:
            if prid:
                product = {}
                product['PAid'] = paid
                product['PRname'] = prname
                product['PRpic'] = prpic
                product['PRoldprice'] = proldprice
                product['PRprice'] = prprice
                product['PRlogisticsfee'] = prlogisticsfee
                product['PRstatus'] = prstatus
                product['PAdiscountnum'] = prdiscountnum
                product['sowingmap'] = sowingmap
                result = self.sgoods.update_product(session, prid, product)
                if not result:
                    return SYSTEM_ERROR
                skuid_list = get_model_return_list(self.sgoods.get_all_skuid(session, prid))
                db_skuid_list = []
                for id in skuid_list:
                    db_skuid_list.append(id['PSid'])
                web_skuid_list = []
                for sku in skulist:
                    if not sku['psid']:
                        coid = sku['coid']
                        colorname = sku['colorname']
                        siid = sku['siid']
                        sizename = sku['sizename']
                        stock = sku['stock']
                        time_now = datetime.strftime(datetime.now(), format_for_db)
                        self.sgoods.create_sku(session, prid, coid, colorname, siid, sizename, stock, time_now)
                    if sku['psid']:
                        web_skuid_list.append(sku['psid'])
                        self.sgoods.update_sku(session, prid, sku['psid'], {'PSstock': sku['stock']})
                for dbskuid in db_skuid_list:
                    if dbskuid not in web_skuid_list:
                        session.query(ProductSku).filter(ProductSku.PRid == prid).filter(ProductSku.PSid == dbskuid)\
                        .update({'PSstatus': 0})
                session.commit()
                response = import_status("update_product_success", "OK")
                return response
            else:
                time_now = datetime.strftime(datetime.now(), format_for_db)
                prid = str(uuid.uuid4())
                result = self.sgoods.create_product(session, prid, paid, prname, prpic, proldprice, prprice
                                           , prlogisticsfee, prstatus, prdiscountnum, time_now, sowingmap)
                if not result:
                    return SYSTEM_ERROR
                for sku in skulist:
                    coid = sku['coid']
                    colorname = sku['colorname']
                    siid = sku['siid']
                    sizename = sku['sizename']
                    stock = sku['stock']
                    time_now = datetime.strftime(datetime.now(), format_for_db)
                    self.sgoods.create_sku(session, prid, coid, colorname, siid, sizename, stock, time_now)
                session.commit()
                response = import_status("create_product_success", "OK")
                return response
        except Exception as e:
            print e
            session.rollback()
            return SYSTEM_ERROR
        finally:
            session.close()

    @verify_token_decorator
    def withdraw_product(self):
        if not is_admin():
            return TOKEN_ERROR
        try:
            data = request.json
            prid = data.get('prid')
        except:
            return PARAMS_ERROR
        if not prid:
            return PARAMS_ERROR
        result = self.sgoods.withdraw_product(prid)
        if not result:
            return SYSTEM_ERROR
        response = import_status("withdraw_product_success", "OK")
        return response


    @verify_token_decorator
    def add_sowingmap(self):
        if not is_admin():
            return TOKEN_ERROR
        try:
            data = request.json
            type = data['type']
            urls = data['urls']
        except:
            return PARAMS_ERROR 
        if int(type) < 0:
            return PARAMS_ERROR
        result = self.sgoods.update_sowingmap_by_type(type)
        if not result:
            return SYSTEM_ERROR
        result = self.sgoods.add_sowingmap(type, urls)
        if not result:
            return SYSTEM_ERROR
        response = import_status("add_sowingmap_success", "OK")
        return response

    @verify_token_decorator
    def get_sowingmap(self):
        if is_tourist():
            return TOKEN_ERROR
        mallUrls = []
        personUrls = []
        list = get_model_return_list(self.sgoods.get_sowingmap())
        for pic in list:
            if pic['SMtype'] == 1:
                personUrls.append(pic)
            if pic['SMtype'] == 2:
                mallUrls.append(pic)
        data = {}
        data['mallUrls'] = mallUrls
        data['personUrls'] = personUrls
        response = import_status("get_sowingmap_success", "OK")
        response['data'] = data
        return response

    @verify_token_decorator
    def delete_sowingmap(self):
        if not is_admin():
            return TOKEN_ERROR
        try:
            data = request.json
            smid = data.get('smid')
        except:
            return PARAMS_ERROR
        if not smid:
            return PARAMS_MISS
        result = self.sgoods.update_sowingmap(smid)
        if not result:
            return SYSTEM_ERROR
        response = import_status("delete_sowingmap_success", "OK")
        return response


    def json_param_miss(self, type):
        if is_tourist():
            return {
                "status": 405,
                "status_code": 405003,
                "message": "未登陆"
            }
        if type == "get":
            pass
        elif type == "post":
            json_data = request.json
            if not json_data:
                return PARAMS_MISS
        else:
            pass

    @verify_token_decorator
    def add_color(self):
        if not is_admin():
            return TOKEN_ERROR
        try:
            data = request.json
            colorname = data.get("colorname")
        except Exception as e:
            print e
            return PARAMS_ERROR
        is_same = self.sgoods.get_color_by_colorname(colorname.encode('utf-8'))
        if is_same:
            return REPERT_COLOR
        time_now = datetime.strftime(datetime.now(), format_for_db)
        result = self.sgoods.add_color(colorname, time_now)
        if not result:
            return SYSTEM_ERROR
        response = import_status("add_color_success", "OK")
        return response

    @verify_token_decorator
    def get_color(self):
        if not is_admin():
            return TOKEN_ERROR
        list = get_model_return_list(self.sgoods.get_color_list())
        response = import_status("get_color_list_success", "OK")
        response['data'] = list
        return response

    @verify_token_decorator
    def add_size(self):
        if not is_admin():
            return TOKEN_ERROR
        try:
            data = request.json
            sizename = data.get("sizename")
        except Exception as e:
            print e
            return PARAMS_ERROR
        is_same = self.sgoods.get_color_by_sizename(sizename.encode('utf-8'))
        if is_same:
            return REPERT_SIZE
        time_now = datetime.strftime(datetime.now(), format_for_db)
        result = self.sgoods.add_size(sizename, time_now)
        if not result:
            return SYSTEM_ERROR
        response = import_status("add_size_success", "OK")
        return response

    @verify_token_decorator
    def get_size(self):
        if not is_admin():
            return TOKEN_ERROR
        list = get_model_return_list(self.sgoods.get_size_list())
        response = import_status("get_size_list_success", "OK")
        response['data'] = list
        return response

    @verify_token_decorator
    def add_shoppingcart(self):
        if is_tourist():
            return TOKEN_ERROR
        params = ['prid', 'psid', 'colorid', 'colorname', 'sizeid', 'sizename', 'number']
        data = request.json
        for param in params:
            if param not in data:
                response = {}
                response['message'] = u"参数缺失"
                response['paramname'] = param
                response['status'] = 405
                return response
        prid = data.get('prid')
        psid = data.get('psid')
        sku_stock = get_model_return_dict(self.sgoods.get_sku_stock(psid))['PSstock']
        is_exist = get_model_return_dict(self.sgoods.check_is_exist_sku(request.user.id, prid, psid))
        if is_exist:
            new_number = is_exist['number'] + int(data.get('number'))
            if sku_stock < new_number:
                return STOCK_NOT_ENOUGH
            update = {
                "number": new_number
            }
            result = self.sgoods.update_user_sku(request.user.id, psid, update)
            if not result:
                return SYSTEM_ERROR
        else:
            if int(data.get('number')) > sku_stock:
                return STOCK_NOT_ENOUGH
            result = self.sgoods.add_shoppingcart(request.user.id, data)
            if not result:
                return SYSTEM_ERROR
        response = import_status("add_shoppingcart_success", "OK")
        return response

    @verify_token_decorator
    def get_shoppingcart(self):
        if not is_ordirnaryuser():
            return TOKEN_ERROR
        product_list = get_model_return_list(self.sgoods.get_shoppingcart_product(request.user.id))
        for product in product_list:
            product_info = get_model_return_dict(self.sgoods.get_product_details(product['PRid']))
            product['PRpic'] = product_info['PRpic']
            product['PRlogisticsfee'] = product_info['PRlogisticsfee']
            product['PRprice'] = product_info['PRprice']
            product['PRname'] = product_info['PRname']
            product_status = self.sgoods.get_product_info(product['PRid'])
            sku_list = get_model_return_list(self.sgoods.get_shoppingcart_sku(request.user.id, product['PRid']))
            for sku in sku_list:
                sku_stok = get_model_return_dict(self.sgoods.get_sku_stock(sku['PSid']))
                if int(sku['number']) > int(sku_stok['PSstock']):
                    sku['SCstatus'] = 2
                sku_status = self.sgoods.get_sku_status(sku['PSid'])
                if not sku_status:
                    sku['SCstatus'] = 3
                if not product_status:
                    sku['SCstatus'] = 4
            product['skulist'] = sku_list
        if len(product_list) != 0:
            return_list = sorted(product_list, key=lambda product: product['skulist'][0]['SCcreatetime'], reverse=True)
        else:
            return_list = []
        response = import_status("get_shoppingcart_success", "OK")
        response['data'] = return_list
        return response

    @verify_token_decorator
    def delete_shoppingcart_sku(self):
        if not is_ordirnaryuser():
            return TOKEN_ERROR
        try:
            data = request.json
            scidlist = data.get('scidlist')
        except:
            return PARAMS_ERROR
        update = {
            "SCstatus": 0
        }
        session = db_session()
        try:
            for scid in scidlist:
                self.sgoods.update_user_sku_by_scid(session, request.user.id, str(scid), update)
            session.commit()
        except Exception as e:
            print e
            session.rollback()
            return SYSTEM_ERROR
        finally:
            session.close()
        response = import_status("delete_shoppingcart_sku_success", "OK")
        return response

    @verify_token_decorator
    def update_shoppingcart_number(self):
        if not is_ordirnaryuser():
            return TOKEN_ERROR
        try:
            data = request.json
            psid = data.get('psid')
            number = data.get('number')
        except:
            return PARAMS_ERROR
        sku_stock = get_model_return_dict(self.sgoods.get_sku_stock(psid))
        if sku_stock['PSstatus'] != 1:
            return PRODUCT_STATUS_WRONG
        if int(number) > sku_stock['PSstock']:
            return STOCK_NOT_ENOUGH
        if int(number) < 0:
            return PARAMS_MISS
        result = self.sgoods.update_user_sku(request.user.id, psid, {"number": number})
        if not result:
            return SYSTEM_ERROR
        response = import_status("change_shoppingcart_number_success", "OK")
        return response

