# *- coding:utf8 *-

import sys
import os
from common.get_model_return_list import get_model_return_list, get_model_return_dict
from service.SUser import SUser
from service.SMessage import SMessage
from service.SOrder import SOrder
from service.SGoods import SGoods
from service.SMyCenter import SMyCenter
from service.DBSession import db_session
from service.SAccount import SAccount
from models.model import User, AgentMessage, Performance, Amount, Reward, MoneyRecord, OrderSkuInfo, ShoppingCart\
    , ProductSku, OrderInfo

class modify_data():
    def __init__(self):
        self.suser = SUser()
        self.sorder = SOrder()
        self.sgoods = SGoods()
        self.smycenter = SMyCenter()
        self.smessage = SMessage()
        self.saccount = SAccount()


    def modify(self):
        all_order = get_model_return_list(self.sorder.get_all_order(None, None, None, 1, None, None))\
            + get_model_return_list(self.sorder.get_all_order(None, None, None, 2, None, None))\
            + get_model_return_list(self.sorder.get_all_order(None, None, None, 4, None, None)) \
            + get_model_return_list(self.sorder.get_all_order(None, None, None, 5, None, None))
        session = db_session()
        try:
            for order in all_order:
                product_list = get_model_return_list(self.sorder.get_product_list(order['OIid']))
                real_discount = 0
                for product in product_list:
                    check_product = get_model_return_dict(self.sgoods.get_product_info(product['PRid']))
                    sku_list = get_model_return_list(self.sorder.get_sku_list_by_opiid(product['OPIid']))
                    for sku in sku_list:
                        real_discount = real_discount + sku['number'] * check_product['PAdiscountnum']
                session.query(OrderInfo).filter(OrderInfo.OIid == order['OIid']).update({'discountnum': real_discount})
            session.commit()
        except:
            session.rollback()
        finally:
            session.close()
        session = db_session()
        try:
            amount_list = get_model_return_list(session.query(Amount.AMmonth, Amount.USid).all())
            for amount in amount_list:
                real_amount = 0
                order_list = get_model_return_list(session.query(OrderInfo.discountnum)
                    .filter(OrderInfo.USid == amount['USid']).filter(OrderInfo.OIstatus == 2).all())
                for order in order_list:
                    real_amount = real_amount + order['discountnum']
                session.query(Amount).filter(Amount.USid == amount['USid']).update({'performance': real_amount})
            session.commit()
        except:
            session.rollback()
        finally:
            session.close()

modify_data().modify()