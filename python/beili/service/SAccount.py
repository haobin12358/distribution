# *- coding:utf8 *-
import sys
import os
import uuid
from werkzeug.security import check_password_hash
from service.SBase import SBase, close_session
from models.model import User,DrawMoney, Amount, DiscountRuler, ChargeMoney, BailRecord, WeixinCharge, MoneyRecord, Reward
from sqlalchemy import func
from common.beili_error import dberror, stockerror
from common.get_model_return_list import get_model_return_list, get_model_return_dict
sys.path.append(os.path.dirname(os.getcwd()))


class SAccount(SBase):

    @close_session
    def get_account_by_month(self, usid, month):  # 获取用户直推奖励和个人业绩数
        return self.session.query(Amount.reward, Amount.performance, Amount.AMid, Amount.AMstatus)\
            .filter(Amount.USid == usid).filter(Amount.AMmonth == month).first()

    @close_session
    def update_account(self, session, amid, update):
        session.query(Amount).filter(Amount.AMid == amid).update(update)
        return True

    @close_session
    def get_discount_ruler(self):
        return self.session.query(DiscountRuler.DRnumber, DiscountRuler.DRmoney).order_by(DiscountRuler.DRnumber).all()

    @close_session
    def get_user_performance(self, usid, month):
        return self.session.query(Amount.USname, Amount.performance, Amount.USheadimg, Amount.USagentid
                                  ).filter_by(USid=usid).filter_by(AMmonth=month).all()

    @close_session
    def get_user_date(self, id, month):
        return self.session.query(Amount.reward, Amount.performance).filter(Amount.USid == id)\
            .filter(Amount.AMmonth == month).first()

    @close_session
    def add_drawmoney(self, session, id, usid, bankname, branchbank, accountname, cardnum, amount, time_now, tradenum):
        draw = DrawMoney()
        draw.DMid = id
        draw.USid = usid
        draw.DMbankname = bankname
        draw.DMbranchname = branchbank
        draw.DMaccountname = accountname
        draw.DMcardnum = cardnum
        draw.DMamount = amount
        draw.DMcreatetime = time_now
        draw.DMtradenum = tradenum
        draw.DMstatus = 1
        session.add(draw)
        return True

    @close_session
    def get_drawmoney_list(self, id, status):
        return self.session.query(DrawMoney.DMstatus, DrawMoney.DMcreatetime, DrawMoney.DMamount, DrawMoney.DMtradenum)\
            .filter(DrawMoney.USid == id).filter(DrawMoney.DMstatus == status).order_by(DrawMoney.DMcreatetime.desc()).all()

    @close_session
    def get_all_drawmoney_list(self, id):
        return self.session.query(DrawMoney.DMstatus, DrawMoney.DMcreatetime, DrawMoney.DMamount, DrawMoney.DMtradenum)\
            .filter(DrawMoney.USid == id).order_by(DrawMoney.DMcreatetime.desc()).all()

    @close_session
    def get_alluser_drawmoney_list(self, status):
        result = self.session.query(DrawMoney.DMstatus, DrawMoney.DMcreatetime, DrawMoney.DMamount, DrawMoney.DMtradenum
                                  , DrawMoney.DMbankname, DrawMoney.DMbranchname, DrawMoney.DMaccountname, DrawMoney.DMid
                                  , DrawMoney.DMcardnum).order_by(DrawMoney.DMcreatetime.desc())
        if status > 0:
            result = result.filter(DrawMoney.DMstatus == status)
        result = result.all()
        return result

    @close_session
    def update_by_dmid(self, id, update2):
        self.session.query(DrawMoney).filter(DrawMoney.DMid == id).update(update2)
        return True

    @close_session
    def get_drawmoney_info(self, id):
        return self.session.query(DrawMoney.USid, DrawMoney.DMstatus, DrawMoney.DMamount, DrawMoney.DMtradenum).filter(DrawMoney.DMid == id).first()

    @close_session
    def get_alluser_chargemoney(self, status):
        result = self.session.query(ChargeMoney.USid, ChargeMoney.CMpaytime, ChargeMoney.CMstatus, ChargeMoney.CMamount, ChargeMoney.CMproof
                                  , ChargeMoney.CMtradenum, ChargeMoney.CMcreatetime, ChargeMoney.CMpaytime, ChargeMoney.CMremark
                                  , ChargeMoney.CMcardnum, ChargeMoney.CMaccountname, ChargeMoney.CMbankname, ChargeMoney.CMalipaynum
                                  , ChargeMoney.CMstatus, ChargeMoney.CMid).order_by(ChargeMoney.CMcreatetime.desc())
        if status > 0:
            result = result.filter(ChargeMoney.CMstatus == status)
        result = result.all()
        return result

    @close_session
    def add_moneyrecord(self, session, usid,  amount, type, createtime, tradenum=None, oiid=None):
        record = MoneyRecord()
        record.MRid = str(uuid.uuid4())
        record.USid = usid
        record.MRamount = amount
        record.MRtype = type
        record.MRcreatetime = createtime
        record.MRtradenum = tradenum
        record.OIid = oiid
        session.add(record)
        return True


    @close_session
    def get_chargemoney_info(self, cmid):
        return self.session.query(ChargeMoney.USid, ChargeMoney.CMamount, ChargeMoney.CMtradenum).filter(ChargeMoney.CMid == cmid).first()

    @close_session
    def update_by_cmid(self, id, update2):
        self.session.query(ChargeMoney).filter(ChargeMoney.CMid == id).update(update2)
        return True

    @close_session
    def get_all_chargemoney_list(self, id):
        return self.session.query(ChargeMoney.CMstatus, ChargeMoney.CMcreatetime, ChargeMoney.CMtradenum,
                                  ChargeMoney.CMamount, ChargeMoney.CMpaytime).filter(ChargeMoney.USid == id).all()

    @close_session
    def get_chargemoney_list(self, id, status):
        return self.session.query(ChargeMoney.CMstatus, ChargeMoney.CMcreatetime, ChargeMoney.CMtradenum,
            ChargeMoney.CMamount, ChargeMoney.CMpaytime).filter(ChargeMoney.USid == id).filter(ChargeMoney.CMstatus == status).all()

    @close_session
    def charge_money(self, cmid, usid, paytype, alipaynum, bankname, accountname, cardnum, amount, remark, tradenum,\
                     createtime, proof, paytime):
        charge = ChargeMoney()
        charge.CMid = cmid
        charge.USid = usid
        charge.CMpaytype = paytype
        charge.CMalipaynum = alipaynum
        charge.CMbankname = bankname
        charge.CMaccountname = accountname
        charge.CMcardnum = cardnum
        charge.CMamount = amount
        charge.CMremark = remark
        charge.CMstatus = 1
        charge.CMtradenum = tradenum
        charge.CMcreatetime = createtime
        charge.CMproof = proof
        charge.CMpaytime = paytime + '000000'
        self.session.add(charge)
        return True

    @close_session
    def check_openid(self, usid):
        return self.session.query(User.openid).filter(User.USid == usid).first()

    @close_session
    def get_bail_record(self, id, status):
        return self.session.query(BailRecord).filter(BailRecord.USid == id).filter(BailRecord.BRstatus == status).first()

    @close_session
    def get_alluser_bailrecord(self, status):
        list = self.session.query(BailRecord.BRtradenum, BailRecord.USid, BailRecord.BRstatus, BailRecord.BRcreatetime
                    , BailRecord.BRtype, BailRecord.BRmount, BailRecord.BRid).order_by(BailRecord.BRcreatetime.desc())
        if status > 0:
            list = list.filter(BailRecord.BRstatus == status)
        list = list.all()
        return list

    @close_session
    def get_bailrecord_info(self, id):
        return self.session.query(BailRecord.USid, BailRecord.BRtradenum, BailRecord.BRmount)\
            .filter(BailRecord.BRid == id).first()

    @close_session
    def update_bailrecord(self, id, update):
        self.session.query(BailRecord).filter(BailRecord.BRid == id).update(update)
        return True

    @close_session
    def get_alluser_account(self, name, month, agentid, status):
        list = self.session.query(Amount.USid, Amount.reward, Amount.USagentid, Amount.USname, Amount.AMmonth, Amount.AMstatus
                                  , Amount.AMid, Amount.performance, Amount.AMtradenum)
        if name:
            list = list.filter(Amount.USname.like('%{0}%'.format(name)))
        if month:
            list = list.filter(Amount.AMmonth == month)
        if agentid:
            list = list.filter(Amount.USagentid.like('%{0}%'.format(agentid)))
        if int(status) > 0:
            list = list.filter(Amount.AMstatus == status)
        list = list.all()
        return list

    @close_session
    def getstatus_by_admidandmonth(self, amid, usid, month):
        return self.session.query(Amount.AMstatus, Amount).filter(Amount.AMid == amid).filter(Amount.USid == usid)\
                .filter(Amount.AMmonth == month).first()

    @close_session
    def get_moneyrecord(self, id):
        return self.session.query(MoneyRecord.MRid, MoneyRecord.MRcreatetime, MoneyRecord.MRamount, MoneyRecord.OIid
                                  , MoneyRecord.MRtype, MoneyRecord.MRtradenum).filter(MoneyRecord.USid == id)\
                                  .order_by(MoneyRecord.MRcreatetime.desc()).all()

    @close_session
    def get_reward_by_nextid(self, id):
        return self.session.query(Reward.REmount, Reward.REmonth).filter(Reward.REnextuserid == id).first()

    @close_session
    def create_weixin_charge(self, id, openid, wcsn, amount):
        charge = WeixinCharge()
        charge.WCid = str(uuid.uuid4())
        charge.USid = id
        charge.WCamount = amount
        charge.WCopenid = openid
        charge.WCstatus = 1
        charge.WCsn = wcsn
        self.session.add(charge)
        return True

    @close_session
    def get_record_by_wcsn(self, wcsn):
        return self.session.query(WeixinCharge.WCstatus).filter(WeixinCharge.WCsn == wcsn, WeixinCharge.WCstatus < 2).first()

    @close_session
    def update_weixin_charge(self, session, wcsn):
        return self.session.query(WeixinCharge.WCid).filter(WeixinCharge.WCsn == wcsn).update(
            {"WCstatus": 2}, synchronize_session=False)

    @close_session
    def get_discountruler(self):
        return self.session.query(DiscountRuler.DRid, DiscountRuler.DRnumber, DiscountRuler.DRmoney)\
            .order_by(DiscountRuler.DRnumber).all()