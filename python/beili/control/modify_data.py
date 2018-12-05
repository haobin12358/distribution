# *- coding:utf8 *-

import re
import sys
import os
import uuid
import random
import shutil
import xlrd
import xlwt
from flask import request
# import logging
import threading
from config.response import PARAMS_MISS, SYSTEM_ERROR, PARAMS_ERROR, TOKEN_ERROR, AUTHORITY_ERROR, STOCK_NOT_ENOUGH,\
        NO_ENOUGH_MOUNT, NO_BAIL, NO_ADDRESS, NOT_FOUND_ORDER, PRODUCT_OFFLINE, SKU_WRONG, CANNOT_CANCEL
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
from configparser import ConfigParser
from common.beili_error import stockerror, dberror
from datetime import datetime
from common.timeformat import format_for_db, get_random_str, get_random_int
from models.model import User, AgentMessage, Performance, Amount, Reward, MoneyRecord, OrderSkuInfo, ShoppingCart\
    , ProductSku, OrderInfo

sys.path.append(os.path.dirname(os.getcwd()))

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

if __name__ == "__main__":
    modify_data().modify()