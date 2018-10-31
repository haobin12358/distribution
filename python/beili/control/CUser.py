# *- coding:utf8 *-
import sys
import os
import json
from flask import request
# import logging
from config.response import PARAMS_MISS, PHONE_OR_PASSWORD_WRONG, PARAMS_ERROR, TOKEN_ERROR, AUTHORITY_ERROR,\
    NOT_FOUND_IMAGE, PASSWORD_WRONG, NOT_FOUND_USER, INFORCODE_WRONG, SYSTEM_ERROR, NOT_FOUND_FILE
from config.setting import QRCODEHOSTNAME
from common.token_required import verify_token_decorator, usid_to_token, is_tourist, is_ordirnaryuser
from common.import_status import import_status
from common.get_model_return_list import get_model_return_list, get_model_return_dict
from common.timeformat import get_db_time_str
from service.SUser import SUser
from service.DBSession import db_session
from common.beili_error import stockerror, dberror
from service.SMyCenter import SMyCenter
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
        if not is_ordirnaryuser():
            return AUTHORITY_ERROR(u"权限不足")
        files = request.files.get("file")
        if not files:
            return NOT_FOUND_IMAGE(u"图片不存在")
        if platform.system() == "Windows":
            rootdir = "D:/task"
        else:
            rootdir = "/opt/beili/imgs/mycenter/"
        if not os.path.isdir(rootdir):
            os.mkdir(rootdir)
        lastpoint = str(files.filename).rindex(".")
        filessuffix = str(files.filename)[lastpoint+1:]
        filename = request.user.id + get_db_time_str() + "." + filessuffix
        filepath = os.path.join(rootdir, filename)
        print(filepath)
        files.save(filepath)
        response = import_status("updata_headimg_success", "OK")
        # url = Inforcode.ip + Inforcode.LinuxImgs + "/" + filename
        url = QRCODEHOSTNAME + "/imgs/mycenter/" + filename
        user_update = {}
        user_update['USheadimg'] = url
        self.suser.update_user_by_uid(request.user.id, user_update)
        # print(url)
        response["data"] = url
        return response

    @verify_token_decorator
    def upload_file(self):
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

    @verify_token_decorator
    def remove_file(self):
        try:
            data = request.json
            url = str(data.get('url'))
        except:
            return PARAMS_ERROR
        list = url.split('/file/')
        filename = list[0] + '/opt/beili/file/' + list[1]
        os.remove(filename)
        response = import_status("remove_file_success", "OK")
        return response


    @verify_token_decorator
    def make_qrcode(self):
        if is_tourist():
            return TOKEN_ERROR
        userinfo = self.smycenter.get_user_basicinfo(request.user.id)

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

