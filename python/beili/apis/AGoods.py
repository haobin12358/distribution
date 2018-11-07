# *- coding:utf8 *-
import sys
import os
from flask import jsonify
from flask_restful import Resource
from control.CGoods import CGoods
sys.path.append(os.path.dirname(os.getcwd()))


class AGoods(Resource):

    def __init__(self):
        self.cgoods = CGoods()

    def get(self, product):
        print(product)
        apis = {
            "get_product_list": "self.cgoods.get_product_list()",
            "get_product": "self.cgoods.get_product()",
            "get_product_category": "self.cgoods.get_product_category()",
            "get_product_category_list":"self.cgoods.get_product_category_list()",
        }
        res = eval(apis[product])
        return res

    def post(self, product):
        print(product)
        apis = {
            "new_product": "self.cgoods.new_product()",
            "update_product": "self.cgoods.update_product()",
            "add_product_category": "self.cgoods.add_product_category()",
            "update_category": "self.cgoods.update_category()",
            "delete_category": "self.cgoods.delete_category()",
        }
        res = eval(apis[product])
        return res