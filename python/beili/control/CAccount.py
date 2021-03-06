# *- coding:utf8 *-
import re
import sys
import os
import uuid
import random
from flask import request
# import logging
from config.response import PARAMS_MISS, SYSTEM_ERROR, PARAMS_ERROR, TOKEN_ERROR, AUTHORITY_ERROR, STOCK_NOT_ENOUGH,\
        NO_ENOUGH_MOUNT, NO_BAIL, NO_ADDRESS, NOT_FOUND_USER, NOT_FOUND_OPENID, NOT_FOUND_RECORD, MONEY_ERROR, REPERT_NUMBER
from config.setting import QRCODEHOSTNAME, APP_ID, MCH_ID, MCH_KEY, notify_url
from common.token_required import verify_token_decorator, usid_to_token, is_tourist, is_admin
from common.import_status import import_status
#from config.setting import QRCODEHOSTNAME, ALIPAYNUM, ALIPAYNAME, WECHAT, BANKNAME, COUNTNAME, CARDNUM, MONEY, BAIL, \
 #   WECHATSERVICE, REWARD, REDIRECT_URI, APP_ID, APP_SECRET, SERVER, CHARGEBANKNAME
from common.timeformat import get_db_time_str, get_web_time_str
from common.get_model_return_list import get_model_return_list, get_model_return_dict
from service.SUser import SUser
from service.SMessage import SMessage
from service.SOrder import SOrder
from service.SGoods import SGoods
from service.SMyCenter import SMyCenter
from service.DBSession import db_session
from service.SAccount import SAccount
import threading
from configparser import ConfigParser
from config.urlconfig import get_code
import platform
from configparser import ConfigParser
from common.beili_error import stockerror, dberror
from datetime import datetime, date, timedelta
from weixin import WeixinError
from weixin.login import WeixinLoginError, WeixinLogin
from weixin.pay import WeixinPay, WeixinPayError
from common.timeformat import format_for_db, get_random_str, format_for_db_no_HMS, get_random_int\
    , format_forweb_no_HMS, format_for_dbmonth
from models.model import User, DiscountRuler, BailRecord, DrawMoney, ChargeMoney, Amount
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
        self.conf = ConfigParser()
        self.conf.read('config/setting.ini')

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
        data2 = {}
        if not account:
            data2["reward"] = 0
        else:
            data2["reward"] = round(account['reward'], 2)
        mydiscount = self.get_mydiscount(id, month)
        teamperformance = self.get_myteamsalenum(id, month)
        response = import_status("get_saleinfo_success", "OK")
        data2["discount"] = round(mydiscount, 2)
        data2["performance"] = round(teamperformance, 2)
        data2["myprofit"] = data2["reward"] + round(mydiscount, 2)
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
        ruler_list = get_model_return_list(self.saccount.get_discount_ruler())
        if not ruler_list:
            return 0
        else:
            if num < ruler_list[0]['DRnumber']:
                return 0
            for i in range(0, len(ruler_list)):
                if i < (len(ruler_list) - 1) :
                    if num >= ruler_list[i]['DRnumber'] and num < ruler_list[i+1]['DRnumber']:
                        return ruler_list[i]['DRmoney']
                else:
                    return ruler_list[len(ruler_list)-1]['DRmoney']

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
            self_performance = get_model_return_list(self_performance)
            self_performance[0]['performance'] = round(self_performance[0]['performance'], 2)
            performance_list = performance_list + self_performance
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
            args = request.args.to_dict()
            page_num = int(args.get("page_num"))
            page_size = int(args.get("page_size"))
        except:
            page_num = page_size = None
            print 'no params'
        direct_list = self.suser.getuser_by_preid(request.user.id)
        if direct_list:
            direct_list = get_model_return_list(direct_list)
            all_direct_num = int(len(direct_list))
            distribution_list = self.get_tatal_distribu(request.user.id)
            distribution_num = len(distribution_list)

            if page_num and page_size:
                mount = len(direct_list)
                page = mount / page_size
                if page == 0 or page == 1 and mount % page_size == 0:
                    return_list = direct_list[0:]
                else:
                    if ((mount - (page_num - 1) * page_size) / page_size) >= 1 and \
                            (mount - (page_num * page_size)) > 0:
                        return_list = direct_list[((page_num - 1) * page_size):(page_num * page_size)]
                    else:
                        return_list = direct_list[((page_num - 1) * page_size):]

                response = import_status("get_directagent_list_success", "OK")
                response['data'] = return_list
                response['directcount'] = all_direct_num
                response['distribucount'] = distribution_num
                return response
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
    def get_distribute(self):  # 获取所有分销商
        if is_tourist():
            return TOKEN_ERROR
        try:
            args = request.args.to_dict()
            page_num = int(args.get("page_num"))
            page_size = int(args.get("page_size"))
        except:
            page_num = page_size = None
            print 'no params'
        distribution_list = self.get_tatal_distribu(request.user.id)
        if distribution_list == []:
            response = import_status("get_distribuagent_list_success", "OK")
            response['data'] = []
            return response
        if page_num and page_size:
            mount = len(distribution_list)
            page = mount / page_size
            if page == 0 or page == 1 and mount % page_size == 0:
                return_list = distribution_list[0:]
            else:
                if ((mount - (page_num - 1) * page_size) / page_size) >= 1 and \
                        (mount - (page_num * page_size)) > 0:
                    return_list = distribution_list[((page_num - 1) * page_size):(page_num * page_size)]
                else:
                    return_list = distribution_list[((page_num - 1) * page_size):]

            response = import_status("get_distribuagent_list_success", "OK")
            response['data'] = return_list
            return response
        response = import_status("get_distribuagent_list_success", "OK")
        response['data'] = distribution_list
        return response

    @verify_token_decorator
    def get_draw_info(self):
        if is_tourist():
            return TOKEN_ERROR
        bank = self.conf.get('account', 'drawbank')
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
    def draw_money(self):  # 提现
        if is_tourist():
            return TOKEN_ERROR
        try:
            data = request.json
            bankname = str(data.get('bankname'))
            branchbank = str(data.get('branchbank'))
            accountname = str(data.get('accountname'))
            cardnum = str(data.get('cardnum'))
            amount = float(data.get('amount'))
        except:
            return PARAMS_ERROR
        user = get_model_return_dict(self.smycenter.get_user_basicinfo(request.user.id))
        if not user:
            return NOT_FOUND_USER
        if user['USmount'] < round(amount, 2):
            return NO_ENOUGH_MOUNT
        session = db_session()
        try:
            time_now = datetime.strftime(datetime.now(), format_for_db)
            tradenum = 'tx' + datetime.strftime(datetime.now(), format_for_db) + str(random.randint(10000, 100000))
            result = self.saccount.add_drawmoney(session, str(uuid.uuid4()), request.user.id, bankname, branchbank, accountname, cardnum, \
                                        round(amount, 2), time_now, tradenum)
            result2 = self.saccount.add_moneyrecord(session, request.user.id, -amount, 2, time_now, tradenum=tradenum, oiid=None)
            update = {}
            update['USmount'] = round(user['USmount'] - round(amount, 2), 2)
            self.smycenter.update_user_by_uid(session, request.user.id, update)
            session.commit()
        except Exception as e:
            print e
            session.rollback()
            return SYSTEM_ERROR
        finally:
            session.close()
        response = import_status("drawmoney_success", "OK")
        return response

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
                if param not in data:
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
            amount = float(data.get('amount'))
            remark = str(data.get('remark'))
            proof = str(data.get('proof'))
            paytime = str(data.get('paytime'))
        except:
            from config.response import PARAMS_ERROR
            return PARAMS_ERROR

        createtime = datetime.strftime(datetime.now(), format_for_db)
        tradenum = 'cz' + datetime.strftime(datetime.now(), format_for_db) + str(random.randint(10000, 100000))
        result = self.saccount.charge_money(str(uuid.uuid4()), request.user.id, paytype, alipaynum, bankname, accountname, \
                                            cardnum, round(amount, 2), remark, tradenum, createtime, proof, paytime)
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
        system_bail = float(self.conf.get('account', 'bail'))
        userinfo = get_model_return_dict(self.smycenter.get_user_basicinfo(request.user.id))
        if not userinfo:
            return SYSTEM_ERROR
        record = self.saccount.get_bail_record(request.user.id, 2)
        if record:
            response = import_status("check_bail_success", "OK")
            response['bailstatus'] = 3  # 退还中
            return response
        if float(userinfo['USbail']) < system_bail :
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
            mount = float(data.get('mount'))
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
                result2 = self.saccount.add_moneyrecord(session, request.user.id, -mount, 3, time_now
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
            real['discount'] = round(self.get_mydiscount(real['USid'], month), 2)
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

    def deal_reward_discount(self):  # 发放奖金
        import datetime
        time_now = datetime.datetime.now().strftime("%Y%m%d%H%M%S")
        print time_now
        global TIMER
        print 'check reward and discount'
        if time_now[6:10] == '0101' or time_now[6:10] == '0102' or time_now[6:10] == '0103':
            print 'start deal reward and discount'
            last_month = (datetime.datetime.now() - datetime.timedelta(days=1)).strftime("%Y%m")
            print last_month

            # 将没有在金额表里的用户插入一条数据
            session = db_session()
            try:
                all_user_list = get_model_return_list(self.suser.get_all_user_info())
                print 'len(all_user_list)', len(all_user_list)
                usid_list = []
                account_list2 = get_model_return_list(self.saccount.get_all_account_by_month2(last_month))
                for account in account_list2:
                    usid_list.append(account['USid'])
                print 'len(usid_list)', len(usid_list)
                if len(usid_list) != len(all_user_list):
                    for user in all_user_list:
                        if user['USid'] not in usid_list:
                            print '2222222'
                            amount = Amount()
                            amount.USid = user['USid']
                            amount.AMid = str(uuid.uuid4())
                            amount.USagentid = user['USagentid']
                            amount.USname = user['USname']
                            amount.reward = 0
                            amount.AMstatus = 1
                            amount.USheadimg = user['USheadimg']
                            amount.AMcreattime = datetime.datetime.strftime(datetime.datetime.now(), format_for_db)
                            amount.AMmonth = last_month
                            session.add(amount)
                    session.commit()
            except Exception as e:
                print '3333333', e
                session.rollback()
            finally:
                session.close()

            account_list = get_model_return_list(self.saccount.get_all_account_by_month(last_month))
            if account_list:
                result = self.deal_account_list(account_list, last_month)
                if not result:
                    print 'deal_profit_fail'
                else:
                    print 'deal_profit_success'
            print 'end deal reward and discount'
        print(u'当前线程数为{}'.format(threading.activeCount()))
        TIMER = threading.Timer(3600, self.deal_reward_discount)
        TIMER.setDaemon(True)
        TIMER.start()

    def deal_account_list(self, account_list, last_month):


        time_now = datetime.strftime(datetime.now(), format_for_db)
        for account in account_list:
            session = db_session()
            try:
                mydiscount = self.get_mydiscount(account['USid'], last_month)
                # 写入代理消息
                tradenum = datetime.strftime(datetime.now(), format_for_db_no_HMS) + get_random_str(8)
                content = u'您' + last_month + u'月的销售折扣返点已发放，金额为' + str(round(mydiscount, 2)) \
                          + '，流水号为' + ' ' + str(tradenum)
                agent_result = self.smessage.create_agentmessage(session, account['USid'], time_now, content, 1)
                if not agent_result:
                    raise dberror
                # 更改数据表状态
                update = {}
                update["AMstatus"] = 2
                update['AMtradenum'] = tradenum
                result = self.saccount.update_account(session, account['AMid'], update)
                if not result:
                    raise dberror
                # 更改账户余额
                user = get_model_return_dict(self.smycenter.get_user_basicinfo(account['USid'])) if \
                    self.smycenter.get_user_basicinfo(account['USid']) else None
                update = {}
                update['USmount'] = user['USmount'] + mydiscount
                self.smycenter.update_user_by_uid(session, account['USid'], update)
                session.commit()
            except Exception as e:
                print e
                session.rollback()
                return None
            finally:
                session.close()
        return True

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
            reason = data.get("reason")
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
        session = db_session()
        try:
            if willstatus == 3:
                # 写入代理消息
                time_now = datetime.strftime(datetime.now(), format_for_db)
                content = u'您已提现成功，流水号为' + ' ' + str(result['DMtradenum'])
                agent_result = self.smessage.create_agentmessage(session, result['USid'], time_now, content, 1)
                if not agent_result:
                    return SYSTEM_ERROR
            if willstatus == 4:
                time_now = datetime.strftime(datetime.now(), format_for_db)
                result2 = self.saccount.add_moneyrecord(session, result['USid'], +result['DMamount'], 7, time_now
                                                       , tradenum=result['DMtradenum'], oiid=None)
                user = get_model_return_dict(self.smycenter.get_user_basicinfo(result['USid'])) if \
                    self.smycenter.get_user_basicinfo(result['USid']) else None
                session.query(DrawMoney).filter(DrawMoney.DMid == dmid).update({"DMreason": str(reason)})
                update = {}
                update['USmount'] = round(user['USmount'] + result['DMamount'], 2)
                self.smycenter.update_user_by_uid(session, result['USid'], update)
            session.commit()
        except Exception as e:
            print e
            session.rollback()
            return SYSTEM_ERROR
        finally:
            session.close()
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
            user = get_model_return_dict(self.smycenter.get_user_basicinfo(record['USid']))
            record['username'] = user['USname']
            record['userphonenum'] = user['USphonenum']

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
            reason = data.get("reason")
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
        time_now = datetime.strftime(datetime.now(), format_for_db)
        session = db_session()
        try:
            if willstatus == 2:
                # 写入收支记录
                self.saccount.add_moneyrecord(session, result['USid'], result['CMamount'], 4, time_now
                                                        , tradenum=result['CMtradenum'], oiid=None)
                # 写入代理消息
                content = u'您已充值成功，流水号为' + ' ' + str(result['CMtradenum'])
                agent_result = self.smessage.create_agentmessage(session, result['USid'], time_now, content, 1)
                if not agent_result:
                    return SYSTEM_ERROR
                # 加余额
                user = get_model_return_dict(self.smycenter.get_user_basicinfo(result['USid'])) if \
                    self.smycenter.get_user_basicinfo(result['USid']) else None
                update = {}
                update['USmount'] = round(user['USmount'] + result['CMamount'], 2)
                self.smycenter.update_user_by_uid(session, result['USid'], update)
            if willstatus == 3:
                # 写入代理消息
                content = u'您充值失败，请联系客服处理，流水号为' + result['CMtradenum']
                session.query(ChargeMoney).filter(ChargeMoney.CMid == cmid).update({"CMreason": str(reason)})
                agent_result = self.smessage.create_agentmessage(session, result['USid'], time_now, content, 1)
                if not agent_result:
                    return SYSTEM_ERROR
            session.commit()
        except Exception as e:
            print e
            session.rollback()
            return SYSTEM_ERROR
        finally:
            session.close()
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
            response = import_status("get_bailrecordlist_success", "OK")
            response['data'] = []
            return response
        for record in result:
            from common.timeformat import get_web_time_str
            record['USphonenum'] = get_model_return_dict(self.smycenter.get_user_basicinfo(record['USid']))['USphonenum']
            record['USname'] = get_model_return_dict(self.smycenter.get_user_basicinfo(record['USid']))['USname']
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
            reason = data.get("reason")
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
        session = db_session()
        try:
            if willstatus == 3:
                time_now = datetime.strftime(datetime.now(), format_for_db)
                # 写入代理消息
                content = u'您的保证金退还成功，流水号为' + ' ' + str(result['BRtradenum'])
                agent_result = self.smessage.create_agentmessage(session, result['USid'], time_now, content, 1)

                self.saccount.add_moneyrecord(session, result['USid'], result['BRmount'], 6, time_now
                                              , tradenum=result['BRtradenum'], oiid=None)
                user = get_model_return_dict(self.smycenter.get_user_basicinfo(result['USid'])) if \
                    self.smycenter.get_user_basicinfo(result['USid']) else None
                update = {}
                update['USmount'] = user['USmount'] + result['BRmount']
                self.smycenter.update_user_by_uid(session, result['USid'], update)
            if willstatus == 4:
                # 写入代理消息
                content = u'您的保证金退还失败，原因:' + reason + u',请联系客服处理'
                time_now = datetime.strftime(datetime.now(), format_for_db)
                agent_result = self.smessage.create_agentmessage(session, result['USid'], time_now, content, 1)

                user = get_model_return_dict(self.smycenter.get_user_basicinfo(result['USid'])) if \
                    self.smycenter.get_user_basicinfo(result['USid']) else None
                update_bail = {}
                update_bail['USbail'] = user['USbail'] + result['BRmount']
                self.smycenter.update_user_by_uid(session, result['USid'], update_bail)
            session.commit()
        except Exception as e:
            print e
            session.rollback()
            return SYSTEM_ERROR
        finally:
            session.close()
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
        print 'start wxcz'
        wcsn = 'cz' + datetime.strftime(datetime.now(), format_for_db) + get_random_int(5)  # 充值号
        user = get_model_return_dict(self.smycenter.get_user_basicinfo(request.user.id))
        if not user:
            return NOT_FOUND_USER

        openid = user['openid']
        print 'get openid', openid
        if not openid:
            return NOT_FOUND_OPENID
        print 'add wxcz log'
        result = self.saccount.create_weixin_charge(request.user.id, openid, wcsn, amount)
        if not result:
            return SYSTEM_ERROR
        total_fee = float(amount) * 100
        print total_fee
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

    def pay_callback(self):
        data = self.pay.to_dict(request.data)
        print data
        if not self.pay.check(data):
            return self.pay.reply(u"签名验证失败", False)
        user = get_model_return_dict(self.suser.get_qrcode_by_openid(data.get("openid")))
        if not user:
            return SYSTEM_ERROR
        sn = str(data.get("out_trade_no"))
        if not self.saccount.get_record_by_wcsn(sn):
            return self.pay.reply(u'OK', True)

        USmount = float(user.get('USmount')) + (float(data.get('total_fee')) / 100)
        print 'to add usmount :', USmount
        result = self.suser.update_user_by_uid(user.get("USid"), {'USmount': USmount})
        if not result:
            return SYSTEM_ERROR
        # 修改微信充值状态
        session = db_session()
        try:
            self.saccount.update_weixin_charge(session, str(data.get("out_trade_no")))
            # todo 收支记录
            self.saccount.add_moneyrecord(
                session, user.get("USid"), float(data.get('total_fee')) / 100, 4,
                datetime.strftime(datetime.now(), format_for_db), sn, str(data.get("out_trade_no")))
            # 写入代理消息
            time_now = datetime.strftime(datetime.now(), format_for_db)
            content = u'您已通过微信充值成功，流水号为' + ' ' + str(sn)
            agent_result = self.smessage.create_agentmessage(session, user.get("USid"), time_now, content, 1)
            session.commit()
        except Exception as e:
            print e
            session.rollback()
        finally:
            session.close()
        return self.pay.reply(u'OK', True)

    def get_data_by_day(self, day):  # 获取当日的订单数以及销售额
        # 获取订单
        money = 0
        this_day = day + '000000'
        next_day = day + '240000'
        list = get_model_return_list(self.sorder.get_order_by_day(this_day, next_day))
        count = len(list)
        if list:
            for order in list:
                money = money + order['OImount']
        response = {}
        response['date'] = get_web_time_str(this_day, formattype=format_forweb_no_HMS)
        response['count'] = count
        response['money'] = money
        return response

    def get_data_by_month(self, month):  # 获取当月的订单数以及销售额
        # 获取订单
        money = 0
        this_month = month + '01000000'
        next_month = month + '32000000'
        list = get_model_return_list(self.sorder.get_order_by_day(this_month, next_month))
        count = len(list)
        if list:
            for order in list:
                money = money + order['OImount']
        response = {}
        response['date'] = get_web_time_str(this_month, formattype='%Y-%m')
        response['count'] = count
        response['money'] = money
        return response

    @verify_token_decorator
    def get_sevendays_data(self):  # 获取最近七天的销售数据
        if not is_admin():
            return TOKEN_ERROR
        today = date.today()
        days_list = []
        days_list.append(self.get_data_by_day(today.strftime("%Y%m%d")))
        for i in range(6):
            days_list.append(self.get_data_by_day((today + timedelta(days=-(i+1))).strftime("%Y%m%d")))
        response = import_status("get_sevendays_data_success", "OK")
        response['data'] = days_list
        return response

    @verify_token_decorator
    def get_thisyear_date(self):  # 获取当年销售数据
        if not is_admin():
            return TOKEN_ERROR
        today = date.today()
        year = today.year
        month = today.month
        print '11111111111111month', month
        year_month = str(year) + str(month)
        date_list = []
        # date_list.append(self.get_data_by_month(year_month))
        print '1111111111111int()', int(month)
        for i in range(1, int(month) + 1):
            last_month = str(i) if i >= 10 else '0'+str(i)
            last_yearmonth = str(year) + last_month
            date_list.append(self.get_data_by_month(last_yearmonth))
        response = import_status("get_year_data_success", "OK")
        response['date'] = date_list
        return response

    @verify_token_decorator
    def get_count_data(self):
        if not is_admin():
            return TOKEN_ERROR
        total_sale_num = 0
        total_sale_money = 0
        order_list = get_model_return_list(self.sorder.admin_get_all_order())
        total_order_num = len(order_list)
        if order_list:
            for order in order_list:
                total_sale_num = total_sale_num + order['productnum']
                total_sale_money = total_sale_money + order['OImount']
        order_user = get_model_return_list(self.sorder.get_order_user_num())
        unit_price = float(total_sale_money) / float(len(order_user)) if float(len(order_user)) >0 else 0
        total_agent_num = int(self.suser.get_user_num())
        response = import_status("get_count_data_success", "OK")
        data = {}
        data['total_sale_num'] = round(total_sale_num, 2)
        data['total_sale_money'] = total_sale_money
        data['total_agent_num'] = total_agent_num
        data['total_order_num'] = total_order_num
        data['unit_price'] = round(unit_price, 2)
        response['data'] = data
        return response

    @verify_token_decorator
    def get_thismonth_agentnum(self):
        if not is_admin():
            return TOKEN_ERROR
        starttime = datetime.strftime(datetime.now(), format_for_db)[:6] + '01000000'
        endtime = datetime.strftime(datetime.now(), format_for_db)
        num = int(self.suser.get_thismonth_agentnum(starttime, endtime))
        print starttime, endtime
        print '111111111111111num', num
        response = import_status("get_thismonth_agentnum_success", "OK")
        data = {
            "num": num
        }
        response['data'] = data
        return response

    @verify_token_decorator
    def update_configure(self):
        if not is_admin():
            return TOKEN_ERROR
        params_list = ['alipaynum', 'alipayname', 'bankname', 'accountname', 'cardnum', 'agentmoney', 'wechat', 'drawbank'
            , 'bail', 'reward', 'sendname', 'sendphone', 'sendaddress']
        data = request.json
        for param in params_list:
            if param not in data:
                params_miss = {
                    "paramname": param,
                    "status": 405,
                    "status_code": 405002,
                    "message": u"参数错误"
                }
                return params_miss
        alipaynum = data.get('alipaynum')
        alipayname = data.get('alipayname').encode('utf-8')
        bankname = data.get('bankname').encode('utf-8')
        accountname = data.get('accountname').encode('utf-8')
        cardnum = data.get('cardnum')
        money = float(data.get('agentmoney'))
        service = data.get('wechat').encode('utf-8')
        drawbank = data.get('drawbank').encode('utf-8')
        bail = float(data.get('bail'))
        reward = float(data.get('reward'))
        sendname = data.get('sendname')
        sendphone = data.get('sendphone')
        sendaddress = data.get('sendaddress')
        from config.modify_setting import modify
        result = modify(alipaynum, alipayname, bankname, accountname, cardnum, str(money), service, drawbank, str(bail)
                        , str(reward), sendname, sendphone, sendaddress)
        if not result:
            return SYSTEM_ERROR
        response = import_status("update_account_success", "OK")
        return response

    @verify_token_decorator
    def get_discountruler(self):
        if not is_admin():
            return TOKEN_ERROR
        list = get_model_return_list(self.saccount.get_discountruler())
        response = import_status("get_discountruler_success", "OK")
        response['data'] = list
        return response

    @verify_token_decorator
    def update_discountruler(self):
        if not is_admin():
            return TOKEN_ERROR
        try:
            data = request.json
            rulers = data.get('ruler')
        except:
            return PARAMS_ERROR
        session = db_session()
        all_number = []
        try:
            session.query(DiscountRuler).delete()
            for ruler in rulers:
                number = float(ruler['number'])
                if number in all_number:
                    return REPERT_NUMBER
                all_number.append(number)
                money = float(ruler['money'])
                discount = DiscountRuler()
                discount.DRid = str(uuid.uuid4())
                discount.DRnumber = number
                discount.DRmoney = money
                session.add(discount)
            session.commit()
        except Exception as e:
            print e
            session.rollback()
            return SYSTEM_ERROR
        finally:
            session.close()
        response = import_status("update_discountruler_success", "OK")
        return response

    @verify_token_decorator
    def get_configure(self):
        if not is_admin():
            return TOKEN_ERROR
        conf = ConfigParser()
        conf.read('config/setting.ini')
        user_dict = {}
        user_dict['alipaynum'] = conf.get('account', 'alipaynum')
        user_dict['alipayname'] = conf.get('account', 'alipayname')
        user_dict['bankname'] = conf.get('account', 'bankname')
        user_dict['accountname'] = conf.get('account', 'accountname')
        user_dict['cardnum'] = conf.get('account', 'cardnum')
        user_dict['agentmoney'] = float(conf.get('account', 'money'))
        user_dict['wechat'] = conf.get('account', 'service')
        user_dict['drawbank'] = conf.get('account', 'drawbank')
        user_dict['bail'] = float(conf.get('account', 'bail'))
        user_dict['reward'] = float(conf.get('account', 'reward'))
        user_dict['sendname'] = conf.get('account', 'sendname')
        user_dict['sendphone'] = (conf.get('account', 'sendphone'))
        user_dict['sendaddress'] = (conf.get('account', 'sendaddress'))
        response = import_status("get_configure_success", "OK")
        response['data'] = user_dict
        return response
