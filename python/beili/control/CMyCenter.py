# *- coding:utf8 *-
import re
import sys
import os
import uuid
import json
from flask import request
# import logging
from config.response import PARAMS_MISS, SYSTEM_ERROR, PARAMS_ERROR, TOKEN_ERROR, NOT_FOUND
from common.token_required import verify_token_decorator, usid_to_token, is_tourist
from common.import_status import import_status
from service.front import SMyCenter
sys.path.append(os.path.dirname(os.getcwd()))


class CMyCenter():

    def __init__(self):
        self.smycenter = SMyCenter()

    def get_inforcode(self):
        print "get_inforcode"
        try:
            args = request.args.to_dict()
            phonenum = args.get('usphonenum')
        except Exception as e:
            return PARAMS_ERROR(u"参数错误")
        if not phonenum:
            return PARAMS_ERROR(u"参数错误")
        user = self.suser.getuser_by_phonenum(phonenum)
        if not user:
            return NOT_FOUND(u"该号码未注册")
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
        time_up = self.smycenter.get_uptime_by_usphonenum(phonenum)
        if time_up:
            time_up_time = datetime.datetime.strptime(time_up.ICtime, format_for_db)
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

    def check_inforcode(self):
        data = request.json
        try:
            phonenum = data.get('usphonenum')
            iccode = data.get('iccode')
        except Exception as e:
            return PARAMS_ERROR("参数错误")
        if not phonenum or not iccode:
            return PARAMS_ERROR("参数错误")
        codeinfo = self.smycenter.get_inforcode_by_usphonenum(phonenum)
        if not codeinfo:
            return SYSTEM_ERROR(u"用户验证信息错误")
        checkstatus = True if iccode == codeinfo.ICcode else False
        checkmessage = u"验证码正确" if checkstatus is True else u"验证码错误"
        response = import_status("check_inforcode_access", "OK")
        response["data"] = {"checkstatus": checkstatus,
                            "checkmessage": checkmessage
                            }
        return response
