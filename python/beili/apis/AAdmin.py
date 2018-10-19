# *- coding:utf8 *-
import sys
import os
from flask import jsonify
from flask_restful import Resource
from control.CUser import CUser
from control.CAdmin import CAdmin
sys.path.append(os.path.dirname(os.getcwd()))


class AAdmin(Resource):
    def __init__(self):
        self.cadmin = CAdmin()

    def post(self, admin):
        print admin
        apis = {
            'login': 'self.cadmin.login()',
            'register': 'self.admin.register()',
            'findback_pwd': 'self.cuser.findback_pwd()',
            'update_pwd': 'self.cuser.update_pwd()',
            'update_headimg': 'self.cuser.update_headimg()'
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
