# *- coding:utf8 *-
import re
import sys
import os
import uuid
import random
from flask import request
# import logging
from config.response import PARAMS_MISS, SYSTEM_ERROR, PARAMS_ERROR, TOKEN_ERROR, AUTHORITY_ERROR
from config.setting import QRCODEHOSTNAME
from common.token_required import verify_token_decorator, usid_to_token, is_tourist, is_admin
from common.import_status import import_status
from common.timeformat import get_db_time_str
from common.get_model_return_list import get_model_return_list
from service.SUser import SUser
from service.SMessage import SMessage
from service.SOrder import SOrder
import platform
from datetime import datetime
from common.timeformat import format_for_db
sys.path.append(os.path.dirname(os.getcwd()))


class COrder():

    def __init__(self):
        self.suser = SUser()
        self.sorder = SOrder()

    @verify_token_decorator
    def create_order(self):
        if is_tourist():
            return TOKEN_ERROR
        data = request.json
        if not data:
            return PARAMS_MISS
        params_list = ["UAid", "product_list", "OInote", "OImount"]
        for params in params_list:
            if params not in data:
                return PARAMS_MISS
        product_list = []
        #try:
        UAid = data['UAid']
        OInote = data['OInote']
        OImount = data['OImount']
        for product in data['product_list']:
            product_list.append(product)
        #except:
        #return PARAMS_ERROR
        OIid = str(uuid.uuid4())
        OIsn = datetime.strftime(datetime.now(), format_for_db) + str(random.randint(10000, 100000))
        OIcreatetime = datetime.strftime(datetime.now(), format_for_db)
        for product in product_list:
            OPIid = str(uuid.uuid4())
            PRid = product['PRid']
            PRnum = product['PRnum']
            PRname = product['PRname']
            PRimage = product['PRimage']
            PRprice = product['PRprice']
            result = self.sorder.add_orderproductinfo(OPIid, OIid, PRid, PRname, PRprice, PRnum, PRimage)
            if not result:
                return SYSTEM_ERROR
        result = self.sorder.add_order(OIid, OIsn, request.user.id, OInote, OImount, UAid, OIcreatetime)
        if not result:
            return SYSTEM_ERROR
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

