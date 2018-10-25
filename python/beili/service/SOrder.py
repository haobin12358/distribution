# *- coding:utf8 *-
import sys
import os
import uuid
from werkzeug.security import check_password_hash
from service.SBase import SBase, close_session
from models.model import User, IdentifyingCode, OrderInfo, AlreadyRead, ComMessage, OrderProductInfo, Product
from sqlalchemy import func
from common.beili_error import dberror, stockerror
from common.get_model_return_list import get_model_return_list, get_model_return_dict
sys.path.append(os.path.dirname(os.getcwd()))


class SOrder(SBase):

    @close_session
    def check_stock(self, product_list):
        for product in product_list:
            PRid = product['PRid']
            PRstock = product['PRnum']
            real_num = get_model_return_dict(self.session.query(Product.PRstock).filter_by(PRid=PRid).first())
            if real_num['PRstock'] < PRstock:
                raise stockerror('库存不足')
            update_stock = {}
            update_stock['PRstock'] = real_num['PRstock'] - PRstock
            result = self.session.query(Product).filter_by(PRid=PRid).update(update_stock)
            if not result:
                raise dberror
        return True


    @close_session
    def add_orderproductinfo(self, OPIid, OIid, PRid, PRname, PRprice, PRnum, PRimage):
        product = OrderProductInfo()
        product.OPIid = OPIid
        product.OIid = OIid
        product.PRid = PRid
        product.PRname = PRname
        product.PRprice = PRprice
        product.PRnum = PRnum
        product.PRimage = PRimage
        self.session.add(product)
        return True

    @close_session
    def add_order(self, OIid, OIsn, USid, OInote, OImount, UAid, OIcreatetime):
        order = OrderInfo()
        order.OIid = OIid
        order.OIsn = OIsn
        order.USid = USid
        order.OInote = OInote
        order.OImount = OImount
        order.UAid = UAid
        order.OIcreatetime = OIcreatetime
        self.session.add(order)
        return True

    @close_session
    def get_order_list(self, usid, type):
        return self.session.query(OrderInfo.OIsn, OrderInfo.OIcreatetime, OrderInfo.OIstatus, OrderInfo.OImount, \
            OrderInfo.OIid).filter(OrderInfo.USid == usid).filter(OrderInfo.OIstatus == type).all()

    @close_session
    def get_allorder_list(self, usid):
        return self.session.query(OrderInfo.OIsn, OrderInfo.OIcreatetime, OrderInfo.OIstatus, OrderInfo.OImount, \
            OrderInfo.OIid).filter(OrderInfo.USid == usid).all()

    @close_session
    def get_product_list(self, oiid):
        return self.session.query(OrderProductInfo.PRname, OrderProductInfo.PRimage, OrderProductInfo.PRnum\
                                  , OrderProductInfo.PRprice).filter(OrderProductInfo.OIid == oiid).all()