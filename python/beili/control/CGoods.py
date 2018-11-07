# *- coding:utf8 *-
import re
import sys
import os
from flask import request
import copy
# import logging
from config.response import PARAMS_MISS, NO_THIS_CATEGORY, PARAMS_ERROR, PRODUCE_CATEGORY_EXIST, PRODUCE_CATEGORY_NOT_EXIST
from config.setting import QRCODEHOSTNAME
from common.token_required import verify_token_decorator, usid_to_token, is_tourist, is_ordirnaryuser,is_superadmin, is_admin
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
        #self.json_param_miss("get")
        args = request.args.to_dict()
        try:
            page_num = int(args.get("page_num"))
            page_size = int(args.get("page_size"))
            PRstatus = int(args.get("PRstatus"))
            PAid = args.get("PAid")
            PAtype = int(args.get("PAtype"))
        except:
            return PARAMS_MISS
        if int(PAid) == 0:
            return_list, mount = self.sgoods.get_product_list(page_size, page_num, None, PRstatus)
            return_list = get_model_return_list(return_list)
        elif PAtype == 1:
            paid_list = get_model_return_list(self.sgoods.get_childid(int(args.get("PAid"))))
            product_list = []
            for row in paid_list:
                product_list = product_list + (get_model_return_list(self.sgoods.get_type1_product(row['PAid'], PRstatus)))
            mount = len(product_list)
            page = mount/page_size
            if page == 0 or page == 1 and mount%page_num == 0:
                return_list = product_list[0:]
            else:
                if ((mount - (page_num - 1) * page_size)/page_size) >= 1 and \
                        ((mount - (page_num - 1) * page_size)%page_size) > 0:
                    return_list = product_list[((page_num - 1) * page_size):(page_num * page_size)]
                else:
                    return_list = product_list[((page_num - 1) * page_size):]

        elif PAtype == 2:
            return_list, mount = self.sgoods.get_product_list(page_size, page_num, PAid, PRstatus)
            return_list = get_model_return_list(return_list)
        else:
            return PARAMS_MISS
        for product in return_list:
            product['PRcreatetime'] = get_web_time_str(product['PRcreatetime'])
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

    def get_product_category_list(self):
        #商品分类列表
        try:
            first_level = get_model_return_list(self.sgoods.get_first_product_category_status(0))
            print first_level
            options = []
            product_category_list = {}
            for parent_category in first_level:
                parnetid = parent_category['PAid']
                parentname = parent_category['PAname']
                pastatus = parent_category['PAstatus']
                if pastatus == False:
                    continue
                product_category_list['PAid'] = parnetid
                product_category_list['Parentname'] = parentname
                child_category = get_model_return_list(self.sgoods.get_first_product_category(parnetid))
                product_category_list['child_category'] = child_category
                test = product_category_list.copy()
                options.append(test)
            print options
            response = import_status("get_product_category_list_success", "OK")
            response['data'] = options
            #response['child_data'] = product_category_list
        except Exception as e:
            print(e.message)
            return PARAMS_MISS
        return response
    @verify_token_decorator
    def add_product_category(self):
        #添加商品分类
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
            get_PAstatus = get_model_return_list(self.sgoods.get_product_category(PAid))
            if get_PAstatus:
                return PRODUCE_CATEGORY_EXIST
            # elif get_Parentid == 0:
            #     self.sgoods.add_product_category(PAid, PAname, PAtype)
            else:
                self.sgoods.add_product_category(PAid, PAname, PAtype, Parentid)

        except Exception as e :
            print Exception
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
            get_PAstatus = get_model_return_list(self.sgoods.get_product_category(PAid))
            if not get_PAstatus:
                return PRODUCE_CATEGORY_NOT_EXIST
            # elif get_Parentid == 0:
            #     self.sgoods.add_product_category(PAid, PAname, PAtype)
            else:
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
        #response["data"] = product_category
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
            get_PAstatus = get_model_return_list(self.sgoods.get_product_category(PAid))
            if not get_PAstatus:
                return PRODUCE_CATEGORY_NOT_EXIST
            # elif get_Parentid == 0:
            #     self.sgoods.add_product_category(PAid, PAname, PAtype)
            else:
                delete_category = {}
                delete_category['PAstatus'] = False
                self.sgoods.delete_category(PAid, delete_category)

        except Exception as e :
            print Exception
            return PARAMS_MISS
        response = import_status("delete_product_category_success", "OK")
        #response["data"] = product_category
        return response



    #@verify_token_decorator
    def get_product_category(self):
        #self.json_param_miss("get")
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


