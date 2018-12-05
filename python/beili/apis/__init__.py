# *- coding:utf8 *-
from control.COrder import COrder
from control.CAccount import CAccount
import threading

print "start timer_fun after 5s!"
timer1 = threading.Timer(5, COrder().timer_fun)  # 首次启动定时器
timer1.setDaemon(True)
timer1.start()

print "start deal_profit_fail after 5s!"
timer2 = threading.Timer(5, CAccount().deal_reward_discount)  # 首次启动处理奖金定时器
timer2.setDaemon(True)
timer2.start()

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
        print '1111', all_order
        session = db_session()
        try:
            for order in all_order:
                product_list = get_model_return_list(self.sorder.get_product_list(order['OIid']))
                real_discount = 0
                print '22222'
                for product in product_list:
                    check_product = get_model_return_dict(self.sgoods.get_product_info(product['PRid']))
                    sku_list = get_model_return_list(self.sorder.get_sku_list_by_opiid(product['OPIid']))
                    for sku in sku_list:
                        print float(sku['number'] * check_product['PAdiscountnum'])
                        print real_discount
                        real_discount = real_discount + int(sku['number']) * float(check_product['PAdiscountnum'])
                        print real_discount
                session.query(OrderInfo).filter(OrderInfo.OIid == order['OIid']).update({'discountnum': real_discount})
            session.commit()
        except Exception as e:
            print e
            session.rollback()
        finally:
            session.close()
        session = db_session()
        print 'order ok!'
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
        except Exception as e:
            print e
            session.rollback()
        finally:
            session.close()
        print 'amount ok!'

modify_data().modify()