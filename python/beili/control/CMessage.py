# *- coding:utf8 *-
import re
import sys
import os
from flask import request
# import logging
from config.response import PARAMS_MISS, SYSTEM_ERROR, PARAMS_ERROR, TOKEN_ERROR, NOT_FOUND, AUTHORITY_ERROR
from config.setting import QRCODEHOSTNAME
from common.token_required import verify_token_decorator, usid_to_token, is_tourist, is_ordirnaryuser
from common.import_status import import_status
from common.timeformat import get_db_time_str
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
            return TOKEN_ERROR(u"未登录")
        try:
            args = request.args.to_dict()
            page = int(args.get('page', 1))  # 页码
            count = int(args.get('count', 15))  # 取出条数
        except Exception as e:
            return PARAMS_ERROR
        user = self.suser.getuser_by_uid(request.user.id)
        message_list = self.smessage.get_agentMessage_by_usid(user.USid, page, count)
        data = import_status('get_agentmessage_list_success', 'OK')
        data['data'] = message_list
        return data

    @verify_token_decorator
    def get_comMessage(self):
        if is_tourist():
            return TOKEN_ERROR(u"未登录")
        try:
            args = request.args.to_dict()
            page = int(args.get('page', 1))  # 页码
            count = int(args.get('count', 10))  # 取出条数
        except Exception as e:
            return PARAMS_ERROR
        comMessage_num = self.smessage.get_commessage_num()  # 公司消息总条数
        comMessage_list = self.smessage.get_comMessage_list(page, count)  # 分页查询出的公司消息列表
        already_list = self.smessage.get_alreadyMessage_by_usid(request.user.id)  # 已经阅读的消息的id集合
        notread_count = comMessage_num - len(already_list)  # 该用户未读的消息条数
        return_message_list = []
        for message in comMessage_list:
            message_dic = {}
            if message.CMid not in already_list:  # 如果没有读，加个标记isread
                message_dic['isread'] = 0
                message_dic['CMid'] = message.CMid
                message_dic['CMdate'] = message.CMdate
                message_dic['CMtype'] = message.CMtype
                message_dic['CMtext'] = message.CMtext
                message_dic['CMpic'] = message.CMpic
                return_message_list.append(message_dic)
            else:
                message_dic['isread'] = 1
                message_dic['CMid'] = message.CMid
                message_dic['CMdate'] = message.CMdate
                message_dic['CMtype'] = message.CMtype
                message_dic['CMtext'] = message.CMtext
                message_dic['CMpic'] = message.CMpic
                return_message_list.append(message_dic)
        data = import_status('get_commessage_list_success', 'OK')
        data['notread'] = notread_count
        data['data'] = return_message_list

    @verify_token_decorator
    def get_commessage_details(self):
        if is_tourist():
            return TOKEN_ERROR(u"未登录")
        try:
            json_data = request.json
            messageid = json_data.get('messageid')
        except Exception as e:
            return PARAMS_ERROR
        if not messageid:
            return PARAMS_MISS
        message = self.smessage.get_commessage_details(messageid)
        self.smessage.update_commessage_status(messageid, request.user.id)
        data = import_status('get_commessage_details_success', 'OK')
        data['data'] = message
        return data
