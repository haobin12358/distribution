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
            'charge_draw_bail': 'self.caccount.charge_draw_bail()',
            'get_alluser_account': 'self.caccount.get_alluser_account()',
            'get_directagent_performance': "self.caccount.get_directagent_performance()",
            "get_all_performance": "self.caccount.get_all_performance()",
            'get_alluser_drawmoney_list': 'self.caccount.get_alluser_drawmoney_list()',
            'deal_drawmoney': 'self.caccount.deal_drawmoney()',
            'get_all_chargemoney': 'self.caccount.get_all_chargemoney()',
            'deal_chargemoney': 'self.caccount.deal_chargemoney()',
            'get_alluser_bailrecord': 'self.caccount.get_alluser_bailrecord()',
            'deal_bailrecord': 'self.caccount.deal_bailrecord()',
            'deal_reward_discount': 'self.caccount.deal_reward_discount()',
            'weixin_pay': 'self.caccount.weixin_pay()',
            'pay_callback': 'self.caccount.pay_callback()',
            'update_configure': 'self.caccount.update_configure()',
            'update_discountruler': 'self.caccount.update_discountruler()'
        }
        res = eval(apis[account])
        if account == 'pay_callback':
            print " pay_callback response" , res
            return res
        return jsonify(res)

    def get(self, account):
        print account
        apis = {
            'get_directagent': 'self.caccount.get_directagent()',
            'get_distribute': 'self.caccount.get_distribute()',
            'get_draw_info': 'self.caccount.get_draw_info()',
            'check_bail': 'self.caccount.check_bail()',
            'get_moneyrecord': 'self.caccount.get_moneyrecord()',
            'get_sevendays_data': 'self.caccount.get_sevendays_data()',
            'get_thisyear_date': 'self.caccount.get_thisyear_date()',
            'get_count_data': 'self.caccount.get_count_data()',
            'get_thismonth_agentnum': 'self.caccount.get_thismonth_agentnum()',
            'get_discountruler': 'self.caccount.get_discountruler()',
            'get_configure': 'self.caccount.get_configure()'

        }
        res = eval(apis[account])
        return jsonify(res)