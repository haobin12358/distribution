# *- coding:utf8 *-
import re
import sys
import os
import uuid
from flask import request
# import logging
from config.response import PARAMS_MISS, SYSTEM_ERROR, PARAMS_ERROR, PHONE_OR_PASSWORD_WRONG, \
    AUTHORITY_ERROR, PARAMS_MISS, NO_PHONENUM_OR_PASSWORD, ADMINNUM_ERROR, ADMINNAME_ERROR, PASSWORD_WRONG
from config.setting import QRCODEHOSTNAME
from common.token_required import verify_token_decorator, is_superadmin, usid_to_token, is_admin, is_ordirnaryuser
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
            if admin['ADisfreeze'] == True:
                return PHONE_OR_PASSWORD_WRONG
        token = usid_to_token(admin['ADid'], type='SuperUser')
        data = import_status('generic_token_success', "OK")
        data['data'] = {
            'token': token,
        }
        return data

    # 更新密码
    @verify_token_decorator
    def update_pwd(self):
        if not is_admin():
            return AUTHORITY_ERROR
        json_data = request.json
        if not json_data:
            return PARAMS_MISS
        oldpassword = json_data.get('oldpassword')
        newpassword = json_data.get('newpassword')
        user = get_model_return_dict(self.sadmin.getadmin_by_adminid(request.user.id))
        if not user or user['ADpassword'] != oldpassword:
            return PASSWORD_WRONG
        admin_update = {}
        admin_update["ADpassword"] = newpassword
        result = self.sadmin.update_amdin_by_adminid(user['ADid'], admin_update)
        if not result:
            return SYSTEM_ERROR
        data = import_status("update_password_success", "OK")
        return data

    # 获得所有的管理员

    # 创建管理员
    @verify_token_decorator
    def register(self):
        if not is_superadmin():
            return AUTHORITY_ERROR
        try:
            data = request.json
            ADnum = data.get('ADnum')
            ADname = data.get('ADname')
            ADpassword = data.get('ADpassword')
            ADlevel = data.get('ADlevel')
        except:
            return PARAMS_ERROR
        try:
            all_adnum = get_model_return_list(self.sadmin.get_all_adnum())  # 查看是否有相同的管理员号码
            for adnum_dict in all_adnum:
                if ADnum == adnum_dict['ADnum']:
                    return 'sorry, this adnum is already exists'
            all_adname = get_model_return_list(self.sadmin.get_all_adname())  # 查看是否有相同的管理员名
            for adname_dict in all_adname:
                if ADname == adname_dict['ADname']:
                    return 'sorry, this adname is already exists'
            import datetime
            from common.timeformat import format_for_db
            time_time = datetime.datetime.now()
            time_str = datetime.datetime.strftime(time_time, format_for_db)
            adid = str(uuid.uuid1())
            self.sadmin.add_admin(adid, ADnum, ADname, ADpassword, ADlevel, time_str)
            response = import_status("get_admin_success", "OK")
            return response
        except:
            return SYSTEM_ERROR

    # 删除管理员
    @verify_token_decorator
    def delete_admin(self):
        if not is_superadmin():
            return AUTHORITY_ERROR
        try:
            data = request.json
            ADnum = data.get('ADnum')
            #ADname = data.get('ADname')
        except:
            return PARAMS_ERROR
        try:
            retnum = False  #判断ADnum是否在admin列表中
            retname = False  #判断ADname是否在admin列表中
            all_adnum = get_model_return_list(self.sadmin.get_all_adnum())
            #all_adname = get_model_return_list(self.sadmin.get_all_adname())
            for adnum_dict in all_adnum:
                if ADnum == int(adnum_dict['ADnum']):
                    retnum = True
            # if retnum == False:
            #     return ADMINNUM_ERROR
            # for adname_dict in all_adname:
            #     if ADname == adname_dict['ADname']:
            #         retcode = True
            #     else:
            #         return ADMINNAME_ERROR
            #if retnum and retname:
            if retnum:
                update_admin = {}
                update_admin['ADisfreeze'] = True
                self.sadmin.delete_admin(ADnum, update_admin)
                response = import_status("delete_admin_success", "OK")
                return response
            else:
                return ADMINNUM_ERROR
        except Exception as e:
            print e
            return SYSTEM_ERROR


    # 更新管理员个人信息
    @verify_token_decorator
    def update_admin(self):
        if not is_superadmin():
            return AUTHORITY_ERROR
        try:
            data = request.json
            ADnum = data.get('ADnum')
            ADname = data.get('ADname')
            ADpassword = data.get('ADpassword')
            ADlevel = data.get('ADlevel')
        except:
            return PARAMS_ERROR
        try:
            retnum = False  #判断ADnum是否在admin列表中
            all_adnum = get_model_return_list(self.sadmin.get_all_adnum())
            for adnum_dict in all_adnum:
                if ADnum == int(adnum_dict['ADnum']):
                    retnum = True
            if retnum == False:
                return ADMINNUM_ERROR
            update = {}
            update['ADname'] = ADname
            update['ADpassword'] = ADpassword
            update['ADlevel'] = ADlevel
            self.sadmin.update_admin(ADnum, update)
            response = import_status("update_admin", "OK")
            return response
        except Exception as e:
            print e
            return SYSTEM_ERROR










