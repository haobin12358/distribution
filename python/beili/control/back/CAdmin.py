# *- coding:utf8 *-
import re
import sys
import os
from flask import request
# import logging
from config.response import PARAMS_MISS, SYSTEM_ERROR, PARAMS_ERROR, TOKEN_ERROR, NOT_FOUND, AUTHORITY_ERROR
from config.setting import QRCODEHOSTNAME
from common.token_required import verify_token_decorator, usid_to_token, is_admin, is_ordirnaryuser
from common.import_status import import_status
from common.timeformat import get_db_time_str
from service.back.SAdmin import SAdmin
import platform
sys.path.append(os.path.dirname(os.getcwd()))


class CAdmin():

    def __init__(self):
        self.sadmin = SAdmin()

    def login(self):
        print "hello"
        json_data = request.json
        if not json_data:
            return PARAMS_MISS
        adnum = json_data.get('adnum')
        adpassword = json_data.get('adpassword')
        if not adnum or not adpassword:
            return PARAMS_MISS(u'请输入账号或密码')
        admin = self.sadmin.getadmin_by_adnum(adnum)
        # print "aaaa" + user.USphone + ":" + user.USpassword
        # print(dir(user))
        if not admin or adpassword != admin.ADpassword:
            return SYSTEM_ERROR(u'账号或者密码错误')
        token = usid_to_token(admin.ADid)
        data = import_status('generic_token_success', "OK")
        data['data'] = {
            'token': token,
        }
        return data

    @verify_token_decorator
    def update_pwd(self):
        if not is_admin():
            return AUTHORITY_ERROR
        json_data = request.json
        if not json_data:
            return PARAMS_MISS
        oldpassword = json_data.get('oldpassword')
        newpassword = json_data.get('newpassword')
        user = self.sadmin.getadmin_by_adminid(request.user.id)
        if not user or user.ADpassword != oldpassword:
            return PARAMS_ERROR(u"密码错误")
        admin_update = {}
        admin_update["ADpassword"] = newpassword
        self.sadmin.update_amdin_by_adminid(user.ADid, admin_update)
        data = import_status("update_password_success", "OK")
        return data
