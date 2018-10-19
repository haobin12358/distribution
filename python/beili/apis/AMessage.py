# -*- coding:utf8 -*-
import sys
import os
from flask import jsonify
from flask_restful import Resource
from control import CMessage
sys.path.append(os.path.dirname(os.getcwd()))

class AMessage(Resource):
    def __init__(self):
        self.cmessage = CMessage()

    def post(self, message):
        print message
        apis = {
            'check_inforcode': 'self.cmycenter.check_inforcode()'
        }
        res = eval(apis[message])
        return jsonify(res)

    def get(self, message):
        print message
        apis = {
            'get_agent_message': 'self.cmessage.get_agentMessage()',
            'get_com_message': 'self.cmessage.get_comMessage()',
            'get_commessage_details': 'self.cmessage.get_commessage_details()',
        }
        res = eval(apis[message])
        return jsonify(res)