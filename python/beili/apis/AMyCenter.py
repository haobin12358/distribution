# -*- coding:utf8 -*-
import sys
import os
from flask import jsonify
from flask_restful import Resource
from control.CMyCenter import CMyCenter
sys.path.append(os.path.dirname(os.getcwd()))

class AMyCenter(Resource):
    def __init__(self):
        self.cmycenter = CMyCenter()

    def post(self, mycenter):
        print mycenter
        apis = {
            'check_inforcode': 'self.cmycenter.check_inforcode()',
            'update_headimg': 'self.cmycenter.update_headimg()',
            'add_useraddress': 'self.cmycenter.add_useraddress()',
            'get_useraddress': 'self.cmycenter.get_useraddress()',
            'delete_useraddress': 'self.cmycenter.delete_useraddress()',
            'update_useraddress': 'self.cmycenter.update_useraddress()',
            'change_default': 'self.cmycenter.change_default()',
            'add_comments':'self.cmycenter.add_comments()',
            'deal_comments': 'self.cmycenter.deal_comments()'
        }
        res = eval(apis[mycenter])
        return jsonify(res)

    def get(self, mycenter):
        print mycenter
        apis = {
            'get_inforcode': 'self.cmycenter.get_inforcode()',
            'get_province': 'self.cmycenter.get_province()',
            'get_city_by_province': 'self.cmycenter.get_city_by_province()',
            'get_area_by_city': 'self.cmycenter.get_area_by_city()',
            'get_all_area': 'self.cmycenter.get_all_area()',
            'get_user_basicinfo': 'self.cmycenter.get_user_basicinfo()',
            'get_user_totalinfo': 'self.cmycenter.get_user_totalinfo()',
            'get_comment_list': 'self.cmycenter.get_comment_list()'
        }
        res = eval(apis[mycenter])
        return jsonify(res)