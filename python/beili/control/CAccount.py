# *- coding:utf8 *-
import re
import sys
import os
import uuid
import random
from flask import request
# import logging
from config.response import PARAMS_MISS, SYSTEM_ERROR, PARAMS_ERROR, TOKEN_ERROR, AUTHORITY_ERROR, STOCK_NOT_ENOUGH,\
        NO_ENOUGH_MOUNT, NO_BAIL, NO_ADDRESS, NOT_FOUND_USER
from config.setting import QRCODEHOSTNAME, DRAWBANK
from common.token_required import verify_token_decorator, usid_to_token, is_tourist, is_admin
from common.import_status import import_status
from common.timeformat import get_db_time_str
from common.get_model_return_list import get_model_return_list, get_model_return_dict
from service.SUser import SUser
from service.SMessage import SMessage
from service.SOrder import SOrder
from service.SGoods import SGoods
from service.SMyCenter import SMyCenter
from service.DBSession import db_session
from service.SAccount import SAccount
import platform
from common.beili_error import stockerror, dberror
from datetime import datetime
from common.timeformat import format_for_db
from models.model import User, AgentMessage
sys.path.append(os.path.dirname(os.getcwd()))


class CAccount():

    def __init__(self):
        self.suser = SUser()
        self.sorder = SOrder()
        self.sgoods = SGoods()
        self.smycenter = SMyCenter()
        self.smessage = SMessage()
        self.saccount = SAccount()
        self.rulerlist = get_model_return_list(self.saccount.get_discount_ruler())

    @verify_token_decorator
    def get_account(self):
        if is_tourist():
            return TOKEN_ERROR
        try:
            data = request.json
            month = str(data.get('month'))
        except:
            return PARAMS_ERROR
        id = request.user.id
        account = get_model_return_dict(self.saccount.get_account_by_month(id, month)) if self.saccount.get_account_by_month(id, month) else None
        if not account:
            response = import_status("get_saleinfo_success", "OK")
            data2 = {}
            data2["reward"] = 0
            data2["discount"] = 0
            data2["performance"] = 0
            data2["myprofit"] = 0
            response['data'] = data2
            return response
        mydiscount = self.get_mydiscount(id, month)
        teamperformance = self.get_myteamsalenum(id, month)
        response = import_status("get_saleinfo_success", "OK")
        data2 = {}
        data2["reward"] = account['reward']
        data2["discount"] = mydiscount
        data2["performance"] = teamperformance
        data2["myprofit"] = account['reward'] + mydiscount
        response['data'] = data2
        return response

    def get_mydiscount(self, id, month):  # 获取个人的销售折扣数
        myteamnum = self.get_myteamsalenum(id, month)  # 团队总销售量
        myteamnummoney = self.get_discount_ratio(myteamnum) * myteamnum  # 我以及我下面的人总的折扣数
        team_list = get_model_return_list(self.suser.getuser_by_preid(id)) if self.suser.getuser_by_preid(id) else None
        if team_list:
            for user in team_list:
                num = self.get_myteamsalenum(user['USid'], month)
                myteamnummoney = myteamnummoney - num * self.get_discount_ratio(num)  # 分别减去我的直属代理的总的折扣数
        return myteamnummoney

    def get_myteamsalenum(self, id, month):
        totalpnum = float(get_model_return_dict(self.saccount.get_account_by_month(id, month))['performance']) if self.\
            saccount.get_account_by_month(id, month) else 0
        team_list = self.suser.getuser_by_preid(id)
        if team_list:
            team_list = get_model_return_list(team_list)
            for user in team_list:
                totalpnum = totalpnum + self.get_myteamsalenum(user['USid'], month)
        return totalpnum

    def get_discount_ratio(self, num):  # 获取商品数量对应的奖励金额
        ruler_list = self.rulerlist
        if not ruler_list:
            return 0
        else:
            if num < ruler_list[0]['DRnumber']:
                return 0
            for i in range(0, len(ruler_list)):
                if i < (len(ruler_list) - 1) :
                    if num >= ruler_list[i]['DRnumber'] and num < ruler_list[i+1]['DRnumber']:
                        return ruler_list[i]['DRratio']
                else:
                    return ruler_list[len(ruler_list)-1]['DRratio']

    @verify_token_decorator
    def get_rank_list(self):
        if is_tourist():
            return TOKEN_ERROR
        try:
            data = request.json
            month = str(data.get('month'))
        except:
            return PARAMS_ERROR

        performance_list = self.get_teamperformance_list(request.user.id, month)
        if not performance_list:
            response = import_status("get_performancelist_success", "OK")
            response['data'] = []
            return response
        new_list = sorted(performance_list, key=lambda performance: performance['performance'], reverse=True)
        response = import_status("get_performancelist_success", "OK")
        response['data'] = new_list[:10]
        return response


    def get_teamperformance_list(self, id, month):
        performance_list = []
        self_performance = self.saccount.get_user_performance(id, month)
        if self_performance:
            performance_list = performance_list + (get_model_return_list(self_performance))
        teamid_list = self.suser.getuser_by_preid(id)
        if teamid_list:
            teamid_list = get_model_return_list(teamid_list)
            for user in teamid_list:
                list = self.get_teamperformance_list(user['USid'], month)
                performance_list = performance_list + list
        return performance_list

    @verify_token_decorator
    def get_directagent(self):
        if is_tourist():
            return TOKEN_ERROR
        direct_list = self.suser.getuser_by_preid(request.user.id)
        if direct_list:
            direct_list = get_model_return_list(direct_list)
            all_direct_num = int(len(direct_list))
            distribution_list = self.get_tatal_distribu(request.user.id)
            distribution_num = len(distribution_list)
            response = import_status("get_directagent_list_success", "OK")
            response['data'] = direct_list
            response['directcount'] = all_direct_num
            response['distribucount'] = distribution_num
            return response
        else:
            response = import_status("get_directagent_list_success", "OK")
            response['data'] = []
            return response

    def get_tatal_distribu(self, id):
        total_distribu = []
        team_list = self.suser.getusername_and_id_by_preid(id)
        if not team_list:
            return total_distribu
        else:
            team_list = get_model_return_list(team_list)
            for user in team_list:
                team_list2 = self.suser.getusername_and_id_by_preid(user['USid'])
                if team_list2:
                    team_list2 = get_model_return_list(team_list2)
                    for user2 in team_list2:
                        total_distribu = total_distribu + self.get_direct_include_self(user2['USid'])
        return total_distribu


    def get_direct_include_self(self, id):
        name_list = get_model_return_list(self.suser.get_myself_name(id))
        team_id = self.suser.getuser_by_preid(id)
        if team_id:
            team_id = get_model_return_list(team_id)
            for id in team_id:
                name_list = name_list + self.get_direct_include_self(id['USid'])
        return name_list

    @verify_token_decorator
    def get_distribute(self):
        if is_tourist():
            return TOKEN_ERROR
        distribution_list = self.get_tatal_distribu(request.user.id)
        if distribution_list == []:
            response = import_status("get_distribuagent_list_success", "OK")
            response['data'] = []
            return response
        response = import_status("get_distribuagent_list_success", "OK")
        response['data'] = distribution_list
        return response

    @verify_token_decorator
    def get_draw_info(self):
        if is_tourist():
            return TOKEN_ERROR
        bank = DRAWBANK
        user = get_model_return_dict(self.suser.getuserinfo_by_uid(request.user.id))
        if not user:
            return NOT_FOUND_USER
        response = import_status("get_drawinfo_success", "OK")
        data = {}
        data['bankname'] = bank
        data['username'] = user['USname']
        response['data'] = data
        return response

    @verify_token_decorator
    def draw_money(self):
        if is_tourist():
            return TOKEN_ERROR
        try:
            data = request.json
            bankname = str(data.get('bankname'))
            branchbank = str(data.get('branchbank'))
            accountname = str(data.get('accountname'))
            cardnum = str(data.get('cardnum'))
            amount = str(data.get('amount'))
        except:
            return PARAMS_ERROR
        user = get_model_return_dict(self.smycenter.get_user_basicinfo(request.user.id))
        if not user:
            return NOT_FOUND_USER
        if float(user['USmount']) < float(amount):
            return NO_ENOUGH_MOUNT
        time_now = datetime.strftime(datetime.now(), format_for_db)
        tradenum = datetime.strftime(datetime.now(), format_for_db) + str(random.randint(10000, 100000))
        result = self.saccount.add_drawmoney(str(uuid.uuid4()), request.user.id, bankname, branchbank, accountname, cardnum,\
                                    amount, time_now, tradenum)
        if result:
            update = {}
            update['USmount'] = float(user['USmount']) - float(amount)
            self.smycenter.update_user_by_uid(request.user.id, update)
            response = import_status("drawmoney_success", "OK")
            return response
        else:
            return SYSTEM_ERROR

    @verify_token_decorator
    def get_drawmoney_list(self):
        if is_tourist():
            return TOKEN_ERROR
        try:
            data = request.json
            status = int(data.get('status'))
            if status < 0:
                return PARAMS_ERROR
        except:
            return PARAMS_ERROR
        if status == 0:
            result_list = get_model_return_list(self.saccount.get_all_drawmoney_list(request.user.id))
            count0 = len(result_list)
            count1 = len(get_model_return_list(self.saccount.get_drawmoney_list(request.user.id, 1)))
            count2 = len(get_model_return_list(self.saccount.get_drawmoney_list(request.user.id, 2)))
            count3 = len(get_model_return_list(self.saccount.get_drawmoney_list(request.user.id, 3)))
            count4 = len(get_model_return_list(self.saccount.get_drawmoney_list(request.user.id, 4)))
            from common.timeformat import get_web_time_str
            for result in result_list:
                result['DMcreatetime'] = get_web_time_str(result['DMcreatetime'])
            response = import_status("get_drawmoneylist_success", "OK")
            response['data'] = result_list
            response['count0'] = count0
            response['count1'] = count1
            response['count2'] = count2
            response['count3'] = count3
            response['count4'] = count4
            return response
        else:
            result_list = get_model_return_list(self.saccount.get_drawmoney_list(request.user.id, status))
            from common.timeformat import get_web_time_str
            for result in result_list:
                result['DMcreatetime'] = get_web_time_str(result['DMcreatetime'])
            response = import_status("get_drawmoneylist_success", "OK")
            response['data'] = result_list
            return response

    @verify_token_decorator
    def charge_monney(self):
        if is_tourist():
            return TOKEN_ERROR
        params_list = ['paytype', 'alipaynum', 'bankname', 'accountname', 'cardnum', 'amount', 'remark', 'proof', 'paytime']
        try:
            data = request.json
            for param in params_list:
                if param not in params_list:
                    PARAMS_ERROR = {
                        "param": param,
                        "status": 405,
                        "status_code": 405002,
                        "message": u"参数错误"
                    }
                    return PARAMS_ERROR
            paytype = int(data.get('paytype'))
            alipaynum = data.get('alipaynum')
            bankname = str(data.get('bankname'))
            accountname = str(data.get('accountname'))
            cardnum = data.get('cardnum')
            amount = int(data.get('amount'))
            remark = str(data.get('remark'))
            proof = str(data.get('proof'))
            paytime = str(data.get('paytime'))
        except:
            from config.response import PARAMS_ERROR
            return PARAMS_ERROR

        createtime = datetime.strftime(datetime.now(), format_for_db)
        tradenum = datetime.strftime(datetime.now(), format_for_db) + str(random.randint(10000, 100000))
        result = self.saccount.charge_money(str(uuid.uuid4()), request.user.id, paytype, alipaynum, bankname, accountname, \
                                            cardnum, amount, remark, tradenum, createtime, proof, paytime)
        if not result:
            return SYSTEM_ERROR
        response = import_status("charge_money_success", "OK")
        return response


    @verify_token_decorator
    def get_chargemoney_list(self):
            if is_tourist():
                return TOKEN_ERROR
            try:
                data = request.json
                status = int(data.get('status'))
                if status < 0:
                    return PARAMS_ERROR
            except:
                return PARAMS_ERROR
            if status == 0:
                result_list = get_model_return_list(self.saccount.get_all_chargemoney_list(request.user.id))
                count0 = len(result_list)
                count1 = len(get_model_return_list(self.saccount.get_chargemoney_list(request.user.id, 1)))
                count2 = len(get_model_return_list(self.saccount.get_chargemoney_list(request.user.id, 2)))
                count3 = len(get_model_return_list(self.saccount.get_chargemoney_list(request.user.id, 3)))
                from common.timeformat import get_web_time_str, format_forweb_no_HMS
                for result in result_list:
                    result['CMcreatetime'] = get_web_time_str(result['CMcreatetime'])
                    result['CMpaytime'] = get_web_time_str(result['CMpaytime'], formattype=format_forweb_no_HMS)
                response = import_status("get_chargemoneylist_success", "OK")
                response['data'] = result_list
                response['count0'] = count0
                response['count1'] = count1
                response['count2'] = count2
                response['count3'] = count3
                return response
            else:
                result_list = get_model_return_list(self.saccount.get_chargemoney_list(request.user.id, status))
                from common.timeformat import get_web_time_str
                for result in result_list:
                    result['CMcreatetime'] = get_web_time_str(result['CMcreatetime'])
                response = import_status("get_chargemoneylist_success", "OK")
                response['data'] = result_list
                return response