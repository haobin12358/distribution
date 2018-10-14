# *- coding:utf8 *-
import sys
import os
from flask import request
# import logging
import uuid
import datetime
import json
import urllib2
from config.response import PARAMS_MISS, SYSTEM_ERROR, PARAMS_ERROR, TOKEN_ERROR
from common.token_required import verify_token_decorator, usid_to_token
from common.import_status import import_status
from common.timeformat import format_for_db
from service.SUser import SUser
sys.path.append(os.path.dirname(os.getcwd()))


class CUser():

    def __init__(self):
        self.suser = SUser()

    def login(self):
        print "hello"
        json_data = request.json
        if not json_data:
            return PARAMS_MISS
        usphonenum = json_data.get('usphone')
        uspassword = json_data.get('uspassword')
        if not usphone or not uspassword:
            return PARAMS_MISS('请输入用户名或密码')
        user = self.suser.getpasswd_by_phonenum(usphonenum)
        print "aaaa" + user.USphone + ":" + user.USpassword
        if not user or uspassword != user.USpassword:
            return SYSTEM_ERROR('用户名或者密码错误')
        token = usid_to_token(user.USphone)
        data = import_status('generic_token_success', "OK")
        data['data'] = {
            'token': token,
        }
        return data

    def update_pwd(self):
        print "changepwd"
        json_data = request.json
        if not json_data:
            return PARAMS_MISS
        usphonenum = json_data.get('usphonenum')
        oldpassword = json_data.get('oldpassword')
        newpassword = json_data.get('newpassword')
        user = self.suser.getpasswd_by_phonenum(usphonenum)
        if not user or user.USpassword != oldpassword:
            return PARAMS_ERROR("旧密码错误")
        user = {}
        user["USpassword"] = newpassword
        self.suser.updatepwd_by_usphonenum(usphonenum)
        data = import_status("get_banner_success", "OK")
        return data