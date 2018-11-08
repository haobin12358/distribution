# *- coding:utf8 *-
import re
import sys
import os
import uuid
from flask import request
# import logging
from config.response import PARAMS_MISS, SYSTEM_ERROR, PARAMS_ERROR, TOKEN_ERROR, AUTHORITY_ERROR
from config.setting import QRCODEHOSTNAME
from common.token_required import verify_token_decorator, usid_to_token, is_tourist, is_admin
from common.import_status import import_status
from common.timeformat import get_db_time_str
from common.get_model_return_list import get_model_return_list, get_model_return_dict
from service.SUser import SUser
from service.SMessage import SMessage
import platform
sys.path.append(os.path.dirname(os.getcwd()))


class CMessage():

    def __init__(self):
        self.suser = SUser()
        self.smessage = SMessage()

    @verify_token_decorator
    def get_agentMessage(self):
        print "hello"
        if is_tourist():
            return TOKEN_ERROR
        try:
            args = request.args.to_dict()
            page = int(args.get('page', 1))  # 页码
            count = int(args.get('count', 15))  # 取出条数
        except Exception as e:
            return PARAMS_ERROR
        from common.timeformat import get_web_time_str
        message_list, mount = self.smessage.get_agentMessage_by_usid(request.user.id, page, count)
        message_list = get_model_return_list(message_list)
        message_return = []
        for message in message_list:
            data = {}
            data['USid'] = message['USid']
            data['AMdate'] = get_web_time_str(message['AMdate'])
            data['AMid'] = message['AMid']
            data['AMcontent'] = message['AMcontent']
            data['AMtype'] = message['AMtype']
            message_return.append(data)
        data = import_status('get_agentmessage_list_success', 'OK')
        data['data'] = message_return
        data['mount'] = mount
        return data

    @verify_token_decorator
    def get_comMessage(self):
        if is_tourist():
            return TOKEN_ERROR
        try:
            args = request.args.to_dict()
            page = int(args.get('page', 1))  # 页码
            count = int(args.get('count', 10))  # 取出条数
        except Exception as e:
            return PARAMS_ERROR
        if is_admin():
            comMessage_list = get_model_return_list(self.smessage.get_comMessage_list(page, count))  # 分页查询出的公司消息列表
            data = import_status('get_commessage_list_success', 'OK')
            data['data'] = comMessage_list
            return data
        else:
            comMessage_num = self.smessage.get_commessage_num()  # 公司消息总条数
            print comMessage_num
            comMessage_list = get_model_return_list(self.smessage.get_comMessage_list(page, count))  # 分页查询出的公司消息列表
            print len(comMessage_list)
            a = request.user.id
            already_list = get_model_return_list(self.smessage.get_alreadyMessage_by_usid(request.user.id)) # 已经阅读的消息的id集合
            already_id_list = []
            for already in already_list:
                already_id_list.append(already['ARmessageid'])
            notread_count = int(comMessage_num) - len(already_list)  # 该用户未读的消息条数
            return_message_list = []
            from common.timeformat import get_web_time_str
            for message in comMessage_list:
                message_dic = {}
                if message['CMid'] not in already_id_list:  # 如果没有读，加个标记isread
                    message_dic['isread'] = 0
                    message_dic['CMid'] = message['CMid']
                    message_dic['CMdate'] = get_web_time_str(message['CMdate'])
                    message_dic['CMtype'] = message['CMtype']
                    message_dic['CMtitle'] = message['CMtitle']
                    message_dic['CMfile'] = message['CMfile']
                    return_message_list.append(message_dic)
                else:
                    message_dic['isread'] = 1
                    message_dic['CMid'] = message['CMid']
                    message_dic['CMdate'] = get_web_time_str(message['CMdate'])
                    message_dic['CMtype'] = message['CMtype']
                    message_dic['CMtitle'] = message['CMtitle']
                    message_dic['CMfile'] = message['CMfile']
                    return_message_list.append(message_dic)
            data = import_status('get_commessage_list_success', 'OK')
            data['notread'] = notread_count
            data['data'] = return_message_list
            data['mount'] = int(comMessage_num)
            return data

    @verify_token_decorator
    def get_commessage_details(self):
        if is_tourist():
            return TOKEN_ERROR
        try:
            args = request.args.to_dict()
            messageid = args.get('messageid')
        except Exception as e:
            return PARAMS_ERROR
        message = get_model_return_dict(self.smessage.get_commessage_details(messageid))
        from common.timeformat import get_web_time_str
        message['CMdate'] = get_web_time_str(message['CMdate'])
        data = import_status('get_commessage_details_success', 'OK')
        data['data'] = message
        if is_admin():
            return data
        else:
            try:
                note = self.smessage.get_isread(messageid, request.user.id)
                if note:
                    return data
                else:
                    self.smessage.insert_alreadyread(str(uuid.uuid4()), messageid, request.user.id)
                    return data
            except Exception as e:
                print 'repeat'


    @verify_token_decorator
    def publish_commessage(self):
        if not is_admin():
            return AUTHORITY_ERROR

        try:
            json_data = request.json
            type = json_data.get('type')
            title = json_data.get('title')
            url = json_data.get('url')
        except Exception as e:
            return PARAMS_ERROR
        if not title or not url:
            return PARAMS_MISS
        # 获取当前时间
        import datetime
        from common.timeformat import format_for_db
        time_time = datetime.datetime.now()
        time_str = datetime.datetime.strftime(time_time, format_for_db)
        id = str(uuid.uuid4())
        self.smessage.publish_commessage(id, time_str, type, title, url)
        response = import_status("publish_message_success", "OK")
        return response

    @verify_token_decorator
    def delete_commessage(self):
        if not is_admin():
            return AUTHORITY_ERROR
        try:
            json_data = request.json
            messageid = json_data.get('messageid')
        except Exception as e:
            return PARAMS_ERROR
        upate_message = {}
        upate_message['CMstatus'] = 0
        self.smessage.delete_commessage(messageid, upate_message)
        self.smessage.delete_alreadyread(messageid)
        response = import_status("delete_message_success", "OK")
        return response

    @verify_token_decorator
    def change_registerstatus(self):
        try:
            json_data = request.json
            IRIid = json_data.get('IRIid')
        except Exception as e:
            return PARAMS_ERROR
        self.smessage.update_status(IRIid)

    @verify_token_decorator
    def message(self):
        pass
