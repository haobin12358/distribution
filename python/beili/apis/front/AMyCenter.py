# -*- coding:utf8 -*-
import sys
import os
from flask import jsonify
from flask_restful import Resource
from control.front import CMyCenter
sys.path.append(os.path.dirname(os.getcwd()))

class AMyCenter(Resource):
    def __init__(self):
        self.cmycenter = CMyCenter()

    def post(self, mycenter):
        print mycenter
        apis = {
            'check_inforcode': 'self.cmycenter.check_inforcode()'
        }
        res = eval(apis[mycenter])
        return jsonify(res)

    def get(self, mycenter):
        print mycenter
        apis = {
            'get_inforcode': 'self.cmycenter.get_inforcode()',
        }
        res = eval(apis[mycenter])
        return jsonify(res)