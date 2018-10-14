# *- coding:utf8 *-
import sys
import os
from flask import jsonify
from flask_restful import Resource
from control.Cuser import CUser
sys.path.append(os.path.dirname(os.getcwd()))


class AUser(Resource):
    def __init__(self):
        self.cuser = CUser()

    def post(self, user):
        print user
        apis = {
            'login': 'self.cuser.login()',
            'register': 'self.cuser.register()',
            'update_pwd': 'self.cuser.update_pwd()',
            'update_single_pic': 'self.cuser.update_single_pic()'
        }
        res = eval(apis[user])
        return jsonify(res)

    def get(self, user):
        print user
        apis = {
            'get_single_message': 'self.cuser.get_single_message()',
        }
        res = eval(apis[user])
        return jsonify(res)
