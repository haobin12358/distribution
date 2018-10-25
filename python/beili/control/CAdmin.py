# *- coding:utf8 *-
import re
import sys
import os
from flask import request
# import logging
from config.response import PARAMS_MISS, SYSTEM_ERROR, PARAMS_ERROR, PHONE_OR_PASSWORD_WRONG, \
    AUTHORITY_ERROR, PARAMS_MISS, NO_PHONENUM_OR_PASSWORD
from config.setting import QRCODEHOSTNAME
from common.token_required import verify_token_decorator, usid_to_token, is_admin, is_ordirnaryuser
from common.import_status import import_status
from common.get_model_return_list import get_model_return_list, get_model_return_dict
from common.timeformat import get_db_time_str
from service.SAdmin import SAdmin
import platform
sys.path.append(os.path.dirname(os.getcwd()))


class CAdmin():

    def __init__(self):
        self.sadmin = SAdmin()

    def login(self):
        try:
            json_data = request.json
            adnum = int(json_data.get('adnum'))
            adpassword = int(json_data.get('adpassword'))
        except:
            return PARAMS_MISS
        if not adnum or not adpassword:
            return NO_PHONENUM_OR_PASSWORD
        admin = get_model_return_dict(self.sadmin.getadmin_by_adnum(adnum))
        if not admin or adpassword != int(admin['ADpassword']):
            return PHONE_OR_PASSWORD_WRONG
        token = usid_to_token(admin['ADid'], type='SuperUser')
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
            return PARAMS_ERROR
        admin_update = {}
        admin_update["ADpassword"] = newpassword
        self.sadmin.update_amdin_by_adminid(user.ADid, admin_update)
        data = import_status("update_password_success", "OK")
        return data
