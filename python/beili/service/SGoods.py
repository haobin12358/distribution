# *- coding:utf8 *-
import sys
import os
import uuid
from service.SBase import SBase, close_session
from models.model import Product, ProductCategory, SowingMap, Color, Size, ProductSku, ShoppingCart
from sqlalchemy import func
from datetime import datetime
from common.timeformat import format_for_db, get_random_str, format_for_db_no_HMS, get_random_int\
    , format_forweb_no_HMS, format_for_dbmonth
sys.path.append(os.path.dirname(os.getcwd()))

class SGoods(SBase):

    def __init__(self):
        super(SGoods, self).__init__()

    @close_session
    def admin_get_product(self, PRstatus=None, PRname=None, PAid=None):
        product_list = self.session.query(Product.PRpic, Product.PRname, Product.PAid, Product.PRoldprice, Product.PRprice,
                                          Product.PRid, Product.PRlogisticsfee, Product.PAdiscountnum,
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
    def get_product_details(self, prid):
        return self.session.query(Product.sowingmap, Product.PRid, Product.PRlogisticsfee, Product.PRoldprice, Product.PRprice
                                  , Product.PRname, Product.PRpic).filter(Product.PRid == prid).first()

    @close_session
    def get_sku_by_prid(self, prid):
        return self.session.query(ProductSku.PSid, ProductSku.colorid, ProductSku.colorname, ProductSku.sizeid
                                  , ProductSku.sizename, ProductSku.PSstock).filter(ProductSku.PRid == prid)\
                                  .filter(ProductSku.PSstatus == 1).order_by(ProductSku.sizename).all()


    @close_session
    def get_category_byid(self, id):
        return self.session.query(ProductCategory.PAname, ProductCategory.Parentid).filter(ProductCategory.PAid == id).first()

    @close_session
    def withdraw_product(self, prid):
        update = {}
        update['PRstatus'] = 3
        self.session.query(Product).filter(Product.PRid == prid).update(update)
        return True

    @close_session
    def get_product_list(self, page_size, page_num, PAid=None, PRstatus=None):
        product_list = self.session.query(Product.PRpic, Product.PRname, Product.PRoldprice, Product.PRprice,
                Product.PRid, Product.PRlogisticsfee,
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
                Product.PRlogisticsfee, Product.PRid).filter_by(PRstatus=PRstatus).filter_by(PAid=PAid)


    @close_session
    def get_product(self, PRid):
        return self.session.query(Product.PRpic, Product.PRstatus, Product.PRprice, Product.PRoldprice,
                Product.PRname, Product.PRpic, Product.PRoldprice, Product.PAid, Product.PRcreatetime,
                Product.PRlogisticsfee, Product.PAdiscountnum).filter_by(PRid=PRid).first()

    @close_session
    def update_product(self, session, PRid, product):
        session.query(Product).filter_by(PRid=PRid).update(product)
        return True

    def create_product(self, session, id, paid, prname, prpic, proldprice, prprice, prlogisticsfee, prstatus
                       , prdiscountnum, createtime, sowingmap):
        product = Product()
        product.PRid = id
        product.PAid = paid
        product.PRname = prname
        product.PRpic = prpic
        product.PRoldprice = proldprice
        product.PRprice = prprice
        product.PRlogisticsfee = prlogisticsfee
        product.PRstatus = prstatus
        product.PAdiscountnum = prdiscountnum
        product.PRcreatetime = createtime
        product.sowingmap = sowingmap
        session.add(product)
        return True

    def create_sku(self, session, prid, coid, colorname, siid, sizename, stock, time_now):
        sku = ProductSku()
        sku.PSid = str(uuid.uuid4())
        sku.PRid = prid
        sku.colorid = coid
        sku.colorname = colorname
        sku.sizeid = siid
        sku.sizename = sizename
        sku.PSstock = stock
        sku.PScreatetime = time_now
        sku.PSstatus = 1
        session.add(sku)

    def update_sku(self, session, prid, skuid, update):
        session.query(ProductSku).filter(ProductSku.PRid == prid).filter(ProductSku.PSid == skuid).update(update)


    @close_session
    def get_all_skuid(self, session, prid):
        return session.query(ProductSku.PSid).filter(ProductSku.PRid == prid).filter(ProductSku.PSstatus == 1).all()

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
        return self.session.query(ProductCategory.PAid, ProductCategory.PAname, ProductCategory.PAstatus).filter_by(Parentid=Parentid).filter_by(PAstatus=True).all()
    @close_session
    def get_first_product_category_status(self, Parentid):
        return self.session.query(ProductCategory.PAid, ProductCategory.PAname, ProductCategory.PAstatus).filter_by(Parentid=Parentid).filter_by(PAstatus=True).all()
    @close_session
    def get_first_product_category(self, Parentid):
        return self.session.query(ProductCategory.PAid, ProductCategory.PAname, ProductCategory.PAtype).filter_by(Parentid=Parentid).filter_by(PAstatus=True).all()
    @close_session
    def get_child_product_category(self, Parentid):
        return self.session.query(ProductCategory.PAid, ProductCategory.PAname, ProductCategory.Parentid).filter_by(Parentid=Parentid).filter_by(PAstatus=True).all()
    @close_session
    def get_product_category(self, PAid):
        return self.session.query(ProductCategory.PAstatus).filter_by(PAid=PAid).filter_by(PAstatus=True).all()
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

    @close_session
    def get_product_by_paid(self, paid):
        return self.session.query(Product.PRid).filter(Product.PAid == paid).all()

    @close_session
    def add_sowingmap(self, type, list):
        for i in list:
            pic = SowingMap()
            pic.SMid = str(uuid.uuid4())
            pic.SMurl = str(i)
            pic.SMstatus = True
            pic.SMtype = type
            self.session.add(pic)
        return True

    @close_session
    def get_sowingmap(self):
        return self.session.query(SowingMap.SMid, SowingMap.SMtype, SowingMap.SMurl)\
            .filter(SowingMap.SMstatus == 1).all()

    @close_session
    def update_sowingmap(self, smid):
        self.session.query(SowingMap).filter(SowingMap.SMid == smid).update({'SMstatus':False})
        return True

    @close_session
    def add_color(self, colorname, time):
        color = Color()
        color.COid = str(uuid.uuid4())
        color.COname = colorname
        color.COcreatetime = time
        self.session.add(color)
        return True

    @close_session
    def get_color_by_colorname(self, name):
        return self.session.query(Color).filter(Color.COname == name).first()

    @close_session
    def get_color_list(self):
        return self.session.query(Color.COid, Color.COname).order_by(Color.COcreatetime.desc()).all()

    @close_session
    def add_size(self, sizename, time):
        size = Size()
        size.SIid = str(uuid.uuid4())
        size.SIname = sizename
        size.SIcreatetime = time
        self.session.add(size)
        return True

    @close_session
    def get_color_by_sizename(self, name):
        return self.session.query(Size).filter(Size.SIname == name).first()

    @close_session
    def get_size_list(self):
        return self.session.query(Size.SIid, Size.SIname).order_by(Size.SIcreatetime.desc()).all()

    @close_session
    def add_shoppingcart(self, usid, data):
        cart = ShoppingCart()
        cart.SCid = str(uuid.uuid4())
        cart.USid = usid
        cart.PRid = data.get('prid')
        cart.PRname = data.get('prname')
        cart.PRprice = data.get('prprice')
        cart.PRlogisticsfee = data.get('prlogisticsfee')
        cart.PRpic = data.get('prpic')
        cart.PSid = data.get('psid')
        cart.colorid = data.get('colorid')
        cart.colorname = data.get('colorname')
        cart.sizeid = data.get('sizeid')
        cart.sizename = data.get('sizename')
        cart.number = data.get('number')
        cart.SCcreatetime = datetime.strftime(datetime.now(), format_for_db)
        self.session.add(cart)
        return True

    @close_session
    def get_product_info(self, id):
        return self.session.query(Product.PRid, Product.PRprice, Product.PAdiscountnum
                                  ).filter(Product.PRid == id).filter(Product.PRstatus == 1).first()

    @close_session
    def get_shoppingcart_product(self, id):
        return self.session.query(ShoppingCart.PRid).filter(ShoppingCart.USid == id).filter(ShoppingCart.SCstatus == 1)\
            .group_by(ShoppingCart.PRid).all()

    @close_session
    def get_shoppingcart_sku(self, usid, prid):
        return self.session.query(ShoppingCart.SCid, ShoppingCart.colorid, ShoppingCart.colorname, ShoppingCart.SCcreatetime\
            , ShoppingCart.sizeid, ShoppingCart.sizename, ShoppingCart.number, ShoppingCart.PSid, ShoppingCart.SCstatus)\
            .filter(ShoppingCart.USid == usid).filter(ShoppingCart.PRid == prid).filter(ShoppingCart.SCstatus == 1)\
            .order_by(ShoppingCart.SCcreatetime.desc()).all()

    @close_session
    def get_sku_status(self, psid):
        return self.session.query(ProductSku.PSstock).filter(ProductSku.PSid == psid).filter(ProductSku.PSstatus == 1).first()

    @close_session
    def get_sku_stock(self, psid):
        return self.session.query(ProductSku.PSstock, ProductSku.PSstatus).filter(ProductSku.PSid == psid).first()


    @close_session
    def check_is_exist_sku(self, usid, prid, psid):
        return self.session.query(ShoppingCart.number).filter(ShoppingCart.USid == usid).filter(ShoppingCart.PRid == prid)\
                           .filter(ShoppingCart.PSid == psid).filter(ShoppingCart.SCstatus == 1).first()

    @close_session
    def update_user_sku(self, usid, psid, update):
        self.session.query(ShoppingCart).filter(ShoppingCart.USid == usid).filter(ShoppingCart.PSid == psid).update(update)
        return True

    @close_session
    def update_user_sku_by_scid(self, session, usid, scid, update):
        session.query(ShoppingCart).filter(ShoppingCart.USid == usid).filter(ShoppingCart.SCid == scid).update(
            update)
        return True