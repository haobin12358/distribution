# *- coding:utf8 *-
# 兼容linux系统
import random
import sys
import os
import uuid
import model
import pymysql
from service.DBSession import db_session
from werkzeug.security import generate_password_hash
from sqlalchemy.orm import scoped_session, sessionmaker
sys.path.append(os.path.dirname(os.getcwd()))  # 增加系统路径

change_index = 10  # 循环中改变type的点
info_count = 22  # 需要插入的数据库条数


class MakeData():
    def __init__(self):
        # self.act = SActivity()
        self.session = scoped_session(sessionmaker(autocommit=False,
                                                   autoflush=False,
                                                   bind=model.mysql_engine))
        self.user_id = self.generic_uuid()
        self.activity_id = self.generic_uuid() 
        self.media_id = self.generic_uuid()
        self.comment_id = self.generic_uuid()
        self.tag_id = self.generic_uuid()
        self.banner_id = self.generic_uuid()
        self.product_id = self.generic_uuid()
        self.hotmessege_id = self.generic_uuid()
        self.topnav_id = self.generic_uuid()[:4]
        self.recommendbanner_id = self.generic_uuid()

    def generic_uuid(self):
        return [str(uuid.uuid4()) for i in range(info_count)]

    def add_super(self):
        # from WeiDian.models.model import SuperUser
        from werkzeug.security import generate_password_hash
        super = model.SuperUser()
        super.SUid = self.user_id[0]
        # super.SUid = '6882ad09-bf5f-4607-8ad1-1cd46b6158e0'
        super.header = '这是头像图片'
        super.SUname = '这是用户名称'
        super.SUpassword = generate_password_hash('hello')  # 密码是hello
        super.SUlevel = 1  # 级别为1, 管理员
        self.session.add(super)
        self.session.commit()



    def add_media(self):
        for i in self.media_id:
            media = model.ActivityMedia()
            media.AMid = str(i)
            media.ACid = random.choice(self.activity_id)
            tem = random.randint(1, 2)
            if tem == 1:
                media.AMimage = 'http://www.thisimage'
            else:
                is_exists = self.session.query(model.ActivityMedia).filter_by(ACid=media.ACid).first()
                if not is_exists:
                    media.AMvideo = 'http://www.thisvideo'
                else:
                    media.AMimage = 'http://www.thisimage1'
            media.AMsort = random.randint(1, 9)
            self.session.add(media)
            self.session.commit()


    def add_alreadyRead(self):
        from model import AlreadyRead
        for i in range(10):
            message = AlreadyRead()
            message.ARid = str(i) + "dfdef"
            message.USid = str(i+1) + "gfvfvd"
            self.session.add(message)
            self.session.commit()

    def add_product(self):
        from model import Product
        for i in range(20):
            product = Product()
            product.PRid = 'test' + str(i)
            product.PRname = '商品名' + str(i)
            product.PRpic = 'https://timgsa.baidu.com/timg?image&quality=80&size=b9999_10000&sec=1540919391&di=91c1ae656341d5814e63280616ad8ade&imgtype=jpg&er=1&src=http%3A%2F%2Fimg.zcool.cn%2Fcommunity%2F0169d55548dff50000019ae9973427.jpg%401280w_1l_2o_100sh.jpg'
            product.PRoldprice = i + 100
            product.PRstock = 1000 + i
            product.PRprice = i + 1
            import datetime
            from common.timeformat import format_for_db
            time_time = datetime.datetime.now()
            time_str = datetime.datetime.strftime(time_time, format_for_db)
            product.PRcreatetime = time_str
            product.PRlogisticsfee = i
            product.PRstatus = (i%3) + 1
            product.PAid = (i%7) + 4
            self.session.add(product)
            self.session.commit()

    def add_user(self):
        from model import User
        user = User()
        user.USid = '1204cf38-c3cf-401f-8ba7-f8ce040f064f'
        user.USname = '123'
        user.USphonenum = '12345678901'
        user.USwechat = 'wechat'
        user.USpassword = generate_password_hash('123')
        user.USbail = 0
        user.USmount = 10000
        user.idcardnum = '12345678909876512'
        user.USheadimg = 'https://timgsa.baidu.com/timg?image&quality=80&size=b9999_10000&sec=1540919391&di=91c1ae656341d5814e63280616ad8ade&imgtype=jpg&er=1&src=http%3A%2F%2Fimg.zcool.cn%2Fcommunity%2F0169d55548dff50000019ae9973427.jpg%401280w_1l_2o_100sh.jpg'
        self.session.add(user)
        self.session.commit()

    def add_user2(self):
        from model import User
        user = User()
        user.USid = '3404cf38-c3cf-401f-8ba7-f8ce040f064f'
        user.USname = 'guodong'
        user.USagentid = 2
        user.USwechat = 'wechat'
        user.USphonenum = '15058968546'
        user.USpassword = "123"
        user.USbail = 0
        user.USmount = 10000
        user.USheadimg = 'https://timgsa.baidu.com/timg?image&quality=80&size=b9999_10000&sec=1540919391&di=91c1ae656341d5814e63280616ad8ade&imgtype=jpg&er=1&src=http%3A%2F%2Fimg.zcool.cn%2Fcommunity%2F0169d55548dff50000019ae9973427.jpg%401280w_1l_2o_100sh.jpg'
        self.session.add(user)
        self.session.commit()

    def add_user3(self):
        from model import User
        for i in range(3):
            user = User()
            user.USid = 'rfesrgbrt34qw32thert4535g' + str(i)
            user.USname = 'guodongtest' + str(i)
            user.USphonenum = '1505896854' + str(i)
            user.USwechat = 'wechat'
            user.USpassword = "123"
            user.USagentid = 100 + int(i)
            user.USbail = 0
            user.USmount = 999999998.56
            user.USheadimg = 'https://timgsa.baidu.com/timg?image&quality=80&size=b9999_10000&sec=1540919391&di=91c1ae656341d5814e63280616ad8ade&imgtype=jpg&er=1&src=http%3A%2F%2Fimg.zcool.cn%2Fcommunity%2F0169d55548dff50000019ae9973427.jpg%401280w_1l_2o_100sh.jpg'
            user.USpre = '3404cf38-c3cf-401f-8ba7-f8ce040f064f'
            self.session.add(user)
            self.session.commit()

    def add_user4(self):
        from model import User
        for i in range(2):
            user = User()
            user.USid = 'rfesrgbrtthert4535g22222' + str(i)
            user.USname = 'guodongtest222' + str(i)
            user.USwechat = 'wechat'
            user.USphonenum = '1505896854' + str(i)
            user.USpassword = "123"
            user.USagentid = 106 + int(i)
            user.USbail = 0
            user.USmount = 10000
            user.USheadimg = 'https://timgsa.baidu.com/timg?image&quality=80&size=b9999_10000&sec=1540919391&di=91c1ae656341d5814e63280616ad8ade&imgtype=jpg&er=1&src=http%3A%2F%2Fimg.zcool.cn%2Fcommunity%2F0169d55548dff50000019ae9973427.jpg%401280w_1l_2o_100sh.jpg'
            user.USpre = 'rfesrgbrtthert4535g1'
            self.session.add(user)
            self.session.commit()

    def add_user5(self):
        from model import User
        user = User()
        user.USid = 'rfesrgbrtthert4535g2222233333'
        user.USname = 'guodongtest222333'
        user.USphonenum = '15058968549'
        user.USwechat = 'wechat'
        user.USagentid = 200
        user.USpassword = "123"
        user.USbail = 0
        user.USmount = 10000
        user.USheadimg = 'https://timgsa.baidu.com/timg?image&quality=80&size=b9999_10000&sec=1540919391&di=91c1ae656341d5814e63280616ad8ade&imgtype=jpg&er=1&src=http%3A%2F%2Fimg.zcool.cn%2Fcommunity%2F0169d55548dff50000019ae9973427.jpg%401280w_1l_2o_100sh.jpg'
        user.USpre = 'rfesrgbrtthert4535g222221'
        self.session.add(user)
        self.session.commit()


    def add_amount(self):
        from model import Amount
        amount = Amount()
        amount.AMid = 'rfesrgbrtwewthert4535geqw'
        amount.USid = '3404cf38-c3cf-401f-8ba7-f8ce040f064f'
        amount.USname = 'guodong'
        amount.USagentid = 123
        amount.USheadimg = 'https://timgsa.baidu.com/timg?image&quality=80&size=b9999_10000&sec=1540919391&di=91c1ae656341d5814e63280616ad8ade&imgtype=jpg&er=1&src=http%3A%2F%2Fimg.zcool.cn%2Fcommunity%2F0169d55548dff50000019ae9973427.jpg%401280w_1l_2o_100sh.jpg'
        amount.reward = 300
        amount.AMmonth = 201810
        amount.performance = 100000
        amount.AMcreattime = 20181010000000
        self.session.add(amount)
        self.session.commit()

    def add_amount2(self):
        from model import Amount
        amount = Amount()
        amount.AMid = 'rfesrgbrtthddert4535gfdsfs'
        amount.USid = 'rfesrgbrtthert4535g0'
        amount.USname = 'guodongtest0'
        amount.USagentid = 124
        amount.USheadimg = 'https://timgsa.baidu.com/timg?image&quality=80&size=b9999_10000&sec=1540919391&di=91c1ae656341d5814e63280616ad8ade&imgtype=jpg&er=1&src=http%3A%2F%2Fimg.zcool.cn%2Fcommunity%2F0169d55548dff50000019ae9973427.jpg%401280w_1l_2o_100sh.jpg'
        amount.reward = 100
        amount.AMmonth = 201810
        amount.performance = 1000
        amount.AMcreattime = 20181010000000
        self.session.add(amount)
        self.session.commit()

    def add_amount3(self):
        from model import Amount
        amount = Amount()
        amount.AMid = 'rfesrgbrtthddert45ewe335g'
        amount.USid = 'rfesrgbrtthert4535g1'
        amount.USname = 'guodongtest1'
        amount.USagentid = 125
        amount.USheadimg = 'https://timgsa.baidu.com/timg?image&quality=80&size=b9999_10000&sec=1540919391&di=91c1ae656341d5814e63280616ad8ade&imgtype=jpg&er=1&src=http%3A%2F%2Fimg.zcool.cn%2Fcommunity%2F0169d55548dff50000019ae9973427.jpg%401280w_1l_2o_100sh.jpg'
        amount.reward = 100
        amount.AMmonth = 201810
        amount.performance = 10
        amount.AMcreattime = 20181010000000
        self.session.add(amount)
        self.session.commit()

    def add_amount4(self):
        from model import Amount
        amount = Amount()
        amount.AMid = 'rfesrgbrtthdd11111ert4535g'
        amount.USid = 'rfesrgbrtthert4535g2'
        amount.USname = 'guodongtest2'
        amount.USagentid = 126
        amount.USheadimg = 'https://timgsa.baidu.com/timg?image&quality=80&size=b9999_10000&sec=1540919391&di=91c1ae656341d5814e63280616ad8ade&imgtype=jpg&er=1&src=http%3A%2F%2Fimg.zcool.cn%2Fcommunity%2F0169d55548dff50000019ae9973427.jpg%401280w_1l_2o_100sh.jpg'
        amount.reward = 100
        amount.AMmonth = 201810
        amount.performance = 100
        amount.AMcreattime = 20181010000000
        self.session.add(amount)
        self.session.commit()

    def add_amount5(self):
        from model import Amount
        amount = Amount()
        amount.AMid = 'rfesrgbrtthert4535g222220234233'
        amount.USid = 'rfesrgbrtthert4535g222220'
        amount.USname = 'guodongtest2220'
        amount.USagentid = 127
        amount.USheadimg = 'https://timgsa.baidu.com/timg?image&quality=80&size=b9999_10000&sec=1540919391&di=91c1ae656341d5814e63280616ad8ade&imgtype=jpg&er=1&src=http%3A%2F%2Fimg.zcool.cn%2Fcommunity%2F0169d55548dff50000019ae9973427.jpg%401280w_1l_2o_100sh.jpg'
        amount.reward = 100
        amount.AMmonth = 201810
        amount.performance = 1000
        amount.AMcreattime = 20181010000000
        self.session.add(amount)
        self.session.commit()

    def add_amount6(self):
        from model import Amount
        amount = Amount()
        amount.AMid = 'rfesrgbrtthert4535g22222023vf4233'
        amount.USid = 'rfesrgbrtthert4535g222221'
        amount.USname = 'guodongtest2221'
        amount.USagentid = 128
        amount.USheadimg = 'https://timgsa.baidu.com/timg?image&quality=80&size=b9999_10000&sec=1540919391&di=91c1ae656341d5814e63280616ad8ade&imgtype=jpg&er=1&src=http%3A%2F%2Fimg.zcool.cn%2Fcommunity%2F0169d55548dff50000019ae9973427.jpg%401280w_1l_2o_100sh.jpg'
        amount.reward = 100
        amount.AMmonth = 201810
        amount.performance = 10000
        amount.AMcreattime = 20181010000000
        self.session.add(amount)
        self.session.commit()

    def add_amount7(self):
        from model import Amount
        amount = Amount()
        amount.AMid = 'rfesrgbrtthert4535g22222023vf423355'
        amount.USid = 'rfesrgbrtthert4535g2222233333'
        amount.USname = 'guodongtest222333'
        amount.USagentid = 129
        amount.USheadimg = 'https://timgsa.baidu.com/timg?image&quality=80&size=b9999_10000&sec=1540919391&di=91c1ae656341d5814e63280616ad8ade&imgtype=jpg&er=1&src=http%3A%2F%2Fimg.zcool.cn%2Fcommunity%2F0169d55548dff50000019ae9973427.jpg%401280w_1l_2o_100sh.jpg'
        amount.reward = 100
        amount.AMmonth = 201810
        amount.performance = 1000
        amount.AMcreattime = 20181010000000
        self.session.add(amount)
        self.session.commit()

    def add_DiscountRuler(self):
        from model import DiscountRuler
        for i in range(5):
            ruler = DiscountRuler()
            ruler.DRid = 'afrewgtrhb' + str(i)
            ruler.DRnumber = 5 + pow(100, int(i))
            ruler.DRratio = 2 + int(i)
            self.session.add(ruler)
            self.session.commit()


    def add_superuser(self):
        from model import Admin
        admin = Admin()
        admin.ADid = '3404cf38-c3cf-401f-8ba7-f8ce040f064f'
        admin.ADnum = '123'
        admin.ADpassword = generate_password_hash('123')
        admin.ADname = 'test'
        admin.ADlevel = 1
        admin.ADheaderimg = 'https://timgsa.baidu.com/timg?image&quality=80&size=b9999_10000&sec=1540919391&di=91c1ae656341d5814e63280616ad8ade&imgtype=jpg&er=1&src=http%3A%2F%2Fimg.zcool.cn%2Fcommunity%2F0169d55548dff50000019ae9973427.jpg%401280w_1l_2o_100sh.jpg'
        self.session.add(admin)
        self.session.commit()

    def add_agent_message(self):
        from model import AgentMessage
        from werkzeug.security import generate_password_hash
        for i in range(30):
            message = AgentMessage()
            message.USid = '3404cf38-c3cf-401f-8ba7-f8ce040f064f'
            message.AMtype = 0
            message.AMcontent = "hh" + str(i)
            message.AMid = "ewrw" + str(i)
            import datetime
            from common.timeformat import format_for_db
            time_time = datetime.datetime.now()
            time_str = datetime.datetime.strftime(time_time, format_for_db)
            message.AMdate = time_str
            self.session.add(message)
            self.session.commit()

    def add_province(self):
        from model import Province
        province = Province()
        province.id = 1
        province.provincename = '浙江'
        province.provinceid = "1"
        self.session.add(province)
        self.session.commit()

    def add_city(self):
        from model import City
        city = City()
        city.id = 2
        city.cityname = "杭州"
        city.cityid = "2"
        city.provinceid = "1"
        self.session.add(city)
        self.session.commit()

    def add_area(self):
        from model import Area
        area = Area()
        area.id = 3
        area.areaname = "滨江区"
        area.areaid = "3"
        area.cityid = "2"
        self.session.add(area)
        self.session.commit()

    def add_company_message(self):
        from model import ComMessage
        from werkzeug.security import generate_password_hash
        for i in range(30):
            message = ComMessage()
            message.CMid = '4304cf38-c3cf-401f-8ba7-f8ce040f064f' + str(i)
            message.CMstatus = 1
            message.CMtitle = "hh" + str(i)
            message.CMtype = 0
            message.CMfile = "https://www.hzmyo.cn/ued/php/upload/20181011/1539237187747826.pdf"
            import datetime
            from common.timeformat import format_for_db
            time_time = datetime.datetime.now()
            time_str = datetime.datetime.strftime(time_time, format_for_db)
            message.CMdate = time_str
            self.session.add(message)
            self.session.commit()

    
    def add_user_partner(self):
        from model import User
        from werkzeug.security import generate_password_hash
        user = User()
        user.USid = 'jfksadjf-fdaslkjf-3213-31231'
        user.USname = 'part'
        user.USpassword = generate_password_hash('pass')
        user.USlevel = 2 
        self.session.add(user)
        self.session.commit()
    # def update_activity(self, ):

    #
    # def add_shops(self, tshop_ids):
    #     for i in range(info_count):
    #         shop_model = model.Shops()
    #         shop_model.Sid = tshop_ids[i]
    #         shop_model.Sname = "test{0}".format(i)
    #         shop_model.Sreview = "5"
    #         shop_model.Sdetail = "包子，粥，面条"
    #         shop_model.Simage = "http://www.baidu.com"
    #         shop_model.Stel = "135880461%02d" % i
    #         self.shop.add_shop(shop_model)
    #
    # def add_conpons(self, conid):
    #     for i in range(info_count):
    #         self.cou.add_coupons(**{
    #             "COid": i,
    #             "COfilter": float("1%02d.00" % i),
    #             "COdiscount": 0.2,
    #             "COamount": 10.1,
    #             "COstart": "2018011421%02d00" % i,
    #             "COend": "2018041421%02d00" % i
    #         })

    def add_test(self):
        from model import Test
        for i in range(3):
            test = Test()
            test.name='fengxin'
            self.session.add(test)
            self.session.commit()


class databse_deal():
    def __init__(self):
        self.conn = pymysql.connect(
            host=model.cfg.host, user=model.cfg.username,
            passwd=model.cfg.password, charset=model.cfg.charset)
        self.cursor = self.conn.cursor()

    def create_database(self):
        sql = "create database if not exists {0} DEFAULT CHARACTER SET 'utf8' COLLATE 'utf8_general_ci' ;".format(
            model.cfg.database)
        print sql
        try:
            self.cursor.execute(sql)
        except Exception as e:
            print(e)
        finally:
            self.conn_close()

    def drop_database(self):
        sql = "drop database if exists {0} ;".format(
            model.cfg.database)
        print sql
        try:
            self.cursor.execute(sql)
        except Exception as e:
            print(e)

        finally:
            self.conn_close()

    def conn_close(self):
        self.conn.close()


def create():
    # databse_deal().create_database()
    from model import Base
    Base.metadata.create_all(model.mysql_engine)


def drop():
    databse_deal().drop_database()


if __name__ == "__main__":
    print("start")
    '''
       运行该文件就可以在对应的数据库里生成本文件声明的所有table
       如果需要清除数据库，输入drop
       如果需要创建数据库 输入任意不包含drop的字符
       '''
    action = raw_input("create database?")
    if "drop" in action:
        drop()


    else:
        databse_deal().create_database()
        create()
        data = MakeData()
        # data.add_test()
        # print "OK!"
        # print('start add data')
        data.add_superuser()
        data.add_user()
        # data.add_user2()
        # data.add_user3()
        # data.add_user4()
        # data.add_user5()
        # data.add_agent_message()
        # data.add_company_message()
        # data.add_alreadyRead()
        # data.add_product()
        # data.add_amount()
        # data.add_amount2()
        # data.add_amount3()
        # data.add_amount4()
        # data.add_amount5()
        # data.add_amount6()
        # data.add_amount7()
        # data.add_DiscountRuler()
