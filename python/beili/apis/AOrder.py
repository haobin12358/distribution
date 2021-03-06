# -*- coding:utf8 -*-
import sys
import os
from flask import jsonify
from flask_restful import Resource
from control.COrder import COrder
sys.path.append(os.path.dirname(os.getcwd()))

class AOrder(Resource):
    def __init__(self):
        self.corder = COrder()

    def post(self, order):
        print order
        apis = {
            'create_order': 'self.corder.create_order()',
            'get_order_list': 'self.corder.get_order_list()',
            'get_order_details': 'self.corder.get_order_details()',
            'get_all_order': 'self.corder.get_all_order()',
            'update_order': 'self.corder.update_order()',
            'cancel_order': 'self.corder.cancel_order()',
            'get_willsend_products': 'self.corder.get_willsend_products()'
        }
        res = eval(apis[order])
        return jsonify(res)

    def get(self, order):
        print order
        apis = {

        }
        res = eval(apis[order])
        return jsonify(res)