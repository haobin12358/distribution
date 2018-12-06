# *- coding:utf8 *-
import sys
import os
import json
import uuid
reload(sys)
sys.setdefaultencoding("utf8")
import flask
from flask import request
# import logging
from config.response import PARAMS_MISS, PHONE_OR_PASSWORD_WRONG, PARAMS_ERROR, TOKEN_ERROR, AUTHORITY_ERROR,\
    NOT_FOUND_IMAGE, PASSWORD_WRONG, NOT_FOUND_USER, INFORCODE_WRONG, SYSTEM_ERROR, NOT_FOUND_FILE, DELETE_CODE_FAIL, \
    NOT_FOUND_QRCODE, HAS_REGISTER, NO_BAIL, BAD_ADDRESS
from config.setting import QRCODEHOSTNAME, APP_ID, APP_SECRET, SERVER
from common.token_required import verify_token_decorator, usid_to_token, is_tourist, is_ordirnaryuser, is_temp, is_admin
from common.import_status import import_status
from common.get_model_return_list import get_model_return_list, get_model_return_dict
from common.timeformat import get_db_time_str, get_random_str
from service.SUser import SUser
from service.DBSession import db_session
from service.SAccount import SAccount
from common.beili_error import stockerror, dberror
from service.SMyCenter import SMyCenter
from service.SMessage import SMessage
from datetime import datetime
from config.urlconfig import get_code
import random
from models.model import Amount, User, Reward
from configparser import ConfigParser
from common.timeformat import format_for_db
import platform
import zlib
from werkzeug.security import generate_password_hash, check_password_hash
from weixin import WeixinError
from PIL import Image
from weixin.login import WeixinLoginError, WeixinLogin
sys.path.append(os.path.dirname(os.getcwd()))


class CUser():

    def __init__(self):
        self.suser = SUser()
        self.smycenter = SMyCenter()
        self.saccount = SAccount()
        self.smessage = SMessage()
        self.conf = ConfigParser()
        self.conf.read('config/setting.ini')

    def login(self):
        print "hello"
        json_data = request.json
        if not json_data:
            return PARAMS_ERROR
        usphonenum = json_data.get('usphonenum')
        uspassword = str(json_data.get('uspassword'))
        if not usphonenum or not uspassword:
            return PARAMS_MISS
        print type(usphonenum)

        user = get_model_return_dict(self.suser.getuser_by_phonenum(usphonenum))
        if user:
            if not check_password_hash(user['USpassword'], uspassword):
                return PHONE_OR_PASSWORD_WRONG
        # 从注册申请表里查询信息
        else:
            info = get_model_return_dict(self.suser.get_registerrecord_by_phonenum(usphonenum))
            if info:
                if int(info['IRIstatus']) == 1:
                    returnbody = {
                        "status": 405,
                        "status_code": 405006,
                        "message": u"您的账户正在审核中，请稍后再试!"
                    }
                    return returnbody
                if int(info['IRIstatus']) == 3:
                    returnbody = {
                        "status": 405,
                        "status_code": 405006,
                        "message": u"您的账户未审核通过，请联系客服微信:" + self.conf.get('account', 'service')
                    }
                    return returnbody
            else:
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
            return TOKEN_ERROR
        json_data = request.json
        if not json_data:
            return PARAMS_MISS
        oldpassword = json_data.get('oldpassword')
        newpassword = json_data.get('newpassword')
        user = get_model_return_list(self.suser.getuser_by_uid(request.user.id))
        if not user or not check_password_hash(user[0]['USpassword'], oldpassword):
            return PASSWORD_WRONG
        user_update = {}
        user_update["USpassword"] = generate_password_hash(newpassword)
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
        user_update["USpassword"] = generate_password_hash(newpassword)
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
        if is_ordirnaryuser() or is_admin():
            try:
                param = request.args.to_dict()
                type = param.get("type")
            except:
                type = None
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
            print 'filessuffix', filessuffix
            if is_ordirnaryuser():
                if filessuffix.lower() in ['png', 'jpg', 'jpeg', 'gif']:
                    image = Image.open(files)
                    w, h = image.size
                    filename = request.user.id + get_db_time_str() + get_random_str(6) + "." + filessuffix
                    filepath = os.path.join(rootdir, filename)
                    if type == 1:
                        image.resize((128, 128)).save(filepath)
                    image.resize((w / 2, h / 2)).save(filepath)
                    response = import_status("upload_file_success", "OK")
                    url = QRCODEHOSTNAME + "/file/" + filename
                    response["data"] = url
                    return response
            if is_admin():
                if filessuffix.lower() in ['png', 'jpg', 'jpeg', 'gif']:
                    image = Image.open(files)
                    w, h = image.size
                    filename = request.user.id + get_db_time_str() + get_random_str(6) + "." + filessuffix
                    filepath = os.path.join(rootdir, filename)
                    image.resize((w / 2, h / 2)).save(filepath)
                    response = import_status("upload_file_success", "OK")
                    url = QRCODEHOSTNAME + "/file/" + filename
                    response["data"] = url
                    return response
            filename = request.user.id + get_db_time_str() + get_random_str(6) + "." + filessuffix
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
            print filessuffix
            if filessuffix.lower() in ['png', 'jpg', 'jpeg', 'gif']:
                image = Image.open(files)
                w, h = image.size
                filename = id1 + get_db_time_str() + "." + filessuffix
                filepath = os.path.join(rootdir, filename)
                image.resize((w / 2, h / 2)).save(filepath)
                url = QRCODEHOSTNAME + "/file/" + filename
                data = import_status("upload_file_success", "OK")
                data['data'] = {
                    'token': token,
                    'url': url
                }
                return data
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
        if is_ordirnaryuser() or is_admin():
            try:
                data = request.json
                url = str(data.get('url'))
            except:
                return PARAMS_ERROR
            real_url = "/opt/beili/file/" + url
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
            real_url = "/opt/beili/file/" + url
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
        try:
            data = request.json
            id = str(data.get('qrid'))
        except:
            return PARAMS_ERROR
        result = get_model_return_dict(self.suser.get_arcode_details(id)) if self.suser.get_arcode_details(id) else None
        if not result:
            return NOT_FOUND_QRCODE
        user_info = get_model_return_dict(self.smycenter.get_user_basicinfo(result['USid'])) if self.smycenter \
            .get_user_basicinfo(result['USid']) else None
        if not user_info:
            return NOT_FOUND_USER
        if user_info['USbail'] < float(self.conf.get('account', 'bail')):
            return NO_BAIL
        else:
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
            from common.timeformat import get_web_time_str
            result['QRovertime'] = get_web_time_str(result['QRovertime'])
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
        user_info = get_model_return_dict(self.smycenter.get_user_basicinfo(request.user.id)) if self.smycenter\
                .get_user_basicinfo(request.user.id) else None
        if not user_info:
            return NOT_FOUND_USER
        if user_info['USbail'] < float(self.conf.get('account', 'bail')):
            return NO_BAIL
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
                if str(code['QRovertime']) > time and int(code['QRnumber']) > 0:
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

    def get_registerinfo(self):
        try:
            data = request.json
            qrcodeid = str(data.get('qrid'))
        except:
            return PARAMS_ERROR

        if not qrcodeid:
            user_dict = {}
            user_dict['alipaynum'] = self.conf.get('account', 'alipaynum')
            user_dict['alipayname'] = self.conf.get('account', 'alipayname')
            user_dict['bankname'] = self.conf.get('account', 'bankname')
            user_dict['accountname'] = self.conf.get('account', 'accountname')
            user_dict['cardnum'] = self.conf.get('account', 'cardnum')
            user_dict['money'] = float(self.conf.get('account', 'money'))
            user_dict['service'] = self.conf.get('account', 'service')
            user_dict['drawbank'] = self.conf.get('account', 'drawbank')
            response = import_status("get_registerinfo_success", "OK")
            response['data'] = user_dict
            return response
        usid = self.suser.get_user_by_qrid(qrcodeid)
        if not usid:
            return NOT_FOUND_QRCODE
        usid = get_model_return_dict(usid)
        user = self.suser.getuserinfo_by_uid(usid['USid'])
        if not user:
            return NOT_FOUND_USER
        user = get_model_return_dict(user)
        user_dict = {}
        user_dict['name'] = user['USname']
        user_dict['USphonenum'] = user['USphonenum']
        user_dict['alipaynum'] = self.conf.get('account', 'alipaynum')
        user_dict['alipayname'] = self.conf.get('account', 'alipayname')
        user_dict['bankname'] = self.conf.get('account', 'bankname')
        user_dict['accountname'] = self.conf.get('account', 'accountname')
        user_dict['cardnum'] = self.conf.get('account', 'cardnum')
        user_dict['money'] = float(self.conf.get('account', 'money'))
        user_dict['service'] = self.conf.get('account', 'service')
        user_dict['drawbank'] = self.conf.get('account', 'drawbank')
        address = self.smycenter.get_user_default_details(usid['USid'])
        if address:
            address = get_model_return_dict(address)
            area = get_model_return_dict(self.smycenter.get_area_by_areaid(address['areaid']))
            if area:
                city = get_model_return_dict(self.smycenter.get_city_by_cityid(area['cityid']))
                province = get_model_return_dict(self.smycenter.get_province_by_provinceid(city['provinceid']))
                provincename = province['provincename']
                cityname = city['cityname']
                areaname = area['areaname']
                details = address['UAdetails']
                real_address = provincename + cityname + areaname + details
                user_dict['address'] = real_address
                response = import_status("get_registerinfo_success", "OK")
                response['data'] = user_dict
                return response
            else:
                city = get_model_return_dict(self.smycenter.get_city_by_cityid(address['cityid']))
                province = get_model_return_dict(self.smycenter.get_province_by_provinceid(city['provinceid']))
                data = {}
                provincename = province['provincename']
                cityname = city['cityname']
                details = address['UAdetails']
                real_address = provincename + cityname + details
                user_dict['address'] = real_address
                response = import_status("get_registerinfo_success", "OK")
                response['data'] = user_dict
                return response
        else:
            address = self.smycenter.get_user_otherdefault_details(usid['USid'])
            if address:
                address = get_model_return_dict(address)
                area = get_model_return_dict(self.smycenter.get_area_by_areaid(address['areaid']))
                if area:
                    city = get_model_return_dict(self.smycenter.get_city_by_cityid(area['cityid']))
                    province = get_model_return_dict(self.smycenter.get_province_by_provinceid(city['provinceid']))
                    provincename = province['provincename']
                    cityname = city['cityname']
                    areaname = area['areaname']
                    details = address['UAdetails']
                    real_address = provincename + cityname + areaname + details
                    response = import_status("get_registerinfo_success", "OK")
                    response['data'] = user_dict
                    return response
                else:
                    city = get_model_return_dict(self.smycenter.get_city_by_cityid(address['cityid']))
                    province = get_model_return_dict(self.smycenter.get_province_by_provinceid(city['provinceid']))
                    data = {}
                    provincename = province['provincename']
                    cityname = city['cityname']
                    details = address['UAdetails']
                    real_address = provincename + cityname + details
                    user_dict['address'] = real_address
                    response = import_status("get_registerinfo_success", "OK")
                    response['data'] = user_dict
                    return response
        return SYSTEM_ERROR

    @verify_token_decorator
    def register(self):
        params = ['qrid','preusername', 'prephonenum','username', 'phonenum', 'inforcode', 'password',
                  'idcardnum', 'wechat', 'cityid', 'areaid', 'details', 'paytype', 'payamount', 'paytime',
                  'headimg', 'proof', 'alipaynum', 'bankname', 'accountname', 'cardnum']
        data = request.json
        for param in data:
            if param not in params:
                return PARAMS_MISS
        try:
            qrid = data['qrid']
            preusername = data['preusername']
            prephonenum = data['prephonenum']
            username = data['username']
            phonenum = data['phonenum']
            inforcode = data['inforcode']  # 验证码
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
            proof = data['proof']
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
        qr = get_model_return_dict(self.suser.get_qrcode_by_qrid(qrid)) if self.suser.get_qrcode_by_qrid(qrid) else None
        if not qr:
            return NOT_FOUND_QRCODE
        update = {}
        update['QRnumber'] = str(int(qr['QRnumber']) - 1)
        result = self.suser.update_qrcode(qrid, update)
        if not result:
            return NOT_FOUND_QRCODE
        check_phone = self.suser.getuser_by_phonenum(phonenum)
        if check_phone:
            return HAS_REGISTER
        codeinfo = get_model_return_dict(self.smycenter.get_inforcode_by_usphonenum(phonenum)) if self.smycenter\
            .get_inforcode_by_usphonenum(phonenum) else None
        if not codeinfo:
            return SYSTEM_ERROR
        if inforcode != codeinfo['ICcode']:
            return INFORCODE_WRONG
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

    @verify_token_decorator
    def get_register_record(self):
        if not is_admin():
            return TOKEN_ERROR
        try:
            data = request.json
            status = int(data.get('status'))
            page_size = data.get('page_size')
            page_num = data.get('page_num')
        except:
            return PARAMS_ERROR
        list = get_model_return_list(self.suser.get_register_record(status))
        if not list:
            response = import_status("get_registerinfo_success", "OK")
            response['data'] = []
            return response
        from common.timeformat import get_web_time_str
        for record in list:
            record['IRIcreatetime'] = get_web_time_str(record['IRIcreatetime'])
            record['IRIpaytime'] = get_web_time_str(record['IRIpaytime'])
            record['IRIproof'] = record['IRIproof'].split(',')

            if record['IRIarea']:
                area = get_model_return_dict(self.smycenter.get_area_by_areaid(record['IRIarea']))
                city = get_model_return_dict(self.smycenter.get_city_by_cityid(area['cityid']))
                province = get_model_return_dict(self.smycenter.get_province_by_provinceid(city['provinceid']))
                record['address'] = province['provincename'] + city['cityname'] + area['areaname']
            else:
                city = get_model_return_dict(self.smycenter.get_city_by_cityid(record['IRIcity']))
                province = get_model_return_dict(self.smycenter.get_province_by_provinceid(city['provinceid']))
                record['address'] = province['provincename'] + city['cityname']

        mount = len(list)
        page = mount / page_size
        if page == 0 or page == 1 and mount % page_size == 0:
            real_return_list = list[0:]
        else:
            if ((mount - (page_num - 1) * page_size) / page_size) >= 1 and \
                    (mount - (page_num * page_size)) > 0:
                real_return_list = list[((page_num - 1) * page_size):(page_num * page_size)]
            else:
                real_return_list = list[((page_num - 1) * page_size):]
        response = import_status("get_registerinfo_success", "OK")
        response['data'] = real_return_list
        response['mount'] = mount
        return response

    @verify_token_decorator
    def deal_register_record(self):
        if not is_admin():
            return TOKEN_ERROR
        try:
            data = request.json
            IRIid = data.get('IRIid')
            willstatus = data.get('willstatus')
        except:
            return PARAMS_ERROR
        info = get_model_return_dict(self.suser.get_registerrecord_by_IRIid(IRIid))
        if not info:
            return NOT_FOUND_USER
        if willstatus == 2:
            session = db_session()
            try:
                user = self.smycenter.get_user_basicinfo_byphone(info['IRIprephonenum'])  # 插入销售表，有数据就更新
                if not user:
                    raise dberror
                user = get_model_return_dict(user)
                monthnow = datetime.strftime(datetime.now(), format_for_db)[0:6]
                amount_data = self.saccount.get_user_date(user['USid'], monthnow)
                if amount_data:
                    amount_data = get_model_return_dict(amount_data)
                    new_data = {}
                    new_data['reward'] = amount_data['reward'] + float(self.conf.get('account', 'reward'))
                    try:
                        session.query(Amount).filter(Amount.USid == user['USid']).update(new_data)
                    except:
                        raise dberror
                else:
                    amount = Amount()
                    amount.USid = user['USid']
                    amount.AMid = str(uuid.uuid4())
                    amount.USagentid = user['USagentid']
                    amount.USname = user['USname']
                    amount.reward = float(self.conf.get('account', 'reward'))
                    amount.AMstatus = 1
                    amount.USheadimg = user['USheadimg']
                    amount.AMcreattime = datetime.strftime(datetime.now(), format_for_db)
                    amount.AMmonth = datetime.strftime(datetime.now(), format_for_db)[0:6]
                    session.add(amount)

                new_userid = str(uuid.uuid4())  # 插入新用户
                new_user = User()
                new_user.USid = new_userid
                new_user.USname = info['IRIname']
                new_user.USpre = user['USid']
                new_user.USagentid = get_random_str(12)
                new_user.USheadimg = info['IRIpic'] if info['IRIpic'] else 'https://timgsa.baidu.com/timg?image&quality=80&size=b9999_100' \
                                                             '00&sec=1540919391&di=91c' \
                                                             '1ae656341d5814e63280616ad8ade&imgtype=jpg&er=1&src=http%3A%2F%2Fimg.zcool.cn%2Fcommun' \
                                                             'ity%2F0169d55548dff50000019ae9973427.jpg%401280w_1l_2o_100sh.jpg'
                new_user.USphonenum = info['IRIphonenum']
                new_user.USmount = 0
                new_user.USbail = 0
                new_user.USwechat = info['IRIwechat']
                new_user.idcardnum = info['IRIidcardnum']
                new_user.UScreatetime = datetime.strftime(datetime.now(), format_for_db)
                new_user.USpassword = generate_password_hash(info['IRIpassword'])
                session.add(new_user)

                reward = Reward()  # 插入直推奖励表
                reward.REid = str(uuid.uuid4())
                reward.RElastuserid = user['USid']
                reward.REnextuserid = new_userid
                reward.REmonth = datetime.strftime(datetime.now(), format_for_db)[0:6]
                reward.REmount = float(self.conf.get('account', 'reward'))
                reward.REcreatetime = datetime.strftime(datetime.now(), format_for_db)
                session.add(reward)

                session.query(User).filter(User.USid == user['USid'])\
                    .update({"USmount": user['USmount'] + float(self.conf.get('account', 'reward'))})

                # 写入代理消息
                content = u'您推荐的代理已审核通过，直推奖励已发放至余额'
                agent_result = self.smessage.create_agentmessage(session, user['USid']
                                                    , datetime.strftime(datetime.now(), format_for_db), content, 2)
                if not agent_result:
                    return SYSTEM_ERROR

                USname = info['IRIname']  # 插入默认收货地址
                USphonenum = info['IRIphonenum']
                USdatails = info['IRIaddress']
                areaid = info['IRIarea']
                cityid = info['IRIcity']
                if areaid:
                    all_areaid = get_model_return_list(self.smycenter.get_all_areaid())
                    area_list = []
                    for area in all_areaid:
                        area_list.append(area['areaid'])
                    if areaid not in area_list:
                        return BAD_ADDRESS
                    time_time = datetime.now()
                    time_str = datetime.strftime(time_time, format_for_db)
                    uaid = str(uuid.uuid1())
                    exist_default = self.smycenter.get_default_address_by_usid(new_userid)
                    uadefault = True if not exist_default else False
                    self.smycenter.add_address_selfsession(session, uaid, new_userid, USname, USphonenum, USdatails, \
                                                           areaid, uadefault, time_str, None)
                else:
                    all_cityid = get_model_return_list(self.smycenter.get_all_cityid())
                    cityid_list = []
                    for city in all_cityid:
                        cityid_list.append(city['cityid'])
                    if cityid not in cityid_list:
                        return BAD_ADDRESS
                    time_time = datetime.now()
                    time_str = datetime.strftime(time_time, format_for_db)
                    uaid = str(uuid.uuid1())
                    exist_default = self.smycenter.get_default_address_by_usid(new_userid)
                    uadefault = True if not exist_default else False
                    self.smycenter.add_address_selfsession(session, uaid, new_userid, USname, USphonenum, USdatails, \
                                                           None, uadefault, time_str, cityid)
                session.commit()
            except Exception as e:
                print e
                session.rollback()
                return SYSTEM_ERROR
            finally:
                session.close()
        update = {}
        update['IRIstatus'] = int(willstatus)
        result = self.suser.update_register_record(IRIid, update)
        response = import_status("register_success", "OK")
        return response

    @verify_token_decorator
    def check_openid(self):
        if is_tourist():
            return TOKEN_ERROR
        state = request.args.to_dict().get('state')
        usid = request.user.id
        openid = get_model_return_dict(self.saccount.check_openid(usid))
        if not openid['openid']:
            response = {}
            response['message'] = u'执行跳转'
            response['status'] = 302
            data = {}
            update = {}
            state2 = get_random_str(10)
            update['state'] = state2
            result = self.suser.update_user_by_uid(usid, update)
            if not result:
                return SYSTEM_ERROR
            login = WeixinLogin(APP_ID, APP_SECRET)
            state = state2 + "$$$" + state
            data['url'] = login.authorize(SERVER + "/user/get_code", 'snsapi_base', state=state)
            response['data'] = data
            return response
        response = import_status("has_opid", "OK")
        return response

    def get_code(self):
        args = request.args.to_dict()
        code = args.get('code')
        state = args.get('state')
        print code,state
        login = WeixinLogin(APP_ID, APP_SECRET)
        data = login.access_token(code)

        openid = data.openid
        update = {}
        update['openid'] = openid
        state_list = str(state).split('$$$')

        self.suser.update_user_by_state(state_list[0], update)
        # response = import_status("get_openid_success", "OK")
        return flask.redirect(state_list[1])

    @verify_token_decorator
    def get_authorization(self):
        if is_tourist():
            return TOKEN_ERROR
        result = get_model_return_dict(self.suser.get_authorization(request.user.id)) if\
                self.suser.get_authorization(request.user.id) else None
        if result['authorization']:
            response = import_status("get_authorization_success", "OK")
            response['data'] = {
                "url": result['authorization']
            }
            return response
        else:
            from common.make_pic import make_pic
            user = get_model_return_dict(self.smycenter.get_user_basicinfo(request.user.id))
            if not user:
                return SYSTEM_ERROR
            url = make_pic(user['USname'], user['USwechat'], user['USagentid'], user['idcardnum'])
            update = {'authorization': url}
            self.suser.update_user_by_uid(request.user.id, update)
            response = import_status("get_authorization_success", "OK")
            response['data'] = {
                "url": url
            }
            return response

