# *- coding:utf8 *-
import sys
import os
import uuid
from werkzeug.security import check_password_hash
from service.SBase import SBase, close_session
from models.model import User,DrawMoney, Amount, DiscountRuler, ChargeMoney
from sqlalchemy import func
from common.beili_error import dberror, stockerror
from common.get_model_return_list import get_model_return_list, get_model_return_dict
sys.path.append(os.path.dirname(os.getcwd()))


class SAccount(SBase):

    @close_session
    def get_account_by_month(self, usid, month):  # 获取用户直推奖励和个人业绩数
        return self.session.query(Amount.reward, Amount.performance)\
            .filter(Amount.USid == usid).filter(Amount.AMmonth == month).first()

    @close_session
    def get_discount_ruler(self):
        return self.session.query(DiscountRuler.DRnumber, DiscountRuler.DRratio).order_by(DiscountRuler.DRnumber).all()

    @close_session
    def get_user_performance(self, usid, month):
        return self.session.query(Amount.USname, Amount.performance, Amount.USheadimg, Amount.USagentid
                                  ).filter_by(USid=usid).filter_by(AMmonth=month).all()

    @close_session
    def get_user_date(self, id, month):
        return self.session.query(Amount.reward, Amount.performance).filter(Amount.USid == id)\
            .filter(Amount.AMmonth == month).first()

    @close_session
    def add_drawmoney(self, id, usid, bankname, branchbank, accountname, cardnum, amount, time_now, tradenum):
        draw = DrawMoney()
        draw.DMDid = id
        draw.USid = usid
        draw.DMbankname = bankname
        draw.DMbranchname = branchbank
        draw.DMaccountname = accountname
        draw.DMcardnum = cardnum
        draw.DMamount = amount
        draw.DMcreatetime = time_now
        draw.DMtradenum = tradenum
        draw.DMstatus = 1
        self.session.add(draw)
        return True

    @close_session
    def get_drawmoney_list(self, id, status):
        return self.session.query(DrawMoney.DMstatus, DrawMoney.DMcreatetime, DrawMoney.DMamount, DrawMoney.DMtradenum)\
            .filter(DrawMoney.USid == id).order_by(DrawMoney.DMcreatetime.desc()).filter(DrawMoney.DMstatus == status).all()

    @close_session
    def get_all_drawmoney_list(self, id):
        return self.session.query(DrawMoney.DMstatus, DrawMoney.DMcreatetime, DrawMoney.DMamount, DrawMoney.DMtradenum)\
            .filter(DrawMoney.USid == id).order_by(DrawMoney.DMcreatetime.desc()).all()

    @close_session
    def get_all_chargemoney_list(self, id):
        return self.session.query(ChargeMoney.CMstatus, ChargeMoney.CMcreatetime, ChargeMoney.CMtradenum, ChargeMoney.CMamount)\
            .filter(ChargeMoney.USid == id).all()

    @close_session
    def get_chargemoney_list(self, id, status):
        return self.session.query(ChargeMoney.CMstatus, ChargeMoney.CMcreatetime, ChargeMoney.CMtradenum,
            ChargeMoney.CMamount).filter(ChargeMoney.USid == id).filter(ChargeMoney.CMstatus == status).all()

    @close_session
    def charge_money(self, cmid, usid, paytype, alipaynum, bankname, accountname, cardnum, amount, remark, tradenum, createtime):
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
        self.session.add(charge)
        return True

