# *- coding:utf8 *-
import sys
import os
from service.SBase import SBase, close_session
from models.model import Product, ProductCategory, SowingMap
from sqlalchemy import func
sys.path.append(os.path.dirname(os.getcwd()))

class SGoods(SBase):

    def __init__(self):
        super(SGoods, self).__init__()

    @close_session
    def admin_get_product(self, PRstatus=None, PRname=None, PAid=None):
        product_list = self.session.query(Product.PRpic, Product.PRname, Product.PAid, Product.PRoldprice, Product.PRprice,
                                          Product.PRstock, Product.PRid, Product.PRlogisticsfee, Product.PAdiscountnum,
                                          Product.PRcreatetime, Product.PRstatus)
        if PAid:
            product_list = product_list.filter(Product.PAid == PAid)
        if PRstatus:
            product_list = product_list.filter_by(PRstatus=PRstatus)
        if PRname:
            product_list = product_list.filter(Product.PRname.like('%{0}%'.format(PRname)))
        product_list = product_list.order_by(Product.PRcreatetime.desc()).all()
        return product_list

    @close_session
    def get_category_byid(self, id):
        return self.session.query(ProductCategory.PAname, ProductCategory.Parentid).filter(ProductCategory.PAid == id).first()


    @close_session
    def get_product_list(self, page_size, page_num, PAid=None, PRstatus=None):
        product_list = self.session.query(Product.PRpic, Product.PRname, Product.PRoldprice, Product.PRprice,
                Product.PRstock, Product.PRid, Product.PRlogisticsfee,
                Product.PRcreatetime).filter_by(PRstatus=PRstatus).order_by(Product.PRcreatetime.desc())
        mount = self.session.query(func.count(Product.PAid)).filter_by(PRstatus=PRstatus).scalar()
        if PAid:
            product_list = product_list.filter_by(PAid=PAid)
            mount = self.session.query(func.count(Product.PAid)).filter_by(PAid=PAid).filter_by(PRstatus=PRstatus).scalar()
        product_list = product_list.limit(page_size).offset((page_num - 1) * page_size).all()
        return product_list, mount

    @close_session
    def get_type1_product(self, PAid=None, PRstatus=None):

        return self.session.query(Product.PRpic, Product.PRname, Product.PRoldprice, Product.PRprice, Product.PRcreatetime,
                Product.PRlogisticsfee,Product.PRstock, Product.PRid).filter_by(PRstatus=PRstatus).filter_by(PAid=PAid)


    @close_session
    def get_product(self, PRid):
        return self.session.query(Product.PRstock, Product.PRpic, Product.PRstatus, Product.PRprice, Product.PRoldprice,
                Product.PRname, Product.PRpic, Product.PRoldprice, Product.PAid, Product.PRcreatetime,
                Product.PRlogisticsfee, Product.PAdiscountnum).filter_by(PRid=PRid).first()

    @close_session
    def update_product(self, PRid, product):
        self.session.query(Product).filter_by(PRid=PRid).update(product)
        return True

    @close_session
    def create_product(self, id, paid, prname, prpic, proldprice, prprice, prstock, prlogisticsfee, prstatus, prdiscountnum, createtime):
        product = Product()
        product.PRid = id
        product.PAid = paid
        product.PRname = prname
        product.PRpic = prpic
        product.PRoldprice = proldprice
        product.PRprice = prprice
        product.PRstock = prstock
        product.PRlogisticsfee = prlogisticsfee
        product.PRstatus = prstatus
        product.PAdiscountnum = prdiscountnum
        product.PRcreatetime = createtime
        self.session.add(product)
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
    def get_product_category_list(self, Parentid):
        return self.session.query(ProductCategory.PAid, ProductCategory.PAname, ProductCategory.PAstatus).filter_by(Parentid=Parentid).all()
    @close_session
    def get_first_product_category_status(self, Parentid):
        return self.session.query(ProductCategory.PAid, ProductCategory.PAname, ProductCategory.PAstatus).filter_by(Parentid=Parentid).all()
    @close_session
    def get_first_product_category(self, Parentid):
        return self.session.query(ProductCategory.PAid, ProductCategory.PAname, ProductCategory.PAtype).filter_by(Parentid=Parentid).all()
    @close_session
    def get_child_product_category(self, Parentid):
        return self.session.query(ProductCategory.PAid, ProductCategory.PAname, ProductCategory.Parentid).filter_by(Parentid=Parentid).all()
    @close_session
    def get_product_category(self, PAid):
        return self.session.query(ProductCategory.PAstatus).filter_by(PAid=PAid).all()
    @close_session
    def add_product_category(self, PAid, PAname, PAtype, Parentid=0):
        #添加商品分类
        productcategory = ProductCategory()
        productcategory.PAid = PAid
        productcategory.PAname = PAname
        productcategory.PAtype = PAtype
        productcategory.Parentid = Parentid
        self.session.add(productcategory)
        return True
    @close_session
    def update_product_category(self, PAid, update_category):
        #更新商品分类
        return self.session.query(ProductCategory).filter_by(PAid=PAid).update(update_category)
    @close_session
    def delete_category(self, PAid, delete_category):
        #删除商品分类
        return self.session.query(ProductCategory).filter_by(PAid=PAid).update(delete_category)

class SSowing(SBase):
    def __init__(self):
        super(SSowing, self).__init__()
    @close_session
    def get_url_by_mall(self, url):
        return self.session.query(SowingMap.personUrls).filter_by(mallUrls=url).all()
    @close_session
    def get_url_by_person(self, url):
        return self.session.query(SowingMap.mallUrls).filter_by(personUrls=url).all()
    @close_session
    def update_sowingmap_status(self, url, status):
        return self.session.query(SowingMap).filter_by(mallUrls=url).update(status)
    @close_session
    def update_sowingmap_status(self, url, status):
        return self.session.query(SowingMap).filter_by(personUrls=url).update(status)
