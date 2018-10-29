# -*- coding:utf8 -*-
import sys
import os
from flask import jsonify
from flask_restful import Resource
from control.COrder import COrder
from control.CAccount import CAccount
sys.path.append(os.path.dirname(os.getcwd()))

class AAccount(Resource):
    def __init__(self):
        self.caccount = CAccount()

    def post(self, account):
        print account
        apis = {
            'get_account': 'self.caccount.get_account()'
        }
        res = eval(apis[account])
        return jsonify(res)

    def get(self, account):
        print account
        apis = {

        }
        res = eval(apis[account])
        return jsonify(res)