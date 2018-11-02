# -*- coding:utf8 -*-
import sys
import os
from flask import jsonify
from flask_restful import Resource
from control.CMessage import CMessage
sys.path.append(os.path.dirname(os.getcwd()))

class AMessage(Resource):
    def __init__(self):
        self.cmessage = CMessage()

    def post(self, message):
        print message
        apis = {
            'publish_commessage': 'self.cmessage.publish_commessage()',
            'delete_commessage': 'self.cmessage.delete_commessage()',
            'change_registerstatus': 'self.cmessage.change_registerstatus()'
        }
        res = eval(apis[message])
        return jsonify(res)

    def get(self, message):
        print message
        apis = {
            'get_agent_message': 'self.cmessage.get_agentMessage()',
            'get_com_message': 'self.cmessage.get_comMessage()',
            'get_commessage_details': 'self.cmessage.get_commessage_details()'
        }
        res = eval(apis[message])
        return jsonify(res)