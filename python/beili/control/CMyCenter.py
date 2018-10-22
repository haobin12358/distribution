# *- coding:utf8 *-
import re
import sys
import os
import uuid
import json
import platform
from flask import request
# import logging
from config.response import PARAMS_MISS, SYSTEM_ERROR, PARAMS_ERROR, TOKEN_ERROR, NOT_FOUND_PHONENUM, NOT_FOUND_IMAGE, \
    NO_ADDRESS
from common.token_required import verify_token_decorator, usid_to_token, is_tourist
from common.import_status import import_status
from common.get_model_return_list import get_model_return_list, get_model_return_dict
from service.SMyCenter import SMyCenter
from config.setting import QRCODEHOSTNAME
from common.timeformat import get_db_time_str
from service.SUser import SUser
from models.model import UserAddress
sys.path.append(os.path.dirname(os.getcwd()))


class CMyCenter():

    def __init__(self):
        self.smycenter = SMyCenter()
        self.suser = SUser()

    def get_inforcode(self):
        print "get_inforcode"
        try:
            args = request.args.to_dict()
            print args
            phonenum = args.get('usphonenum')
        except Exception as e:
            return PARAMS_ERROR(u"参数错误")
        if not phonenum:
            return PARAMS_ERROR(u"参数错误")
        user = self.suser.getuser_by_phonenum(phonenum)
        if not user:
            return NOT_FOUND_PHONENUM
        code = ""
        while len(code) < 6:
            import random
            item = random.randint(1, 9)
            code = code + str(item)

        # 获取当前时间，与上一次获取的时间进行比较，小于60秒的获取直接报错
        import datetime
        from common.timeformat import format_for_db
        time_time = datetime.datetime.now()
        time_str = datetime.datetime.strftime(time_time, format_for_db)

        # 根据电话号码获取时间
        time_up = get_model_return_dict(self.smycenter.get_uptime_by_usphonenum(phonenum))
        if time_up:
            time_up_time = datetime.datetime.strptime(time_up['ICtime'], format_for_db)
            delta = time_time - time_up_time
            if delta.seconds < 60:
                return import_status("ERROR_MESSAGE_GET_CODE_FAST", "BEILI_ERROR", "ERROR_CODE_GET_CODE_FAST")

        new_inforcode = self.smycenter.add_inforcode(phonenum, code, time_str)
        if not new_inforcode:
            return SYSTEM_ERROR

        from config.Inforcode import SignName, TemplateCode
        from common.Inforsend import send_sms
        params = '{\"code\":\"' + code + '\",\"product\":\"etech\"}'

        __business_id = uuid.uuid1()
        response_send_message = send_sms(__business_id, phonenum, SignName, TemplateCode, params)
        response_send_message = json.loads(response_send_message)

        if response_send_message["Code"] == "OK":
            status = 200
        else:
            status = 405

        response_ok = {"usphone": phonenum}
        response_ok["status"] = status
        response_ok["messages"] = response_send_message["Message"]
        return response_ok

    def check_inforcode(self):
        data = request.json
        try:
            phonenum = data.get('usphonenum')
            iccode = data.get('iccode')
        except Exception as e:
            return PARAMS_ERROR("参数错误")
        if not phonenum or not iccode:
            return PARAMS_ERROR("参数错误")
        codeinfo = get_model_return_dict(self.smycenter.get_inforcode_by_usphonenum(phonenum))
        if not codeinfo:
            return SYSTEM_ERROR(u"用户验证信息错误")
        checkstatus = True if iccode == codeinfo['ICcode'] else False
        checkmessage = u"验证码正确" if checkstatus is True else u"验证码错误"
        response = import_status("check_inforcode_access", "OK")
        response["data"] = {"checkstatus": checkstatus,
                            "checkmessage": checkmessage
                            }
        return response

    @verify_token_decorator
    def update_headimg(self):  # 更新头像
        # if not is_tourist():
        #     return TOKEN_ERROR
        files = request.files.get("file")
        if not files:
            return NOT_FOUND_IMAGE
        if platform.system() == "Windows":
            rootdir = "D:/task"
        else:
            rootdir = "Users/fx/opt/beili/imgs/mycenter/"
        if not os.path.isdir(rootdir):
            os.makedirs(rootdir)
        lastpoint = str(files.filename).rindex(".")
        filessuffix = str(files.filename)[lastpoint + 1:]
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

    """省市区地址"""
    def get_province(self):
        try:
            province_list = get_model_return_list(self.smycenter.get_province())
            res = import_status("get_province_list_success", "OK")
            res["data"] = province_list
            return res
        except:
            return SYSTEM_ERROR

    def get_city_by_province(self):
        try:
            args = request.args.to_dict()
            province_id = args["provinceid"]
        except:
            return PARAMS_ERROR
        city_list = get_model_return_list(self.smycenter.get_city_by_provincenum(province_id))
        # map(lambda x: x.hide('_id'), city_list)
        res = import_status("get_city_list_success", "OK")
        res["data"] = city_list
        return res

    def get_area_by_city(self):
        try:
            args = request.args.to_dict()
            city_id = args['cityid']
        except:
            return PARAMS_ERROR
        area_list = get_model_return_list(self.smycenter.get_area_by_citynum(city_id))
        res = import_status("get_area_list_success", "OK")
        res["data"] = area_list
        return res

    @verify_token_decorator
    def add_useraddress(self):
        if is_tourist():
            return TOKEN_ERROR

        try:
            data = request.json
            USname = data.get('USname')
            USphonenum = data.get("USphonenum")
            USdatails = data.get("details")
            areaid = data.get("areaid")
        except:
            return PARAMS_ERROR
        try:
            uaid = str(uuid.uuid1())
            exist_default = self.smycenter.get_default_address_by_usid(request.user.id)
            uadefault = True if not exist_default else False
            self.smycenter.add_address(uaid, request.user.id, USname, USphonenum, USdatails, areaid, uadefault)
            response = import_status("add_address_success", "OK")
            response['data'] = {
                "UAid": uaid
            }
            return response
        except:
            return SYSTEM_ERROR

    @verify_token_decorator
    def get_useraddress(self):
        if is_tourist():
            return TOKEN_ERROR
        try:
            data = request.json
            isdefault = int(data.get('isdefault'))
            UAid = data.get('UAid')
        except:
            return PARAMS_ERROR
        if isdefault == 1:
            address = get_model_return_list(self.smycenter.get_default_address(request.user.id))
            area = get_model_return_list(self.smycenter.get_area_by_areaid(address[0]['areaid']))
            city = get_model_return_list(self.smycenter.get_city_by_cityid(area[0]['cityid']))
            province = get_model_return_list(self.smycenter.get_province_by_provinceid(city[0]['provinceid']))
        elif isdefault == 0:
            address = get_model_return_list(self.smycenter.get_other_address(request.user.id, UAid))
            if not address:
                return NO_ADDRESS
            area = get_model_return_list(self.smycenter.get_area_by_areaid(address[0]['areaid']))
            city = get_model_return_list(self.smycenter.get_city_by_cityid(area[0]['cityid']))
            province = get_model_return_list(self.smycenter.get_province_by_provinceid(city[0]['provinceid']))
        data = {}
        data['provincename'] = province[0]['provincename']
        data['cityname'] = city[0]['cityname']
        data['areaname'] = area[0]['areaname']
        data['details'] = address[0]['UAdetails']
        data['username'] = address[0]['UAname']
        data['userphonenum'] = address[0]['UAphonenum']
        data['uaid'] = address[0]['UAid']
        response = import_status("get_address_success", "OK")
        response['data'] = data
        return response



