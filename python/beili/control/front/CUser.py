# *- coding:utf8 *-
import re
import sys
import os
from flask import request
# import logging
from config.response import PARAMS_MISS, SYSTEM_ERROR, PARAMS_ERROR, TOKEN_ERROR, NOT_FOUND
from common.token_required import verify_token_decorator, usid_to_token, is_tourist
from common.import_status import import_status
from service.front.SUser import SUser
sys.path.append(os.path.dirname(os.getcwd()))


class CUser():

    def __init__(self):
        self.suser = SUser()

    def login(self):
        print "hello"
        json_data = request.json
        if not json_data:
            return PARAMS_MISS
        usphonenum = json_data.get('usphonenum')
        uspassword = json_data.get('uspassword')
        if not usphonenum or not uspassword:
            return PARAMS_MISS('请输入用户名或密码')
        print type(usphonenum)
        user = self.suser.getuser_by_phonenum(usphonenum)
        # print "aaaa" + user.USphone + ":" + user.USpassword
        print user.USphonenum
        print type(user.USphonenum)
        if not user or uspassword != user.USphonenum:
            return SYSTEM_ERROR('用户名或者密码错误')
        token = usid_to_token(user.USid)
        data = import_status('generic_token_success', "OK")
        data['data'] = {
            'token': token,
        }
        return data

    @verify_token_decorator
    def update_pwd(self):
        if is_tourist():
            return TOKEN_ERROR(u"未登录")
        json_data = request.json
        if not json_data:
            return PARAMS_MISS
        usphonenum = json_data.get('usphonenum')
        oldpassword = json_data.get('oldpassword')
        newpassword = json_data.get('newpassword')
        user = self.suser.getpasswd_by_phonenum(usphonenum)
        if not user or user.USpassword != oldpassword:
            return PARAMS_ERROR("用户名或者密码错误")
        user_update = {}
        user_update["USpassword"] = newpassword
        self.suser.update_user_by_uid(user.USid, user_update)
        data = import_status("update_password_success", "OK")
        return data

    def findback_pwd(self):
        try:
            json_data = request.json
            usphonenum = json_data.get('usphonenum')
            newpassword = json_data.get('newpassword')
        except Exception as e:
            return PARAMS_ERROR
        if not usphonenum or not newpassword:
            return PARAMS_MISS
        user = self.suser.getpasswd_by_phonenum(usphonenum)
        if not user:
            return NOT_FOUND('该号码未注册')
        user_update = {}
        user_update["USpassword"] = newpassword
        self.suser.update_user_by_uid(user.USid, user_update)
        data = import_status("update_password_success", "OK")
        return data