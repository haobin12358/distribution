# *- coding:utf8 *-
import re
import sys
import os
import uuid
import random
from flask import request
# import logging
from config.response import PARAMS_MISS, SYSTEM_ERROR, PARAMS_ERROR, TOKEN_ERROR, AUTHORITY_ERROR, STOCK_NOT_ENOUGH,\
        NO_ENOUGH_MOUNT, NO_BAIL, NO_ADDRESS
from config.setting import QRCODEHOSTNAME
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
            response['data'] = []
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
        try:
            data = request.json
            page = int(data.get('page'))
            count = int(data.get('count'))
        except:
            return PARAMS_ERROR
        direct_list = self.suser.getusername_by_preid(request.user.id, page, count)
        if direct_list:
            direct_list = get_model_return_list(direct_list)
            all_direct_num = int(self.suser.get_totaldirect(request.user.id))
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
        try:
            data = request.json
            page = int(data.get('page'))
            count = int(data.get('count'))
        except:
            return PARAMS_ERROR
        distribution_list = self.get_tatal_distribu(request.user.id)
        if distribution_list == []:
            response = import_status("get_distribuagent_list_success", "OK")
            response['data'] = []
            return response
        mount = len(distribution_list)
        page2 = mount / page
        if page2 == 0 or page2 == 1 and mount % count == 0:
            return_list = distribution_list[0:]
        else:
            if ((mount - (page - 1) * count) / page) >= 1 and \
                    ((mount - (page - 1) * count) % page) > 0:
                return_list = distribution_list[((page - 1) * count):(count * page)]
            else:
                return_list = distribution_list[((page - 1) * count):]

        response = import_status("get_distribuagent_list_success", "OK")
        response['data'] = return_list
        return response