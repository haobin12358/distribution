# *- coding:utf8 *-
import re
import sys
import os
import uuid
import random
from flask import request
# import logging
from config.response import PARAMS_MISS, SYSTEM_ERROR, PARAMS_ERROR, TOKEN_ERROR, AUTHORITY_ERROR, STOCK_NOT_ENOUGH,\
        NO_ENOUGH_MOUNT, NO_BAIL, NO_ADDRESS
from config.setting import QRCODEHOSTNAME
from common.token_required import verify_token_decorator, usid_to_token, is_tourist, is_admin
from common.import_status import import_status
from common.timeformat import get_db_time_str
from config.setting import BAIL
from common.get_model_return_list import get_model_return_list, get_model_return_dict
from service.SUser import SUser
from service.SMessage import SMessage
from service.SOrder import SOrder
from service.SGoods import SGoods
from service.SMyCenter import SMyCenter
from service.DBSession import db_session
import platform
from common.beili_error import stockerror, dberror
from datetime import datetime
from common.timeformat import format_for_db
from models.model import User, AgentMessage
sys.path.append(os.path.dirname(os.getcwd()))


class COrder():

    def __init__(self):
        self.suser = SUser()
        self.sorder = SOrder()
        self.sgoods = SGoods()
        self.smycenter = SMyCenter()
        self.smessage = SMessage()

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
        user_info = get_model_return_dict(self.smycenter.get_user_basicinfo(request.user.id))
        if not user_info:
            return SYSTEM_ERROR
        if user_info['USbail'] < BAIL:
            return NO_BAIL
        mount = 0
        new_list = []
        try:
            for product in product_list:
                num = product['PRnum']
                check_product = get_model_return_dict(self.sgoods.get_product(product['PRid']))
                mount = mount + num * check_product['PRprice']
                product['PRprice'] = check_product['PRprice']
                new_list.append(product)
            if totalprice != mount or real_PRlogisticsfee != PRlogisticsfee:
                response = {}
                response['status'] = 200
                response['success'] = False
                response['data'] = new_list
                response['PRlogisticsfee'] = real_PRlogisticsfee
                response['totalprice'] = mount
                return response
            if user_info['USmount'] < mount + PRlogisticsfee:
                return NO_ENOUGH_MOUNT
        except:
            return SYSTEM_ERROR
        session = db_session()
        try:
            OIid = str(uuid.uuid4())
            OIsn = datetime.strftime(datetime.now(), format_for_db) + str(random.randint(10000, 100000))
            OIcreatetime = datetime.strftime(datetime.now(), format_for_db)
            result = self.sorder.check_stock(new_list)
            if not result:
                raise dberror
            result = self.sorder.add_order(session, OIid, OIsn, request.user.id, OInote, mount, UAid, OIcreatetime, PRlogisticsfee)
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
            user = {}
            user['USmount'] = user_info['USmount'] - mount
            session.query(User).filter_by(USid=request.user.id).update(user)
            agentmessage = AgentMessage()
            agentmessage.AMid = str(uuid.uuid4())
            agentmessage.USid = request.user.id
            agentmessage.AMdate = OIcreatetime
            agentmessage.AMtype = 0
            agentmessage.AMcontent = u'您的订单创建成功，订单号为' + ' ' + str(OIsn)
            session.add(agentmessage)
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
        if not detail:
            response = import_status("get_orderdetails_success", "OK")
            response['data'] = []
            return response
        address = get_model_return_dict(self.smycenter.get_other_address(request.user.id, detail['UAid']))
        if not address:
            return NO_ADDRESS
        area = get_model_return_dict(self.smycenter.get_area_by_areaid(address['areaid']))
        from common.timeformat import get_web_time_str
        if area:
            city = get_model_return_dict(self.smycenter.get_city_by_cityid(area['cityid']))
            province = get_model_return_dict(self.smycenter.get_province_by_provinceid(city['provinceid']))
            detail['provincename'] = province['provincename']
            detail['cityname'] = city['cityname']
            detail['areaname'] = area['areaname']
            detail['details'] = address['UAdetails']
            detail['username'] = address['UAname']
            detail['userphonenum'] = address['UAphonenum']
            detail['createtime'] = get_web_time_str(address['UAcreatetime'])
        else:
            city = get_model_return_dict(self.smycenter.get_city_by_cityid(address['cityid']))
            province = get_model_return_dict(self.smycenter.get_province_by_provinceid(city['provinceid']))
            detail['provincename'] = province['provincename']
            detail['cityname'] = city['cityname']
            detail['details'] = address['UAdetails']
            detail['username'] = address['UAname']
            detail['userphonenum'] = address['UAphonenum']
            detail['createtime'] = get_web_time_str(address['UAcreatetime'])
        product_list = get_model_return_list(self.sorder.get_product_list(detail['OIid']))
        detail['product_list'] = product_list
        response = import_status("get_orderdetails_success", "OK")
        response['data'] = detail
        return response


