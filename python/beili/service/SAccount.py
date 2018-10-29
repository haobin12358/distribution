# *- coding:utf8 *-
import sys
import os
import uuid
from werkzeug.security import check_password_hash
from service.SBase import SBase, close_session
from models.model import User, IdentifyingCode, OrderInfo, OrderProductInfo, Reward, Performance, Amount, DiscountRuler
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
        return self.session.query(DiscountRuler.DRnumber, DiscountRuler.DRratio).order_by(DiscountRuler.DRmoney).all()
