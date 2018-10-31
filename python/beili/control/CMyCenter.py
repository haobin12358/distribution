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
    NO_ADDRESS, NOT_FOUND_ADDRESS, BAD_ADDRESS, UPDATE_ADDRESS_FAIL, CHANGE_ADDRESS_FAIL
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
            return PARAMS_ERROR
        if not phonenum:
            return PARAMS_ERROR
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
            return PARAMS_ERROR
        if not phonenum or not iccode:
            return PARAMS_ERROR
        codeinfo = get_model_return_dict(self.smycenter.get_inforcode_by_usphonenum(phonenum))
        if not codeinfo:
            return SYSTEM_ERROR
        checkstatus = True if iccode == codeinfo['ICcode'] else False
        checkmessage = u"验证码正确" if checkstatus is True else u"验证码错误"
        response = import_status("check_inforcode_access", "OK")
        response["data"] = {"checkstatus": checkstatus,
                            "checkmessage": checkmessage
                            }
        return response

    @verify_token_decorator
    def update_headimg(self):  # 更新头像
        if is_tourist():
           return TOKEN_ERROR
        files = request.files.get("file")
        if not files:
            return NOT_FOUND_IMAGE
        if platform.system() == "Windows":
            rootdir = "D:/task"
        else:
            rootdir = "/opt/beili/file/mycenter/"
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
        url = QRCODEHOSTNAME + "/file/mycenter/" + filename
        user_update = {}
        user_update['USheadimg'] = url
        self.suser.update_user_by_uid(request.user.id, user_update)
        response["data"] = url
        return response

    @verify_token_decorator
    def get_user_basicinfo(self):
        if is_tourist():
            return TOKEN_ERROR
        result = get_model_return_dict(self.smycenter.get_user_basicinfo(request.user.id))
        if result:
            res = import_status("get_user_basicinfo_success", "OK")
            res['data'] = result
            return res
        else:
            return SYSTEM_ERROR

    @verify_token_decorator
    def get_user_totalinfo(self):
        if is_tourist():
            return TOKEN_ERROR
        result = get_model_return_dict(self.smycenter.get_user_totalinfo(request.user.id))
        if result:
            res = import_status("get_user_basicinfo_success", "OK")
            res['data'] = result
            return res
        else:
            return SYSTEM_ERROR


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

    def get_all_area(self):
        try:
            province_return = []
            province_list = get_model_return_list(self.smycenter.get_province())
            for province in province_list:
                province_dic = {}
                province_dic['name'] = province['provincename']
                province_dic['id'] = province['provinceid']
                city_list = get_model_return_list(self.smycenter.get_city_by_provincenum(province['provinceid']))
                city_return = []
                for city in city_list:
                        city_dic = {}
                        city_dic['name'] = city['cityname']
                        city_dic['id'] = city['cityid']
                        area_list = get_model_return_list(self.smycenter.get_area_by_citynum(city['cityid']))
                        area_return = []
                        for area in area_list:
                            area_dict = {}
                            area_dict['name'] = area['areaname']
                            area_dict['id'] = area['areaid']
                            area_return.append(area_dict)
                        city_dic['area'] = area_return
                        city_return.append(city_dic)
                province_dic['city'] = city_return
                province_return.append(province_dic)
            res = import_status("get_all_area_success", "OK")
            res['data'] = province_return
        except:
            return SYSTEM_ERROR
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
            if not areaid:
                cityid = data.get("cityid")
        except:
            return PARAMS_ERROR
        try:
            if areaid:
                all_areaid = get_model_return_list(self.smycenter.get_all_areaid())
                area_list = []
                for area in all_areaid:
                    area_list.append(area['areaid'])
                if areaid not in area_list:
                    return BAD_ADDRESS
                import datetime
                from common.timeformat import format_for_db
                time_time = datetime.datetime.now()
                time_str = datetime.datetime.strftime(time_time, format_for_db)
                uaid = str(uuid.uuid1())
                exist_default = self.smycenter.get_default_address_by_usid(request.user.id)
                uadefault = True if not exist_default else False
                self.smycenter.add_address(uaid, request.user.id, USname, USphonenum, USdatails, areaid, uadefault, time_str, None)
                response = import_status("add_address_success", "OK")
                response['data'] = {
                    "UAid": uaid
                }
                return response
            else :
                all_cityid = get_model_return_list(self.smycenter.get_all_cityid())
                cityid_list = []
                for city in all_cityid:
                    cityid_list.append(city['cityid'])
                if cityid not in cityid_list:
                    return BAD_ADDRESS
                import datetime
                from common.timeformat import format_for_db
                time_time = datetime.datetime.now()
                time_str = datetime.datetime.strftime(time_time, format_for_db)
                uaid = str(uuid.uuid1())
                exist_default = self.smycenter.get_default_address_by_usid(request.user.id)
                uadefault = True if not exist_default else False
                self.smycenter.add_address(uaid, request.user.id, USname, USphonenum, USdatails, None, uadefault, time_str, cityid)
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
            all = int(data.get('all'))
            UAid = data.get('UAid')
        except:
            return PARAMS_ERROR
        from common.timeformat import get_web_time_str
        if all == 1:
            all_address = get_model_return_list(self.smycenter.get_all_address(request.user.id))
            if not all_address:
                response = import_status("get_address_success", "OK")
                response['data'] = []
                return response
            address_list = []
            for address in all_address:
                address = get_model_return_dict(self.smycenter.get_other_address(request.user.id, address['UAid']))
                if not address:
                    return NO_ADDRESS
                area = get_model_return_dict(self.smycenter.get_area_by_areaid(address['areaid']))
                if area:
                    city = get_model_return_dict(self.smycenter.get_city_by_cityid(area['cityid']))
                    province = get_model_return_dict(self.smycenter.get_province_by_provinceid(city['provinceid']))
                    data = {}
                    data['provincename'] = province['provincename']
                    data['provinceid'] = province['provinceid']
                    data['cityname'] = city['cityname']
                    data['cityid'] = city['cityid']
                    data['areaname'] = area['areaname']
                    data['areaid'] = area['areaid']
                    data['details'] = address['UAdetails']
                    data['username'] = address['UAname']
                    data['userphonenum'] = address['UAphonenum']
                    data['uaid'] = address['UAid']
                    data['isdefault'] = address['UAdefault']
                    data['createtime'] = get_web_time_str(address['UAcreatetime'])
                    address_list.append(data)
                else:
                    city = get_model_return_dict(self.smycenter.get_city_by_cityid(address['cityid']))
                    province = get_model_return_dict(self.smycenter.get_province_by_provinceid(city['provinceid']))
                    data = {}
                    data['provincename'] = province['provincename']
                    data['provinceid'] = province['provinceid']
                    data['cityname'] = city['cityname']
                    data['cityid'] = city['cityid']
                    data['details'] = address['UAdetails']
                    data['username'] = address['UAname']
                    data['userphonenum'] = address['UAphonenum']
                    data['uaid'] = address['UAid']
                    data['isdefault'] = address['UAdefault']
                    data['createtime'] = get_web_time_str(address['UAcreatetime'])
                    address_list.append(data)
            response = import_status("get_address_success", "OK")
            response['data'] = address_list
            return response
        if isdefault == 1:
            address = get_model_return_dict(self.smycenter.get_default_address(request.user.id))
            if not address:
                response = import_status("get_address_success", "OK")
                response['data'] = []
                return response
            area = get_model_return_dict(self.smycenter.get_area_by_areaid(address['areaid']))
            if area:
                city = get_model_return_dict(self.smycenter.get_city_by_cityid(area['cityid']))
                province = get_model_return_dict(self.smycenter.get_province_by_provinceid(city['provinceid']))
                data = {}
                data['provincename'] = province['provincename']
                data['provinceid'] = province['provinceid']
                data['cityname'] = city['cityname']
                data['cityid'] = city['cityid']
                data['areaname'] = area['areaname']
                data['areaid'] = area['areaid']
                data['details'] = address['UAdetails']
                data['username'] = address['UAname']
                data['userphonenum'] = address['UAphonenum']
                data['uaid'] = address['UAid']
                data['createtime'] = get_web_time_str(address['UAcreatetime'])
                response = import_status("get_address_success", "OK")
                response['data'] = data
                return response
            else:
                city = get_model_return_dict(self.smycenter.get_city_by_cityid(address['cityid']))
                province = get_model_return_dict(self.smycenter.get_province_by_provinceid(city['provinceid']))
                data = {}
                data['provincename'] = province['provincename']
                data['provinceid'] = province['provinceid']
                data['cityname'] = city['cityname']
                data['cityid'] = city['cityid']
                data['details'] = address['UAdetails']
                data['username'] = address['UAname']
                data['userphonenum'] = address['UAphonenum']
                data['uaid'] = address['UAid']
                data['createtime'] = get_web_time_str(address['UAcreatetime'])
                response = import_status("get_address_success", "OK")
                response['data'] = data
                return response
        elif isdefault == 0:
            address = get_model_return_dict(self.smycenter.get_other_address(request.user.id, UAid))
            if not address:
                response = import_status("get_address_success", "OK")
                response['data'] = []
                return response
            area = get_model_return_dict(self.smycenter.get_area_by_areaid(address['areaid']))
            if area:
                city = get_model_return_dict(self.smycenter.get_city_by_cityid(area['cityid']))
                province = get_model_return_dict(self.smycenter.get_province_by_provinceid(city['provinceid']))
                data = {}
                data['provincename'] = province['provincename']
                data['provinceid'] = province['provinceid']
                data['cityname'] = city['cityname']
                data['cityid'] = city['cityid']
                data['areaname'] = area['areaname']
                data['areaid'] = area['areaid']
                data['details'] = address['UAdetails']
                data['username'] = address['UAname']
                data['userphonenum'] = address['UAphonenum']
                data['uaid'] = address['UAid']
                data['createtime'] = get_web_time_str(address['UAcreatetime'])
                response = import_status("get_address_success", "OK")
                response['data'] = data
                return response
            else:
                city = get_model_return_dict(self.smycenter.get_city_by_cityid(address['cityid']))
                province = get_model_return_dict(self.smycenter.get_province_by_provinceid(city['provinceid']))
                data = {}
                data['provincename'] = province['provincename']
                data['provinceid'] = province['provinceid']
                data['cityname'] = city['cityname']
                data['cityid'] = city['cityid']
                data['details'] = address['UAdetails']
                data['username'] = address['UAname']
                data['userphonenum'] = address['UAphonenum']
                data['uaid'] = address['UAid']
                data['createtime'] = get_web_time_str(address['UAcreatetime'])
                response = import_status("get_address_success", "OK")
                response['data'] = data
                return response

    @verify_token_decorator
    def update_useraddress(self):
        if is_tourist():
            return TOKEN_ERROR
        try:
            data = request.json
            #print data
            UAid = data.get('UAid')
            USname = data.get('USname')
            USphonenum = data.get('USphonenum')
            details = data.get('details')
            areaid = data.get('areaid')
        except:
            return PARAMS_ERROR
        update_address = {}
        update_address['UAname'] = USname
        update_address['UAphonenum'] = USphonenum
        update_address['UAdetails'] = details
        update_address['areaid'] = areaid
        update_result = self.smycenter.update_address(request.user.id, UAid, update_address)
        if update_result:
            response = import_status("update_address_success", "OK")
            return response
        else:
            return UPDATE_ADDRESS_FAIL

    @verify_token_decorator
    def change_default(self):
        if is_tourist():
            return TOKEN_ERROR
        try:
            data = request.json
            old_defaultid = data.get('old_defaultid')
            new_defaultid = data.get('new_defaultid')
        except:
            return PARAMS_ERROR
        change_result = self.smycenter.change_default(request.user.id, old_defaultid, new_defaultid)
        if change_result:
            response = import_status("change_address_success", "OK")
            return response
        else:
            return CHANGE_ADDRESS_FAIL


    @verify_token_decorator
    def delete_useraddress(self):
        if is_tourist():
            return TOKEN_ERROR
        try:
            data = request.json
            UAid = data.get('UAid')
        except:
            return PARAMS_ERROR
        this_address = get_model_return_dict(self.smycenter.get_other_address(request.user.id, UAid))
        if not this_address:
            return  NOT_FOUND_ADDRESS
        updatde_address = {}
        updatde_address['UAstatus'] = False
        result = self.smycenter.delete_useraddress(request.user.id, UAid, updatde_address)
        if result:
            if this_address['UAdefault']:
                try:
                    one_address = get_model_return_dict(self.smycenter.get_one_address())
                    if one_address:
                        updatde_address = {}
                        updatde_address['UAdefault'] = True
                        self.smycenter.set_default(one_address['UAid'], updatde_address)
                except:
                    return SYSTEM_ERROR
            response = import_status("delete_address_success", "OK")
            return response
        else:
            return NOT_FOUND_ADDRESS