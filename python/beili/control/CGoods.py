# *- coding:utf8 *-
import re
import sys
import os
import uuid
from datetime import datetime
from common.timeformat import format_for_db, get_random_str
from flask import request
# import logging
from config.response import PARAMS_MISS, NO_THIS_CATEGORY, PARAMS_ERROR, AUTHORITY_ERROR, SYSTEM_ERROR
from config.setting import QRCODEHOSTNAME
from common.token_required import verify_token_decorator, usid_to_token, is_tourist, is_admin
from common.import_status import import_status
from common.timeformat import get_db_time_str
from common.get_model_return_list import get_model_return_list, get_model_return_dict
from service.SGoods import SGoods
from common.timeformat import get_web_time_str
import platform
sys.path.append(os.path.dirname(os.getcwd()))


class CGoods():

    def __init__(self):
        self.sgoods = SGoods()

    #@verify_token_decorator
    def get_product_list(self):
        args = request.args.to_dict()
        try:
            page_num = int(args.get("page_num"))
            page_size = int(args.get("page_size"))
            PRstatus = int(args.get("PRstatus"))
            PRname = args.get("PRname")
            PAid = str(args.get("PAid"))
            PAtype = int(args.get("PAtype"))
        except:
            return PARAMS_MISS
        product_list = []
        if PAid == '':
            return PARAMS_ERROR
        if int(PAid) == 0:
            product_list = get_model_return_list(self.sgoods.admin_get_product(PRstatus, PRname))
        elif int(PAtype) == 1:
            paid_list = get_model_return_list(self.sgoods.get_childid(str(PAid)))
            for paid in paid_list:
                product_list = product_list + get_model_return_list(
                    self.sgoods.admin_get_product(PRstatus, PRname, paid['PAid']))
        elif int(PAtype) == 2:
                product_list = product_list + get_model_return_list(
                    self.sgoods.admin_get_product(PRstatus, PRname, PAid))
        for product in product_list:
            categoryname = get_model_return_dict(self.sgoods.get_category_byid(product['PAid']))['PAname']
            product['categoryname'] = categoryname
            product['PRcreatetime'] = get_web_time_str(product['PRcreatetime'])

        mount = len(product_list)
        page = mount / page_size
        if page == 0 or page == 1 and mount % page_num == 0:
            return_list = product_list[0:]
        else:
            if ((mount - (page_num - 1) * page_size) / page_size) >= 1 and \
                    ((mount - (page_num - 1) * page_size) % page_size) > 0:
                return_list = product_list[((page_num - 1) * page_size):(page_num * page_size)]
            else:
                return_list = product_list[((page_num - 1) * page_size):]
        response = import_status("get_product_list_success", "OK")
        response["data"] = return_list
        response['mount'] = mount
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

    #@verify_token_decorator
    def get_product_category(self):
        args = request.args.to_dict()
        try:
            PAtype = int(args.get("PAtype"))
            if PAtype == 1:
                product_category = (get_model_return_list(self.sgoods.get_first_product_category(0)))
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
        params = ['paid', 'prname', 'prpic', 'proldprice', 'prprice', 'prstock', 'prlogisticsfee', 'prdiscountnum', 'prstatus']
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
        prstock = data.get('prstock')
        prlogisticsfee = data.get('prlogisticsfee')
        prdiscountnum = data.get('prdiscountnum')
        prstatus = data.get('prstatus')
        prid = data.get('prid')
        if prid:
            product = {}
            product['PAid'] = paid
            product['PRname'] = prname
            product['PRpic'] = prpic
            product['PRoldprice'] = proldprice
            product['PRprice'] = prprice
            product['PRstock'] = prstock
            product['PRlogisticsfee'] = prlogisticsfee
            product['PRstatus'] = prstatus
            product['PAdiscountnum'] = prdiscountnum
            result = self.sgoods.update_product(prid, product)
            if not result:
                return SYSTEM_ERROR
            response = import_status("update_product_success", "OK")
            return response
        else:
            time_now = datetime.strftime(datetime.now(), format_for_db)
            result = self.sgoods.create_product(str(uuid.uuid4()), paid, prname, prpic, proldprice, prprice, prstock
                                       , prlogisticsfee, prstatus, prdiscountnum, time_now)
            if not result:
                return SYSTEM_ERROR
            response = import_status("create_product_success", "OK")
            return response

    @verify_token_decorator
    def new_category(self):
        self.json_param_miss("post")
        return

    @verify_token_decorator
    def update_category(self):
        self.json_param_miss("post")
        return

    @verify_token_decorator
    def delete_category(self):
        self.json_param_miss("post")
        return

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