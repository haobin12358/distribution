# *- coding:utf8 *-
import sys
import os
from flask import jsonify
from flask_restful import Resource
from control.CUser import CUser
sys.path.append(os.path.dirname(os.getcwd()))


class AUser(Resource):
    def __init__(self):
        self.cuser = CUser()

    def post(self, user):
        print user
        apis = {
            'login': 'self.cuser.login()',
            'register': 'self.cuser.register()',
            'findback_pwd': 'self.cuser.findback_pwd()',
            'update_pwd': 'self.cuser.update_pwd()',
            'update_headimg': 'self.cuser.update_headimg()',
            'upload_file': 'self.cuser.upload_file()',
            'remove_file':'self.cuser.remove_file()',
            'delete_qrcode': 'self.cuser.delete_qrcode()',
            'add_qrcode': 'self.cuser.add_qrcode()',
            'get_registerinfo': 'self.cuser.get_registerinfo()',
            'check_qrcode': 'self.cuser.check_qrcode()'
        }
        res = eval(apis[user])
        return jsonify(res)

    def get(self, user):
        print user
        apis = {
            'get_single_message': 'self.cuser.get_single_message()',
            'get_qrcode': 'self.cuser.get_qrcode()',
            'check_openid': 'self.cuser.check_openid()'
        }
        res = eval(apis[user])
        return jsonify(res)
