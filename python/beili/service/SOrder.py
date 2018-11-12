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


    def add_orderproductinfo(self, session, OPIid, OIid, PRid, PRname, PRprice, PRnum, PRimage):
        product = OrderProductInfo()
        product.OPIid = OPIid
        product.OIid = OIid
        product.PRid = PRid
        product.PRname = PRname
        product.PRprice = PRprice
        product.PRnum = PRnum
        product.PRimage = PRimage
        session.add(product)
        return True

    def add_order(self, session, OIid, OIsn, USid, OInote, OImount, UAid, OIcreatetime, logisticsfee,
                  provincename, cityname, areaname, details, username, userphonenum, product_num):
        order = OrderInfo()
        order.OIid = OIid
        order.OIsn = OIsn
        order.USid = USid
        order.OInote = OInote
        order.OImount = OImount
        order.UAid = UAid
        order.OIcreatetime = OIcreatetime
        order.OIlogisticsfee = logisticsfee
        order.provincename = provincename
        order.cityname = cityname
        order.areaname = areaname
        order.details = details
        order.username = username
        order.userphonenum = userphonenum
        order.productnum = product_num
        session.add(order)
        return True

    @close_session
    def get_order_list(self, usid, type, page, count):
        return self.session.query(OrderInfo.OIsn, OrderInfo.OIcreatetime, OrderInfo.OIstatus, OrderInfo.OImount, \
            OrderInfo.OIid).filter(OrderInfo.USid == usid).filter(OrderInfo.OIstatus == type).order_by(
            OrderInfo.OIcreatetime.desc()).offset((page - 1) * count).limit(count)

    @close_session
    def get_allorder_list(self, usid, page, count):
        return self.session.query(OrderInfo.OIsn, OrderInfo.OIcreatetime, OrderInfo.OIstatus, OrderInfo.OImount, \
            OrderInfo.OIid).filter(OrderInfo.USid == usid).order_by(OrderInfo.OIcreatetime.desc())\
            .offset((page - 1) * count).limit(count)

    @close_session
    def get_total_order_num(self, usid):
        return self.session.query(func.count(OrderInfo.OIid)).filter(OrderInfo.USid == usid).scalar()

    @close_session
    def get_all_order_num(self):
        return self.session.query(func.count(OrderInfo.OIid)).scalar()

    @close_session
    def get_order_num(self, usid, state):
        return self.session.query(func.count(OrderInfo.OIid)).filter(OrderInfo.USid == usid)\
            .filter(OrderInfo.OIstatus == state).scalar()

    @close_session
    def get_product_list(self, oiid):
        return self.session.query(OrderProductInfo.PRname, OrderProductInfo.PRimage, OrderProductInfo.PRnum\
                                  , OrderProductInfo.PRprice).filter(OrderProductInfo.OIid == oiid).all()

    @close_session
    def get_order_details(self, oisn):
        return self.session.query(OrderInfo.OIid, OrderInfo.OIsn, OrderInfo.OIcreatetime, OrderInfo.OIstatus,\
                                  OrderInfo.OIlogisticsfee, OrderInfo.USid, OrderInfo.UAid, OrderInfo.OInote\
                                  , OrderInfo.OImount, OrderInfo.OIcreatetime, OrderInfo.username, OrderInfo.userphonenum\
                                  , OrderInfo.provincename, OrderInfo.cityname, OrderInfo.areaname, OrderInfo.details
                                  , OrderInfo.expressname, OrderInfo.expressnum)\
                                  .filter(OrderInfo.OIsn == oisn).first()

    @close_session
    def get_all_order(self, oisn, starttime, endtime, status, username, userphonenum):
        order_list = self.session.query(OrderInfo.OIid, OrderInfo.OIsn, OrderInfo.OIstatus, OrderInfo.OIlogisticsfee,
                                        OrderInfo.username, OrderInfo.userphonenum, OrderInfo.OImount, OrderInfo.expressname,
                                        OrderInfo.provincename, OrderInfo.cityname, OrderInfo.areaname,OrderInfo.details,
                                        OrderInfo.expressnum, OrderInfo.OIcreatetime).order_by(OrderInfo.OIcreatetime.desc())
        if oisn:
            order_list = order_list.filter(OrderInfo.OIsn.like('%{0}%'.format(oisn)))
        if starttime:
            order_list = order_list.filter(OrderInfo.OIcreatetime >= starttime)
        if endtime:
            order_list = order_list.filter(OrderInfo.OIcreatetime <= endtime)
        if status:
            order_list = order_list.filter(OrderInfo.OIstatus == status)
        if username:
            order_list = order_list.filter(OrderInfo.username.like('%{0}%'.format(username)))
        if userphonenum:
            order_list = order_list.filter(OrderInfo.userphonenum.like('%{0}%'.format(userphonenum)))
        return order_list.all()

    @close_session
    def update_order(self, oisn, update):
        self.session.query(OrderInfo).filter(OrderInfo.OIsn == oisn).update(update)
        return True

    @close_session
    def get_order_by_day(self, this_day, next_day):
        return self.session.query(OrderInfo.OImount).filter(OrderInfo.OIcreatetime >= this_day).filter(OrderInfo\
                    .OIcreatetime < next_day).all()

    @close_session
    def admin_get_all_order(self):
        return self.session.query(OrderInfo.productnum, OrderInfo.OImount).all()

    @close_session
    def get_order_user_num(self):
        return self.session.query(OrderInfo.USid).group_by(OrderInfo.USid)