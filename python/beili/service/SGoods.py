# *- coding:utf8 *-
import sys
import os
from service.SBase import SBase, close_session
from models.model import Product, ProductCategory
sys.path.append(os.path.dirname(os.getcwd()))

class SGoods(SBase):

    def __init__(self):
        super(SGoods, self).__init__()

    @close_session
    def get_product_list(self, page_size, page_num, PAid=None, PRstatus=None):
        product_list = self.session.query(Product.PRpic, Product.PRname, Product.PRoldprice, Product.PRprice,
                                          Product.PRstock, Product.PRid)
        if PAid:
            product_list = product_list.filter_by(PAid=PAid)
        if PRstatus:
            product_list = product_list.filter_by(PRstatus=PRstatus)
        product_list = product_list.limit(page_size).offset((page_num - 1) * page_size).all()
        return product_list

    @close_session
    def get_product(self, PRid):
        return self.session.query(Product.PRstock, Product.PRstatus, Product.PRprice, Product.PRoldprice,
                                  Product.PRname, Product.PRpic, Product.PAid, Product.PRcreatetime,
                                  Product.PRlogisticsfee, Product.PRmodifytime, Product.SUmodifyid)\
            .filter_by(PRid=PRid).first()

    @close_session
    def update_product(self, PRid, product):
        self.session.query(Product).filter_by(PRid=PRid).update(product)
        return True

    @close_session
    def get_paname(self, PAid):
        return self.session.query(ProductCategory.PAname).filter_by(PAid=PAid).first()

    @close_session
    def get_childid(self, Parentid):
        return self.session.query(ProductCategory.PAid).filter_by(Parentid=Parentid).all()

    @close_session
    def update_productcategory(self, PAid, productcategory):
        self.session.query(ProductCategory).filter_by(PAid=PAid).update(productcategory)
        return True

    @close_session
    def get_first_product_category(self, Parentid):
        return self.session.query(ProductCategory.PAid, ProductCategory.PAname).filter_by(Parentid=Parentid).all()