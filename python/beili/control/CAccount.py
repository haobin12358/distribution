# *- coding:utf8 *-
import re
import sys
import os
import uuid
import random
from flask import request
# import logging
from config.response import PARAMS_MISS, SYSTEM_ERROR, PARAMS_ERROR, TOKEN_ERROR, AUTHORITY_ERROR, STOCK_NOT_ENOUGH,\
        NO_ENOUGH_MOUNT, NO_BAIL, NO_ADDRESS, NOT_FOUND_USER, NOT_FOUND_OPENID, NOT_FOUND_RECORD, MONEY_ERROR
from config.setting import QRCODEHOSTNAME, DRAWBANK, BAIL, APP_ID, MCH_ID, MCH_KEY, notify_url
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
from config.urlconfig import get_code
import platform
from common.beili_error import stockerror, dberror
from datetime import datetime
from weixin import WeixinError
from weixin.login import WeixinLoginError, WeixinLogin
from weixin.pay import WeixinPay, WeixinPayError
from common.timeformat import format_for_db, get_random_str
from models.model import User, AgentMessage, BailRecord
sys.path.append(os.path.dirname(os.getcwd()))


class CAccount():

    def __init__(self):
        self.suser = SUser()
        self.sorder = SOrder()
        self.sgoods = SGoods()
        self.smycenter = SMyCenter()
        self.smessage = SMessage()
        self.saccount = SAccount()
        self.pay = WeixinPay(APP_ID, MCH_ID, MCH_KEY, notify_url)
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
    def get_rank_list(self):  # 获取业绩列表
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


    def get_teamperformance_list(self, id, month):  # 获取包含自己的团队所有人业绩
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
            amount = int(data.get('amount'))
        except:
            return PARAMS_ERROR
        user = get_model_return_dict(self.smycenter.get_user_basicinfo(request.user.id))
        if not user:
            return NOT_FOUND_USER
        if float(user['USmount']) < float(amount):
            return NO_ENOUGH_MOUNT
        time_now = datetime.strftime(datetime.now(), format_for_db)
        tradenum = 'tx' + datetime.strftime(datetime.now(), format_for_db) + str(random.randint(10000, 100000))
        result = self.saccount.add_drawmoney(str(uuid.uuid4()), request.user.id, bankname, branchbank, accountname, cardnum,\
                                    float(amount), time_now, tradenum)
        result2 = self.saccount.add_moneyrecord(request.user.id, -amount, 2, time_now, tradenum=tradenum, oiid=None)
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

    @verify_token_decorator
    def check_bail(self):
        if is_tourist():
            return TOKEN_ERROR
        system_bail = BAIL
        userinfo = get_model_return_dict(self.smycenter.get_user_basicinfo(request.user.id))
        if not userinfo:
            return SYSTEM_ERROR
        record = self.saccount.get_bail_record(request.user.id, 2)
        if record:
            response = import_status("check_bail_success", "OK")
            response['bailstatus'] = 3  # 退还中
        if userinfo['USbail'] < system_bail:
            response = import_status("check_bail_success", "OK")
            response['bailstatus'] = 2  # 未充值
            shouldpay = system_bail - userinfo['USbail']
            data = {}
            data['shouldpay'] = shouldpay
            response['data'] = data
        else:
            response = import_status("check_bail_success", "OK")
            response['bailstatus'] = 1  # 已充值
        return response


    @verify_token_decorator
    def charge_draw_bail(self):  # 充值和提取保证金
        if is_tourist():
            return TOKEN_ERROR
        try:
            data = request.json
            type = int(data.get('type'))
            mount = int(data.get('mount'))
        except:
            return PARAMS_ERROR
        user = get_model_return_dict(self.smycenter.get_user_basicinfo(request.user.id))
        if not user:
            return SYSTEM_ERROR
        session = db_session()
        try:
            if type == 1:
                if user['USmount'] < mount:
                    return NO_ENOUGH_MOUNT
                bail_now = user['USbail']
                update_mount = {}
                update_mount['USmount'] = user['USmount'] - mount
                session.query(User).filter(User.USid == request.user.id).update(update_mount)

                update_bail = {}
                update_bail['USbail'] = bail_now + mount
                session.query(User).filter(User.USid == request.user.id).update(update_bail)


                record = BailRecord()
                tradenum = 'bz' + datetime.strftime(datetime.now(), format_for_db) + str(random.randint(10000, 100000))
                record.BRid = str(uuid.uuid4())
                record.USid = request.user.id
                record.BRmount = mount
                record.BRtype = 1
                record.BRstatus = 1
                record.BRtradenum = tradenum
                record.BRcreatetime = datetime.strftime(datetime.now(), format_for_db)
                session.add(record)

                time_now = datetime.strftime(datetime.now(), format_for_db)
                result2 = self.saccount.add_moneyrecord(request.user.id, -mount, 3, time_now
                                                        , tradenum=tradenum, oiid=None)

                session.commit()
                response = import_status("charge_bail_success", "OK")
                return response
            if type == 2:
                update_bail = {}
                update_bail['USbail'] = (user['USbail'] - mount) if (user['USbail'] - mount) >= 0 else 0
                session.query(User).filter(User.USid == request.user.id).update(update_bail)
                record = BailRecord()
                record.BRid = str(uuid.uuid4())
                record.USid = request.user.id
                record.BRmount = mount
                record.BRtype = 2
                record.BRstatus = 2
                record.BRtradenum = 'bz' + datetime.strftime(datetime.now(), format_for_db) + str(random.randint(10000, 100000))
                record.BRcreatetime = datetime.strftime(datetime.now(), format_for_db)
                session.add(record)
                session.commit()
                response = import_status("draw_bail_success", "OK")
                return response
        except Exception as e:
            print e
            session.rollback()
            return SYSTEM_ERROR
        finally:
            session.close()

    @verify_token_decorator
    def get_alluser_account(self):
        if not is_admin():
            return AUTHORITY_ERROR
        try:
            data = request.json
            username = data.get('username')
            userphonenum = data.get('userphonenum')
            month = data.get('month')
            status = data.get('status')
            agentid = data.get('agentid')
            page_size = data.get('page_size')
            page_num = data.get('page_num')
        except:
            return PARAMS_ERROR
        this_month = str(datetime.strftime(datetime.now(), format_for_db))[0:6]
        if month > this_month:
            response = {}
            response['data'] = []
            response['message'] = import_status("get_alluser_account_success", "OK")
            return response
        all_list = get_model_return_list(self.saccount.get_alluser_account(username, month, agentid, status))
        if not all_list:
            response = import_status("get_alluser_account_success", "OK")
            response['data'] = []
            return response
        real_list = []
        if userphonenum:
            for user in all_list:
                phonenum = get_model_return_dict(self.smycenter.get_user_basicinfo(user['USid']))['USphonenum']
                if userphonenum in phonenum:
                    real_list.append(user)
        else:
            real_list = all_list
        if month == this_month:
            for real in real_list:
                real['AMstatus'] = 3
        for real in real_list:
            phonenum = get_model_return_dict(self.smycenter.get_user_basicinfo(real['USid']))['USphonenum']
            real['userphonenum'] = phonenum
            real['discount'] = self.get_mydiscount(real['USid'], month)
            real['teamperformance'] = self.get_myteamsalenum(real['USid'], month)
            real['myprofit'] = real['discount'] + real['reward']

        mount = len(real_list)
        page = mount / page_size
        if page == 0 or page == 1 and mount % page_size == 0:
            real_return_list = real_list[0:]
        else:
            if ((mount - (page_num - 1) * page_size) / page_size) >= 1 and \
                    (mount - (page_num * page_size)) > 0:
                real_return_list = real_list[((page_num - 1) * page_size):(page_num * page_size)]
            else:
                real_return_list = real_list[((page_num - 1) * page_size):]

        response = import_status("get_alluser_account_success", "OK")
        response['data'] = real_return_list
        response['mount'] = mount
        return response

    @verify_token_decorator
    def deal_reward_discount(self):
        if not is_admin():
            return AUTHORITY_ERROR
        try:
            data = request.json
            amid = data.get('amid')
            usid = data.get('usid')
            month = str(data.get('month'))
            profit = data.get('profit')
        except:
            return PARAMS_ERROR
        account = get_model_return_dict(
            self.saccount.get_account_by_month(usid, month)) if self.saccount.get_account_by_month(id, month) else None
        if not account or account['AMid'] != amid or account['AMstatus'] != 1:
            return NOT_FOUND_RECORD
        mydiscount = self.get_mydiscount(id, month)
        reward = account['reward']
        if profit != mydiscount + reward:
            return MONEY_ERROR
        update = {}
        update["AMstatus"] = 2
        result = self.saccount.update_account(amid)
        if not result:
            return SYSTEM_ERROR
        tradenum = get_random_str(5) + datetime.strftime(datetime.now(), format_for_db)
        time_now = datetime.strftime(datetime.now(), format_for_db)
        result2 = self.saccount.add_moneyrecord(usid, profit, 5, time_now
                                                , tradenum=tradenum, oiid=None)
        if not result2:
            return SYSTEM_ERROR
        user = get_model_return_dict(self.smycenter.get_user_basicinfo(usid)) if \
            self.smycenter.get_user_basicinfo(usid) else None
        update = {}
        update['USmount'] = user['USmount'] + profit
        self.smycenter.update_user_by_uid(usid, update)
        response = import_status("deal_profit_success", "OK")
        return response


    @verify_token_decorator
    def get_directagent_performance(self):
        if not is_admin():
            return AUTHORITY_ERROR
        try:
            data = request.json
            usid = data.get('usid')
            month = data.get('month')
        except:
            return PARAMS_ERROR
        direct_list = self.suser.getuser_by_preid(usid)
        if direct_list:
            direct_list = get_model_return_list(direct_list)
            for direct in direct_list:
                teamperformance = self.get_myteamsalenum(direct['USid'], month)
                direct['teamperformance'] = teamperformance
                reward = self.saccount.get_reward_by_nextid(direct['USid'])
                if reward:
                    direct['reward'] = get_model_return_dict(self.saccount.get_reward_by_nextid(direct['USid']))['REmount'] if \
                        self.saccount.get_reward_by_nextid(direct['USid']) else None
            all_direct_num = int(len(direct_list))
            response = import_status("get_directagent_and_performance_list_success", "OK")
            response['data'] = direct_list
            response['directcount'] = all_direct_num
            return response
        else:
            response = import_status("get_directagent_and_performance_list_success", "OK")
            response['data'] = []
            return response

    @verify_token_decorator
    def get_moneyrecord(self):
        if is_tourist():
            return TOKEN_ERROR
        usid = request.user.id
        records = get_model_return_list(self.saccount.get_moneyrecord(usid)) if self.saccount.get_moneyrecord(usid) else None
        if not records:
            response = import_status("get_moneyrecord_success", "OK")
            response['data'] = []
            return response
        for record in records:
            from common.timeformat import get_web_time_str
            record['MRcreatetime'] = get_web_time_str(record['MRcreatetime'])
        response = import_status("get_moneyrecord_success", "OK")
        response['data'] = records
        return response

    @verify_token_decorator
    def get_all_performance(self):  # 获取业绩列表
        if not is_admin():
            return TOKEN_ERROR
        try:
            data = request.json
            month = str(data.get('month'))
            usid = data.get('usid')
        except:
            return PARAMS_ERROR
        performance_list = self.get_teamperformance_list(usid, month)
        if not performance_list:
            response = import_status("get_performancelist_success", "OK")
            response['data'] = []
            return response
        new_list = sorted(performance_list, key=lambda performance: performance['performance'], reverse=True)
        response = import_status("get_performancelist_success", "OK")
        response['data'] = new_list
        return response

    @verify_token_decorator
    def get_alluser_drawmoney_list(self):
        if not is_admin():
            return TOKEN_ERROR
        try:
            data = request.json
            status = data.get("status")
            page_size = data.get('page_size')
            page_num = data.get('page_num')
        except:
            return PARAMS_ERROR
        list = get_model_return_list(self.saccount.get_alluser_drawmoney_list(status)) if\
                self.saccount.get_alluser_drawmoney_list(status) else None
        if not list:
            response = import_status("get_drawmoneylist_success", "OK")
            response['data'] = []
            return response
        for record in list:
            from common.timeformat import get_web_time_str
            record['DMcreatetime'] = get_web_time_str(record['DMcreatetime'])

        mount = len(list)
        page = mount / page_size
        if page == 0 or page == 1 and mount % page_size == 0:
            real_return_list = list[0:]
        else:
            if ((mount - (page_num - 1) * page_size) / page_size) >= 1 and \
                    (mount - (page_num * page_size)) > 0:
                real_return_list = list[((page_num - 1) * page_size):(page_num * page_size)]
            else:
                real_return_list = list[((page_num - 1) * page_size):]
        response = import_status("get_drawmoneylist_success", "OK")
        response['mount'] = mount
        response['data'] = real_return_list
        return response




    @verify_token_decorator
    def deal_drawmoney(self):   # 处理提现操作
        if not is_admin():
            return TOKEN_ERROR
        try:
            data = request.json
            willstatus = int(data.get("willstatus"))
            dmid = data.get("dmid")
        except:
            return PARAMS_ERROR
        result = get_model_return_dict(self.saccount.get_drawmoney_info(dmid)) if self.saccount.get_drawmoney_info(dmid) else None
        if not result:
            return NOT_FOUND_RECORD
        update = {}
        update['DMstatus'] = willstatus
        update_result = self.saccount.update_by_dmid(dmid, update)
        if not update_result:
            return SYSTEM_ERROR
        if willstatus == 4:
            time_now = datetime.strftime(datetime.now(), format_for_db)
            result2 = self.saccount.add_moneyrecord(result['USid'], result['DMamount'], 7, time_now
                                                   , tradenum=result['DMtradenum'], oiid=None)
            user = get_model_return_dict(self.smycenter.get_user_basicinfo(result['USid'])) if \
                self.smycenter.get_user_basicinfo(result['USid']) else None
            update = {}
            update['USmount'] = user['USmount'] + result['DMamount']
            self.smycenter.update_user_by_uid(result['USid'], update)
        response = import_status("update_record_success", "OK")
        return response

    @verify_token_decorator
    def get_all_chargemoney(self):
        if not is_admin():
            return TOKEN_ERROR
        try:
            data = request.json
            status = int(data.get('status'))
            page_size = data.get('page_size')
            page_num = data.get('page_num')
        except:
            return PARAMS_ERROR
        result = get_model_return_list(self.saccount.get_alluser_chargemoney(status)) if self.saccount\
                .get_alluser_chargemoney(status) else None
        if not result:
            response = import_status("get_chargemoneylist_success", "OK")
            response['data'] = []
            return response
        for record in result:
            from common.timeformat import get_web_time_str, format_forweb_no_HMS
            record['CMproof'] = record['CMproof'].split(',')
            record['CMcreatetime'] = get_web_time_str(record['CMcreatetime'])
            record['CMpaytime'] = get_web_time_str(record['CMpaytime'], format_forweb_no_HMS)

        mount = len(result)
        page = mount / page_size
        if page == 0 or page == 1 and mount % page_size == 0:
            real_return_list = result[0:]
        else:
            if ((mount - (page_num - 1) * page_size) / page_size) >= 1 and \
                    (mount - (page_num * page_size)) > 0:
                real_return_list = result[((page_num - 1) * page_size):(page_num * page_size)]
            else:
                real_return_list = result[((page_num - 1) * page_size):]

        response = import_status("get_chargemoneylist_success", "OK")
        response['data'] = real_return_list
        response['mount'] = mount
        return response

    @verify_token_decorator
    def deal_chargemoney(self):  # 处理充值申请
        if not is_admin():
            return TOKEN_ERROR
        try:
            data = request.json
            willstatus = int(data.get("willstatus"))
            cmid = data.get("cmid")
        except:
            return PARAMS_ERROR
        result = get_model_return_dict(self.saccount.get_chargemoney_info(cmid)) if self.saccount.get_chargemoney_info(
            cmid) else None
        if not result:
            return NOT_FOUND_RECORD
        update = {}
        update['CMstatus'] = willstatus
        update_result = self.saccount.update_by_cmid(cmid, update)
        if not update_result:
            return SYSTEM_ERROR
        if willstatus == 2:
            time_now = datetime.strftime(datetime.now(), format_for_db)
            self.saccount.add_moneyrecord(result['USid'], result['CMamount'], 4, time_now
                                                    , tradenum=result['CMtradenum'], oiid=None)
            user = get_model_return_dict(self.smycenter.get_user_basicinfo(result['USid'])) if \
                self.smycenter.get_user_basicinfo(result['USid']) else None
            update = {}
            update['USmount'] = user['USmount'] + result['CMamount']
            self.smycenter.update_user_by_uid(result['USid'], update)
        response = import_status("update_record_success", "OK")
        return response

    @verify_token_decorator
    def get_alluser_bailrecord(self):  # 获取所有保证金列表
        if not is_admin():
            return TOKEN_ERROR
        try:
            data = request.json
            status = int(data.get('status'))
            page_size = data.get('page_size')
            page_num = data.get('page_num')
        except:
            return PARAMS_ERROR
        result = get_model_return_list(self.saccount.get_alluser_bailrecord(status)) if self.saccount\
            .get_alluser_bailrecord(status) else None
        if not result:
            return NOT_FOUND_RECORD
        if not result:
            response = import_status("get_bailrecordlist_success", "OK")
            response['data'] = []
            return response
        for record in result:
            from common.timeformat import get_web_time_str
            record['BRcreatetime'] = get_web_time_str(record['BRcreatetime'])
        mount = len(result)
        page = mount / page_size
        if page == 0 or page == 1 and mount % page_size == 0:
            real_return_list = result[0:]
        else:
            if ((mount - (page_num - 1) * page_size) / page_size) >= 1 and \
                    (mount - (page_num * page_size)) > 0:
                real_return_list = result[((page_num - 1) * page_size):(page_num * page_size)]
            else:
                real_return_list = result[((page_num - 1) * page_size):]
        response = import_status("get_bailrecordlist_success", "OK")
        response['data'] = real_return_list
        response['mount'] = mount
        return response

    @verify_token_decorator
    def deal_bailrecord(self):  # 处理保证金申请
        if not is_admin():
            return TOKEN_ERROR
        try:
            data = request.json
            willstatus = int(data.get("willstatus"))
            brid = data.get("brid")
        except:
            return PARAMS_ERROR
        result = get_model_return_dict(self.saccount.get_bailrecord_info(brid)) if self.saccount.get_bailrecord_info(
            brid) else None
        if not result:
            return NOT_FOUND_RECORD
        update = {}
        update['BRstatus'] = willstatus
        result2 = self.saccount.update_bailrecord(brid, update)
        if not result2:
            return SYSTEM_ERROR
        if willstatus == 3:
            time_now = datetime.strftime(datetime.now(), format_for_db)
            self.saccount.add_moneyrecord(result['USid'], result['BRmount'], 6, time_now
                                          , tradenum=result['BRtradenum'], oiid=None)
            user = get_model_return_dict(self.smycenter.get_user_basicinfo(result['USid'])) if \
                self.smycenter.get_user_basicinfo(result['USid']) else None
            update = {}
            update['USmount'] = user['USmount'] + result['BRmount']
            self.smycenter.update_user_by_uid(result['USid'], update)
        if willstatus == 4:
            user = get_model_return_dict(self.smycenter.get_user_basicinfo(result['USid'])) if \
                self.smycenter.get_user_basicinfo(result['USid']) else None
            update_bail = {}
            update_bail['USbail'] = user['USbail'] + result['BRmount']
            self.smycenter.update_user_by_uid(result['USid'], update_bail)
        response = import_status("update_record_success", "OK")
        return response





    @verify_token_decorator
    def weixin_pay(self):
        if is_tourist():
            raise TOKEN_ERROR()
        try:
            data = request.json
            amount = data.get('amount')
        except:
            return PARAMS_ERROR
        wcsn = 'cz' + datetime.strftime(datetime.now(), format_for_db)  # 充值号
        user = get_model_return_dict(self.smycenter.get_user_basicinfo(request.user.id))
        if not user:
            return NOT_FOUND_USER
        openid = user['openid']
        if not openid:
            return NOT_FOUND_OPENID
        result = self.saccount.create_weixin_charge(request.user.id, openid, wcsn, amount)
        if not result:
            return SYSTEM_ERROR
        total_fee = 1
        raw = self.pay.jsapi(trade_type="JSAPI", openid=openid,
                             out_trade_no=wcsn,
                             total_fee=int(total_fee),
                             spbill_create_ip=request.remote_addr,
                             body='1234')
        res = dict(raw)
        print res
        res['paySign'] = res.get('sign')
        data = import_status('get_prepay_message_ok', 'OK')
        data['data'] = res
        return data

    @verify_token_decorator
    def pay_callback(self):
        data = self.pay.to_dict(request.data)
        if not self.pay.check(data):
            return self.pay.reply(u"签名验证失败", False)
        print data
        result = data.get('return_code')
        if str(result) != 'SUCCESS':
            update = {}
            update
        wcsn = data.get('out_trade_no')
        record = get_model_return_dict(self.saccount.get_record_by_wcsn(wcsn)) if self.saccount.get_record_by_wcsn(wcsn) else None
        if not record or record['WCstatus'] != 1:
            # 无效请求
            return self.pay.reply("OK", True)
        # 修改记录状态
        update = {}
        update['WCstatus'] = 1
        paytime = data.get('time_end')
        update_dict = {
            'OIpaystatus': 5,  # 待发货
            'OIpaytime': paytime,
            'OIpaytype': 1,  # 统一微信支付
        }
        # 如果存在上一级
