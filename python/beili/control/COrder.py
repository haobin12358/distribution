# *- coding:utf8 *-
import re
import sys
import os
import uuid
import random
from flask import request
# import logging
from config.response import PARAMS_MISS, SYSTEM_ERROR, PARAMS_ERROR, TOKEN_ERROR, AUTHORITY_ERROR, STOCK_NOT_ENOUGH,\
        NO_ENOUGH_MOUNT, NO_BAIL, PRlogisticsfee_WRONG, TOTAL_PRICE_WRONG
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
sys.path.append(os.path.dirname(os.getcwd()))


class COrder():

    def __init__(self):
        self.suser = SUser()
        self.sorder = SOrder()
        self.sgoods = SGoods()
        self.smycenter = SMyCenter()

    @verify_token_decorator
    def create_order(self):
        sessions = db_session
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
            PRlogisticsfee = data['PRlogisticsfee']
            totalprice = data['totalprice']
        except:
            return PARAMS_ERROR
        if len(product_list) > 1:
            real_PRlogisticsfee = 0
        else:
            real_PRlogisticsfee = get_model_return_dict(self.sgoods.get_product(product_list[0]['PRid']))['PRlogisticsfee']
        if real_PRlogisticsfee != PRlogisticsfee:
            return PRlogisticsfee_WRONG
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
                price = get_model_return_dict(self.sgoods.get_product(product['PRid']))
                mount = mount + num * price['PRprice']
                product['PRprice'] = price['PRprice']
                new_list.append(product)
            if totalprice != totalprice:
                return TOTAL_PRICE_WRONG
            if user_info['USmount'] < mount + PRlogisticsfee:
                return NO_ENOUGH_MOUNT
        except:
            return SYSTEM_ERROR
        OIid = str(uuid.uuid4())
        OIsn = datetime.strftime(datetime.now(), format_for_db) + str(random.randint(10000, 100000))
        OIcreatetime = datetime.strftime(datetime.now(), format_for_db)
        try:
            result = self.sorder.check_stock(new_list)
            if not result:
                return SYSTEM_ERROR
        except stockerror as e:
            return STOCK_NOT_ENOUGH
        except Exception as e2:
            print e2.message
            return SYSTEM_ERROR
        result = self.sorder.add_order(OIid, OIsn, request.user.id, OInote, mount, UAid, OIcreatetime, PRlogisticsfee)
        if not result:
            raise dberror
        for product in new_list:
            OPIid = str(uuid.uuid4())
            PRid = product['PRid']
            PRnum = product['PRnum']
            PRname = product['PRname']
            PRimage = get_model_return_dict(self.sgoods.get_product(PRid))['PRimage']
            PRprice = product['PRprice']
            result = self.sorder.add_orderproductinfo(OPIid, OIid, PRid, PRname, PRprice, PRnum, PRimage)
            if not result:
                raise dberror
        response = import_status("create_order_success", "OK")
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
        except:
            return PARAMS_ERROR
        if type == 0:
            order_list = get_model_return_list(self.sorder.get_allorder_list(request.user.id))
        else:
            order_list = get_model_return_list(self.sorder.get_order_list(request.user.id, type))
        order_return_list = []
        for order in order_list:
            product_list = get_model_return_list(self.sorder.get_product_list(order['OIid']))
            order['product_list'] = product_list
            order_return_list.append(order)
        response = import_status("get_orderlist_success", "OK")
        response['data'] = order_return_list
        return response

