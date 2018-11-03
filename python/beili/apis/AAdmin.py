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
            'register': 'self.cadmin.register()',#我的任务1 注册管理员账号
            'delete_admin':'self.cadmin.delete_admin()',#我的任务2 删除管理员
            'findback_pwd': 'self.cuser.findback_pwd()',
            'update_pwd': 'self.cuser.update_pwd()',
            'update_headimg': 'self.cuser.update_headimg()',
            'update_admin':'self.cadmin.update_admin()'#我的任务3 更新信息
        }
        res = eval(apis[admin])
        return jsonify(res)

    def get(self, admin):
        print admin
        apis = {
            'get_single_message': 'self.cuser.get_single_message()',
        }
        res = eval(apis[admin])
        return jsonify(res)
