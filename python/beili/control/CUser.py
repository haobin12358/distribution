# *- coding:utf8 *-
import sys
import os
import json
import uuid
from flask import request
# import logging
from config.response import PARAMS_MISS, PHONE_OR_PASSWORD_WRONG, PARAMS_ERROR, TOKEN_ERROR, AUTHORITY_ERROR,\
    NOT_FOUND_IMAGE, PASSWORD_WRONG, NOT_FOUND_USER, INFORCODE_WRONG, SYSTEM_ERROR, NOT_FOUND_FILE, DELETE_CODE_FAIL, \
    NOT_FOUND_QRCODE
from config.setting import QRCODEHOSTNAME
from common.token_required import verify_token_decorator, usid_to_token, is_tourist, is_ordirnaryuser, is_temp
from common.import_status import import_status
from common.get_model_return_list import get_model_return_list, get_model_return_dict
from common.timeformat import get_db_time_str
from service.SUser import SUser
from service.DBSession import db_session
from common.beili_error import stockerror, dberror
from service.SMyCenter import SMyCenter
from datetime import datetime
from common.timeformat import format_for_db
import platform
sys.path.append(os.path.dirname(os.getcwd()))


class CUser():

    def __init__(self):
        self.suser = SUser()
        self.smycenter = SMyCenter()

    def login(self):
        print "hello"
        json_data = request.json
        if not json_data:
            return PARAMS_ERROR
        usphonenum = json_data.get('usphonenum')
        uspassword = json_data.get('uspassword')
        if not usphonenum or not uspassword:
            return PARAMS_MISS(u'请输入手机号或密码')
        print type(usphonenum)
        user = get_model_return_dict(self.suser.getuser_by_phonenum(usphonenum))
        # print "aaaa" + user.USphone + ":" + user.USpassword
        # print(dir(user))
        # print user.USphonenum
        # print type(user.USphonenum)
        if not user or uspassword != user['USpassword']:
            return PHONE_OR_PASSWORD_WRONG
        token = usid_to_token(user['USid'])
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
        oldpassword = json_data.get('oldpassword')
        newpassword = json_data.get('newpassword')
        user = get_model_return_list(self.suser.getuser_by_uid(request.user.id))
        if not user or user[0]['USpassword'] != oldpassword:
            return PASSWORD_WRONG
        user_update = {}
        user_update["USpassword"] = newpassword
        self.suser.update_user_by_uid(request.user.id, user_update)
        data = import_status("update_password_success", "OK")
        return data

    def findback_pwd(self):
        try:
            data = request.json
            phonenum = data.get('usphonenum')
            iccode = data.get('iccode')
            newpassword = data.get('newpassword')
        except Exception as e:
            return PARAMS_ERROR
        if not phonenum or not iccode or not newpassword:
            return PARAMS_ERROR
        codeinfo = get_model_return_dict(self.smycenter.get_inforcode_by_usphonenum(phonenum))
        if not codeinfo:
            return SYSTEM_ERROR
        if iccode != codeinfo['ICcode']:
            return INFORCODE_WRONG
        user = get_model_return_dict(self.suser.getuser_by_phonenum(phonenum))
        if not user:
            return NOT_FOUND_USER
        user_update = {}
        user_update["USpassword"] = newpassword
        self.suser.update_user_by_uid(user['USid'], user_update)
        data = import_status("update_password_success", "OK")
        return data

    @verify_token_decorator
    def update_headimg(self):  # 更新头像
        if is_tourist():
            return TOKEN_ERROR
        try:
            data = request.json
            url = data.get('url')
        except:
            return PARAMS_ERROR
        user_update = {}
        user_update['USheadimg'] = url
        result = self.suser.update_user_by_uid(request.user.id, user_update)
        if result:
            response = import_status("updata_headimg_success", "OK")
            return response
        else:
            return SYSTEM_ERROR

    @verify_token_decorator
    def upload_file(self):
        if is_ordirnaryuser():
            try:
                files = request.files.get("file")
            except:
                return PARAMS_ERROR
            if not files:
                return NOT_FOUND_FILE
            if platform.system() == "Windows":
                rootdir = "D:/task"
            else:
                rootdir = "/opt/beili/file/"
            if not os.path.isdir(rootdir):
                os.makedirs(rootdir)
            lastpoint = str(files.filename).rindex(".")
            filessuffix = str(files.filename)[lastpoint + 1:]
            filename = request.user.id + get_db_time_str() + "." + filessuffix
            filepath = os.path.join(rootdir, filename)
            print(filepath)
            files.save(filepath)
            response = import_status("upload_file_success", "OK")
            url = QRCODEHOSTNAME + "/file/" + filename
            response["data"] = url
            return response
        else:
            id1 = str(uuid.uuid4())
            token = usid_to_token(id=id1, type='Temp')
            try:
                files = request.files.get("file")
            except:
                return PARAMS_ERROR
            if not files:
                return NOT_FOUND_FILE
            if platform.system() == "Windows":
                rootdir = "D:/task"
            else:
                rootdir = "/opt/beili/file/"
            if not os.path.isdir(rootdir):
                os.makedirs(rootdir)
            lastpoint = str(files.filename).rindex(".")
            filessuffix = str(files.filename)[lastpoint + 1:]  # 后缀名
            filename = id1 + get_db_time_str() + "." + filessuffix
            filepath = os.path.join(rootdir, filename)
            print(filepath)
            files.save(filepath)
            url = QRCODEHOSTNAME + "/file/" + filename
            data = import_status("upload_file_success", "OK")
            data['data'] = {
                'token': token,
                'url': url
            }
            return data



    @verify_token_decorator
    def remove_file(self):
        if is_ordirnaryuser():
            try:
                data = request.json
                url = str(data.get('url'))
            except:
                return PARAMS_ERROR
            real_url = QRCODEHOSTNAME + "/opt/beili/file/" + url
            if request.user.id not in real_url:
                return AUTHORITY_ERROR
            try:
                os.remove(real_url)
                response = import_status("remove_file_success", "OK")
                return response
            except:
                return AUTHORITY_ERROR
        elif is_temp():
            try:
                data = request.json
                url = str(data.get('url'))
            except:
                return PARAMS_ERROR
            real_url = QRCODEHOSTNAME + "/opt/beili/file/" + url
            if request.temp not in real_url:
                return AUTHORITY_ERROR
            try:
                os.remove(real_url)
                response = import_status("remove_file_success", "OK")
                return response
            except:
                return AUTHORITY_ERROR
        else:
            return TOKEN_ERROR

    @verify_token_decorator
    def check_qrcode(self):
        if is_tourist():
            return TOKEN_ERROR
        try:
            data = request.json
            id = str(data.get('qrcodeid'))
        except:
            return PARAMS_ERROR
        result = self.suser.get_arcode_details(request.user.id, id)
        if not result:
            return NOT_FOUND_QRCODE
        else:
            result = get_model_return_dict(result)
            response = {}
            date = result['QRovertime']
            number = result['QRnumber']
            timenow = datetime.strftime(datetime.now(), format_for_db)
            if date < timenow:
                response['message'] = u"二维码已过期"
                response['success'] = False
                return response
            if number < 1:
                response['message'] = u"二维码次数已用完"
                response['success'] = False
                return response
            response['status'] = 200
            response['data'] = result
            response['success'] = True
            return response



    @verify_token_decorator
    def add_qrcode(self):
        if is_tourist():
            return TOKEN_ERROR
        try:
            data = request.json
            date = str(data.get('overtime'))
            number = int(data.get('number'))
        except:
            return PARAMS_ERROR
        result = self.suser.add_qrcode(str(uuid.uuid4()), request.user.id, date, number)
        if result:
            response = import_status("add_qrcode_success", "OK")
            return response
        else:
            return SYSTEM_ERROR

    @verify_token_decorator
    def get_qrcode(self):
        if is_tourist():
            return TOKEN_ERROR
        try:
            data = request.json
        except:
            return PARAMS_ERROR
        time = datetime.strftime(datetime.now(), format_for_db)
        from common.timeformat import get_web_time_str
        qrcode_list = self.suser.get_qrcode_list(request.user.id)
        if qrcode_list:
            return_list = []
            qrcode_list = get_model_return_list(qrcode_list)
            for code in qrcode_list:
                if str(code['QRovertime']) > time:
                    code['QRovertime'] = get_web_time_str(code['QRovertime'])
                    return_list.append(code)
            response = import_status("get_qrcode_success", "OK")
            response['data'] = return_list
            return response
        else:
            response = import_status("get_qrcode_success", "OK")
            response['data'] = []
            return response

    @verify_token_decorator
    def delete_qrcode(self):
        if is_tourist():
            return TOKEN_ERROR
        try:
            data = request.json
            qrcodeid = str(data.get('qrcodeid'))
        except:
            return PARAMS_ERROR
        if not qrcodeid:
            return PARAMS_ERROR
        result = self.suser.delete_qrcode(request.user.id, qrcodeid)
        if request:
            response = import_status("delete_qrcode_success", "OK")
            return response
        else:
            return DELETE_CODE_FAIL

    @verify_token_decorator
    def register(self):
        params = ['preid', 'preusername', 'prephonenum', 'predetails', 'username', 'phonenum', 'inforcode', 'password',
                  'idcardnum', 'wechat', 'cityid', 'areaid', 'details', 'paytype', 'payamount', 'paytime',
                  'headimg', 'proof', 'alipaynum', 'bankname', 'accountname', 'cardnum']
        data = request.json
        for param in data:
            if param not in params:
                return PARAMS_MISS
        try:
            preid = data['preid']
            preusername = data['preusername']
            prephonenum = data['prephonenum']
            predetails = data['predetails']
            username = data['username']
            phonenum = data['phonenum']
            inforcode = data['inforcode']
            password = data['password']
            idcardnum = data['idcardnum']
            wechat = data['wechat']
            cityid = data['cityid']
            areaid = data['areaid']
            details = data['details']
            paytype = data['paytype']
            payamount = data['payamount']
            paytime = data['paytime']
            headimg = data['headimg']
            alipaynum = data['alipaynum']
            bankname = data['bankname']
            accountname = data['accountname']
            cardnum = data['cardnum']
            if int(paytype) == 1:
                if not alipaynum or bankname or accountname or cardnum:
                    return PARAMS_ERROR
            if int(paytype) == 2:
                if alipaynum or not bankname or not accountname or not cardnum:
                    return PARAMS_ERROR
        except:
            return PARAMS_ERROR
        session = db_session()
        try:
            result = self.suser.insertInvitate(session, data)
            if not result:
                raise dberror
            session.commit()
        except Exception as e:
            print e
            session.rollback()
            return SYSTEM_ERROR
        finally:
            session.close()
        response = import_status("register_success", "OK")
        return response

