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
            'get_account': 'self.caccount.get_account()',
            'get_rank_list': 'self.caccount.get_rank_list()',
            'draw_money': 'self.caccount.draw_money()',
            'get_drawmoney_list': 'self.caccount.get_drawmoney_list()',
            'charge_monney': 'self.caccount.charge_monney()',
            'get_chargemoney_list': 'self.caccount.get_chargemoney_list()',
            'charge_draw_bail': 'self.caccount.charge_draw_bail()'
        }
        res = eval(apis[account])
        return jsonify(res)

    def get(self, account):
        print account
        apis = {
            'get_directagent': 'self.caccount.get_directagent()',
            'get_distribute': 'self.caccount.get_distribute()',
            'get_draw_info': 'self.caccount.get_draw_info()',
            'check_bail': 'self.caccount.check_bail()'

        }
        res = eval(apis[account])
        return jsonify(res)