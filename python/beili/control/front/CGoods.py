# *- coding:utf8 *-
import re
import sys
import os
from flask import request
# import logging
from config.response import PARAMS_MISS
from config.setting import QRCODEHOSTNAME
from common.token_required import verify_token_decorator, usid_to_token, is_tourist, is_ordirnaryuser
from common.import_status import import_status
from common.timeformat import get_db_time_str
from common.get_model_return_list import get_model_return_list, get_model_return_dict
from service.front.SGoods import SGoods
import platform
sys.path.append(os.path.dirname(os.getcwd()))


class CGoods():

    def __init__(self):
        self.sgoods = SGoods()

    #@verify_token_decorator
    def get_product_list(self):
        #self.json_param_miss("get")
        args = request.args.to_dict()
        try:
            page_num = int(args.get("page_num"))
            page_size = int(args.get("page_size"))
            if "PRstatus" in args:
                PRstatus = args.get("PRstatus")
            else:
                PRstatus = None
            if "PAid" in args and "PAtype" in args:
                if args.get("PAtype") == 1:
                    paid_list = get_model_return_list(self.sgoods.get_childid(args.get("PAid")))
                    product_list = []
                    for row in paid_list:
                        product_list.extend(get_model_return_list(
                            self.sgoods.get_product_list(page_size, page_num, row, PRstatus)))
                elif args.get("PAtype") == 2:
                    product_list = get_model_return_list(
                        self.sgoods.get_product_list(page_size, page_num, args.get("PAid"), PRstatus))
                else:
                    return import_status("BEILI_ERROR", "patype_error", "patype_error")
            else:
                PAid = None
                product_list = get_model_return_list(
                    self.sgoods.get_product_list(page_size, page_num, PAid, PRstatus))
        except Exception as e:
            print(e.message)
            return PARAMS_MISS

        response = import_status("get_product_list_success", "OK")
        response["data"] = product_list
        return response

    @verify_token_decorator
    def get_product(self):
        self.json_param_miss("get")
        args = request.args.to_dict()
        try:
            PRid = args.get("PRid")
            product = get_model_return_dict(self.sgoods.get_product(PRid))
        except Exception as e:
            print(e.message)
            return PARAMS_MISS
        response = import_status("OK", "get_product_success")
        response["data"] = product
        return response

    #@verify_token_decorator
    def get_product_category(self):
        #self.json_param_miss("get")
        args = request.args.to_dict()
        normal_json = {
            "PAid": None,
            "PAname": "全部"
        }
        product_category = []
        product_category.extend(normal_json)
        try:
            PAtype = args.get("PAtype")
            if PAtype == 0:
                product_category.extend(get_model_return_list(self.sgoods.get_first_product_category(0)))
            elif PAtype == 1:
                PAid = args.get("PAid")
                product_category.extend(get_model_return_list(self.sgoods.get_first_product_category(PAid)))
            elif PAtype == 2:
                pass
            else:
                return
        except Exception as e:
            print(e.message)
            return PARAMS_MISS
        response = import_status("OK", "get_product_category_success")
        response["data"] = product_category
        return response

    @verify_token_decorator
    def new_product(self):
        self.json_param_miss("post")
        return

    @verify_token_decorator
    def update_product(self):
        self.json_param_miss("post")
        return

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
            return TOKEN_ERROR(u"未登录")
        if type == "get":
            pass
        elif type == "post":
            json_data = request.json
            if not json_data:
                return PARAMS_MISS
        else:
            pass