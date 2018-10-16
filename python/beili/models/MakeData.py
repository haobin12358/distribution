# *- coding:utf8 *-
# 兼容linux系统
import random
import sys
import os
import uuid
import model
import pymysql
from sqlalchemy.orm import scoped_session, sessionmaker
sys.path.append(os.path.dirname(os.getcwd()))  # 增加系统路径

change_index = 10  # 循环中改变type的点
info_count = 22  # 需要插入的数据库条数


class MakeData():
    def __init__(self):
#        self.act = SActivity()
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

    def add_activity(self):
        for i in self.activity_id:
            activity_model = model.Activity()
            activity_model.ACid = str(i)
            activity_model.ACtype = "2"
            activity_model.ACtext = "活动活动活动" + str(i)
            activity_model.ACbrowsenum = random.randint(10, 200)
            activity_model.AClikeFakeNum = random.randint(10, 200)
            activity_model.ACstarttime = str(random.randint(2017, 2019))+'0510000000'
            activity_model.ACendtime = str(random.randint(2017, 2019))+'0510000000'
            activity_model.PRid = random.choice(self.product_id)
            activity_model.SUid = self.user_id[0]
            activity_model.TopnavId = random.choice(self.topnav_id)
            self.session.add(activity_model)
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

    def add_comment(self):
        from model import ActivityComment
        for i in self.comment_id:
            comment = ActivityComment()
            comment.ACOid = str(i)
            tem = random.randint(1, 2)
            comment.ACid = random.choice(self.activity_id)
            comment.ACtext = '这是评论' + str(i)
            if tem == 1:
                comment.ACOparentid = str(random.randint(0, info_count))
                comment.ACtext = '这是回复' + str(i)
            comment.USid = 'this is usid'
            self.session.add(comment)
            self.session.commit()




    def add_product(self):
        from model import Product
        for i in self.product_id:
            pr = Product()
            pr.PRid = str(i)
            pr.USid = self.user_id[0]
            pr.PAid = str(random.randint(1, 10))
            pr.PRalias = '这是别名' + str(i)
            pr.PRscore = random.randint(1, 10)
            pr.PRsalesvolume = random.randint(0, info_count)
            pr.PRstock = random.randint(0, info_count)
            pr.PRmainpic = '这是主图' + str(i)
            pr.PRname = '这是商品名字' + str(i)
            pr.PRdetail = '这是一个超级大的文本'
            pr.PRtitle = '{hello 这是一个标题'
            pr.PRoldprice = 100.25
            pr.PRsalesvolume = 100
            pr.SUid = 'suid'
            pr.PRprice = random.randint(1, 999)
            self.session.add(pr)
            self.session.commit()

    def add_banner(self):
        from model import Banner
        for i in self.banner_id:
            ba = Banner()
            ba.BAid = str(i)
            ba.ACid = random.choice(self.activity_id)
            ba.BAsort = random.randint(1, 300)
            ba.BAstarttime = str(random.randint(2017, 2019))+'0510000000'
            ba.BAendtime = str(random.randint(2017, 2019))+'0510000000'
            ba.BAimage = '这是轮播图片' + str(i)
            self.session.add(ba)
            self.session.commit()

    def add_recommendbanner(self):
        from model import RecommendBanner
        for i in self.recommendbanner_id:
            rb = RecommendBanner()
            rb.RBid = str(i)
            rb.prid = random.choice(self.product_id)
            rb.RBsort = random.randint(1, 50)
            rb.RBstarttime = str(random.randint(2017, 2019))+'0510000000'
            rb.RBendtime = str(random.randint(2017, 2019))+'0510000000'
            rb.RBimage = '商品轮播图片' + str(i)
            self.session.add(rb)
            self.session.commit()

    def add_user(self):
        from model import User
        from werkzeug.security import generate_password_hash
        user = User()
        user.USid = '4304cf38-c3cf-401f-8ba7-f8ce040f064f'
        user.USname = 'name'
        user.USphonenum = '13511112222'
        user.USpassword = "123"
        self.session.add(user)
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
    from base_model import Base
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
        create()
        data = MakeData()
        data.add_user()
        print "OK!"
        # # tshop_ids = data.make_id()
        # # print("over")
        # data.add_activity()
        # data.add_media()
        # data.add_comment()
        # data.add_tags()
        # data.add_hotmessage()
        # data.add_banner()
        # data.add_product()
        # data.add_super()
        # data.add_recommendbanner()
        # data.add_user_partner()
