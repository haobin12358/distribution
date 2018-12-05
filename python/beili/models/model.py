# -*- coding:utf8 -*-
import sys
import os
sys.path.append(os.path.dirname(os.getcwd()))
from sqlalchemy import Column, create_engine, Integer, String, Text, Float, Boolean, orm, DECIMAL
from config import dbconfig as cfg
from sqlalchemy.ext.declarative import declarative_base
# from models.base_model import Base, auto_createtime

DB_PARAMS = "{0}://{1}:{2}@{3}/{4}?charset={5}".format(
    cfg.sqlenginename,
    cfg.username,
    cfg.password,
    cfg.host,
    cfg.database,
    cfg.charset)
print(DB_PARAMS)
mysql_engine = create_engine(DB_PARAMS, echo=False)
Base = declarative_base()

class User(Base):
    """
    普通用户
    """
    __tablename__ = 'user'
    USid = Column(String(64), primary_key=True,)
    USname = Column(String(64), nullable=False)  # 用户名
    USpassword = Column(String(255))             # 密码
    USphonenum = Column(String(16), nullable=False)  # 手机号
    USagentid = Column(String(64))  # 代理编号
    USheadimg = Column(String(255))              # 头像
    USbail = Column(Float)                       # 保证金余额
    USmount = Column(Float)                      # 账户余额
    USpre = Column(String(64))                   # 上级代理id
    UScreatetime = Column(String(14))            # 创建时间
    authorization = Column(String(512))          # 认证书url
    USwechat = Column(String(64))                # 用户微信号,暂时不用
    idcardnum = Column(String(20))               # 身份证号
    openid = Column(String(64))                  # 微信唯一值
    state = Column(String(128))                  # 用于获取openid
    unionid = Column(String(255))                # 绑定公众号会出现,暂时不用
    accesstoken = Column(String(255))            # 微信token,暂时不用
    subscribe = Column(Integer)                  # 是否关注公众号,暂时不用

class Admin(Base):
    """
    管理员
    """
    __tablename__ = 'admin'
    ADid = Column(String(64), primary_key=True)
    ADnum = Column(String(64), nullable=False)  # 管理员账号
    ADname = Column(String(64), nullable=False)  # 管理员用户名
    ADpassword = Column(String(255), nullable=False)  # 密码
    ADheaderimg = Column(String(255))  # 用户头像, 可以设置一个默认值
    ADlevel = Column(Integer, default=0)  # 用户级别{0: 一般管理员, 1: 超级管理员}　
    ADcreatetime = Column(String(14))  # 创建时间
    ADisfreeze = Column(Boolean, default=False)  # 是否被冻结
    #ADisdelete = Column(Boolean, default=False)  # 是否被删除



class ProductCategory(Base):
    """
    商品分类
    """
    __tablename__ = 'productcategory'
    PAid = Column(String(64), primary_key=True)
    PAname = Column(String(16))  # 类别名
    PAtype = Column(Integer)  # 类目级别{1 一级分类, 2 二级分类, 3 三级分类}
    Parentid = Column(String(64), default='0')  # 父类别id, 默认0
    #PAstatus = Column(Boolean)  # True能用 False不可用
    PAstatus = Column(Boolean, default=True)  # True能用 False不可用

class Product(Base):
    """
    商品表
    """
    __tablename__ = 'product'
    PRid = Column(String(64), primary_key=True)
    PRname = Column(String(64), nullable=False)  # 名称
    PRpic = Column(String(255))  # 商品图片
    PRoldprice = Column(Float)  # 原价
    PRprice = Column(Float, nullable=False)  # 显示价格
    PRcreatetime = Column(String(14))  # 创建时间
    PRlogisticsfee = Column(Float)  # 物流费
    PRstatus = Column(Integer)     # 商品状态，1出售中，2已售罄，3已下架
    PAid = Column(String(64))      # 分类id，用于绑定商品类目，空值表示未绑定分类
    PAdiscountnum = Column(Float,default=1)  # 折扣件数
    sowingmap = Column(Text)  # 轮播图
    detailpics = Column(Text)  # 详情图

class ProductSku(Base):
    """
    商品sku表，一个商品对应着多个sku
    """
    __tablename__ = 'productsku'
    PSid = Column(String(64), primary_key=True)
    PRid = Column(String(64))  # 商品id
    colorid = Column(String(64))  # 颜色id
    colorname = Column(String(64))  # 颜色名称
    sizeid = Column(String(64))  # 尺码id
    sizename = Column(String(64))  # 尺码名称
    PSstock = Column(Integer)  # 库存
    PScreatetime = Column(String(14))  # 创建时间
    PSstatus = Column(Integer)   # 状态

class Color(Base):
    """
    颜色表
    """
    __tablename__ = 'color'
    COid = Column(String(64), primary_key=True)
    COname = Column(String(64))  # 颜色名称
    COcreatetime = Column(String(14))  # 记录创建时间

class Size(Base):
    """
    尺码表
    """
    __tablename__ = 'size'
    SIid = Column(String(64), primary_key=True)
    SIname = Column(String(64))  # 尺码名称
    SIcreatetime = Column(String(14))  # 记录创建时间

class ShoppingCart(Base):
    """
    购物车
    """
    __tablename__ = 'shoppingcart'
    SCid = Column(String(64), primary_key=True)
    USid = Column(String(64))  # 用户id
    PRid = Column(String(64))  # 商品id
    PSid = Column(String(64))  # skuid
    colorid = Column(String(64))  # 颜色id
    colorname = Column(String(64))  # 颜色名称
    sizeid = Column(String(64))  # 尺码id
    sizename = Column(String(64))  # 尺码名称
    number = Column(Integer)  # 商品数量
    SCcreatetime = Column(String(14))  # 记录创建时间
    SCstatus = Column(Integer, default=1)  # 状态 0.用户已删除 1.在售 2.库存不足 3.商品规格发生变化 4.商品已下架

class OrderInfo(Base):
    """订单信息"""
    __tablename__ = 'orderinfo'
    OIid = Column(String(64), primary_key=True)
    OIsn = Column(String(64))  # 订单号
    USid = Column(String(64))  # 用户id
    """
    订单状态: {0:所有订单, 1:待发货, 2:已发货, 3:交易完成, 4:分拣中 5:已取消} 根据需求无待支付状态
    """
    OIstatus = Column(Integer, default=1)
    OInote = Column(String(255))  # 订单留言
    OImount = Column(Float)  # 金额
    UAid = Column(String(255), nullable=False)  # 地址id
    OIcreatetime = Column(String(14))  # 订单创建时间
    OIlogisticsfee = Column(Float)  # 订单运费
    username = Column(String(64))  # 联系人
    userphonenum = Column(String(64))  # 电话号码
    provincename = Column(String(64))  # 省
    cityname = Column(String(64))  # 市
    areaname = Column(String(64))  # 区
    details = Column(String(255))  # 详细地址
    expressname = Column(String(64))  # 快递名称
    expressnum = Column(String(64))  # 快递单号
    productnum = Column(Integer, default=0)  # 商品数量
    discountnum = Column(float)  # 返点数量

class OrderProductInfo(Base):
    """订单商品详情, 多个订单商品详情对应一个订单"""
    __tablename__ = 'orderproductinfo'
    OPIid = Column(String(64), primary_key=True)
    OIid = Column(String(64), nullable=False)  # 订单
    PRid = Column(String(64), nullable=False)  # 商品id
    PRprice = Column(Float, nullable=False)   # 商品价格(购买时候的价格)
    PRname = Column(String(64))  # 商品的名字(购买之时的)
    PRimage = Column(String(255))  # 商品主图

class OrderSkuInfo(Base):
    """
    订单sku详情，
    """
    __tablename__ = 'orderskuinfo'
    OSIid = Column(String(64), primary_key=True)
    OPIid = Column(String(64))  # 对应的订单商品详情id
    colorname = Column(String(64))  # 颜色名称
    sizename = Column(String(64))  # 尺码名称
    number = Column(Integer)  # 购买数量

class BailRecord(Base):
    """
    保证金操作记录表
    """
    __tablename__ = 'bailrecord'
    BRid = Column(String(64), primary_key=True)
    USid = Column(String(64))  # 用户id
    BRtype = Column(Integer)  # 记录类型 1充值 2退还
    BRmount = Column(Float)  # 交易金额
    BRstatus = Column(Integer)  # 状态，1，已充值 2，退还中 3，已退还 4,退还失败
    BRtradenum = Column(String(30))  # 流水号
    BRcreatetime = Column(String(14))  # 创建日期



class InvitaRecord(Base):
    """
    邀请记录详情(人工审核)
    """
    __tablename__ = 'invitarecord'
    IRIid = Column(String(64), primary_key=True)
    IRIprename = Column(String(64))  # 邀请人姓名
    IRIprephonenum = Column(String(64))  # 邀请人电话号码
    IRIname = Column(String(64))  # 被邀请人姓名
    IRIphonenum = Column(String(64))  # 被邀请人电话号码
    IRIpassword = Column(String(64))  # 被邀请人密码
    IRIidcardnum = Column(String(64))  # 被邀请人身份证号码
    IRIwechat = Column(String(64))   # 被邀请人微信号
    IRIcity = Column(String(64))  # 被邀请人城市id
    IRIarea = Column(String(64))  # 被邀请人区县id
    IRIaddress = Column(String(64))  # 被邀请人详细地址
    IRIpaytype = Column(String(64))  # 打款方式: {1: 支付宝, 2:银行转账}
    IRIpayamount = Column(String(64))  # 付款金额
    IRIpaytime = Column(String(14))  # 打款时间
    IRIpic = Column(String(255))  # 被邀请人头像
    IRIproof = Column(String(512))  # 被邀请人凭证
    IRIalipaynum = Column(String(64))  # 支付宝账户
    IRIbankname = Column(String(64))  # 开户银行
    IRIaccountname = Column(String(64))  # 银行户名
    IRIcardnum = Column(String(64))  # 银行卡号
    IRIstatus = Column(String(64))  # 邀请状态:{1:待审核, 2:审核通过, 3:审核不通过}
    IRIcreatetime = Column(String(14))  # 记录创建时间

class Qrcode(Base):
    """
    二维码记录表
    """
    __tablename__ = 'qrcode'
    QRid = Column(String(64), primary_key=True)
    USid = Column(String(64))  # 用户id
    QRovertime = Column(String(64))  # 过期时间
    QRnumber = Column(String(64))  # 使用次数
    QRstatus = Column(Integer, default=1)  #1 可用

class MoneyRecord(Base):
    """
    收支记录表
    """
    __tablename__ = 'moneyrecord'
    MRid = Column(String(64), primary_key=True)
    USid = Column(String(64))
    MRtype = Column(Integer)  # {1,订单支出 2,提现 3,充值保证金 4,余额充值 5,奖金发放 6,保证金退还 7，提现失败 8, 取消订单}
    MRamount = Column(Float)  # 金额
    OIid = Column(String(30))  # 订单号
    MRtradenum = Column(String(30))  # 流水号
    MRcreatetime = Column(String(14))  # 创建日期


class ChargeMoney(Base):
    """
    充值记录表
    """
    __tablename__ = 'chargemoney'
    CMid = Column(String(64), primary_key=True)
    USid = Column(String(64))  # 用户
    CMpaytype = Column(Integer)  # 充值方式:{1:支付宝, 2:银行转账}
    CMalipaynum = Column(String(64))  # 支付宝账户
    CMbankname = Column(String(64))  # 银行名称
    CMaccountname = Column(String(64))  # 开户名称
    CMcardnum = Column(String(64))  # 银行卡卡号
    CMamount = Column(Float)  # 充值金额
    CMpaytime = Column(String(14))  # 充值日期
    CMcreatetime = Column(String(14))  # 创建时间
    CMremark = Column(String(255))  # 充值备注
    CMstatus = Column(Integer)  # 提现状态:{0:全部, 1:待审核, 2:已充值, 3:未通过}
    CMtradenum = Column(String(64))  # 流水号
    CMproof = Column(String(512))  # 打款凭证
    CMreason = Column(Text)  # 理由

class Reward(Base):
    """
    直推奖励记录表
    """
    __tablename__ = 'reward'
    REid = Column(String(64), primary_key=True)
    RElastuserid = Column(String(64))  # 推荐用户id
    REnextuserid = Column(String(64))  # 被推荐用户id
    REmount = Column(Float)  # 奖励金额
    REmonth = Column(String(6))  # 月份
    REcreatetime = Column(String(14))  # 记录创建时间

class Performance(Base):
    """
    个人业绩记录表
    """
    __tablename__ = 'performance'
    PEid = Column(String(64), primary_key=True)
    USid = Column(String(64))
    PEdiscountnum = Column(Integer)  # 销售折扣件数
    REmonth = Column(String(6))  # 月份
    PEcreatetime = Column(String(14))  # 记录创建时间

class Amount(Base):
    """
    直推奖励，销售折扣，业绩记录表，一个用户一个月只有一条数据
    """
    __tablename__ = 'amount'
    AMid = Column(String(64), primary_key=True)
    USid = Column(String(64), nullable=False)
    USname = Column(String(64))  # 用户名
    USagentid = Column(String(64))
    USheadimg = Column(String(255))  # 头像
    reward = Column(Float, default=0)  # 直推奖励金额
    performance = Column(Float, default=0)  # 业绩总额,就是总件数
    AMmonth = Column(String(6))  # 月份
    AMstatus = Column(Integer)  # 状态:{0: 所有状态 1:未打款 2:已打款}
    AMtradenum = Column(String(30))  # 流水号
    AMcreattime = Column(String(14))  # 记录创建时间

class DiscountRuler(Base):
    """
    折扣规则表
    """
    __tablename__ = 'discountruler'
    DRid = Column(String(64), primary_key=True)
    DRnumber = Column(Float)  # 数量
    DRmoney = Column(Float)  # 折扣金额

class WeixinCharge(Base):
    """
    微信线上充值记录表(如果需要)
    """
    __tablename__ = 'weixincharge'
    WCid = Column(String(64), primary_key=True)
    USid = Column(String(64))  # 用户
    WCamount = Column(Float)  # 充值金额
    WCopenid = Column(String(125))  # 充值微信账户
    WCstatus = Column(Integer)  # 记录状态: {0: 全部, 1:未支付 2: 充值成功, 3: 充值失败}
    WCpaytime = Column(String(14))  # 充值时间
    WCsn = Column(String(125))  # 交易号

class DrawMoney(Base):
    """
    银行卡线下提现记录表
    """
    __tablename__ = 'drawmoney'
    DMid = Column(String(64), primary_key=True)
    USid = Column(String(64))  # 用户id
    DMamount = Column(Float)  # 提现金额
    DMbankname = Column(String(64), nullable=False)     # 银行名称
    DMbranchname = Column(String(64), nullable=False)     # 支行名称
    DMcardnum = Column(String(19), nullable=False)      # 银行卡号
    DMaccountname = Column(String(64), nullable=False)     # 开户名称
    DMstatus = Column(Integer)  # 提现状态: {0: 全部, 1: 待审核, 2: 待打款, 3: 已打款 4: 未通过}
    DMcreatetime = Column(String(14))  # 创建时间
    DMtradenum = Column(String(125))  # 交易号, (如果有)
    DMreason = Column(Text)  # 理由

class AgentMessage(Base):
    """
    代理消息表
    """
    __tablename__ = 'agentmessage'
    AMid = Column(String(64), primary_key=True)
    USid = Column(String(64))  # 用户
    AMdate = Column(String(64))  # 消息发布时间
    AMtype = Column(Integer)  # 种类: {0: 订单信息, 1: 款项消息, 2: 代理信息}
    AMcontent = Column(String(128), nullable=False)  # 消息详情

class ComMessage(Base):
    """
    公司消息表
    """
    __tablename__ = 'commessage'
    CMid = Column(String(64), primary_key=True)
    CMdate = Column(String(64))  # 消息发布时间
    CMtype = Column(Boolean)  # 种类: {0: 公告}
    CMtitle = Column(String(128), nullable=False)  # 消息详情
    CMfile = Column(String(255), nullable=False)  # 附加图片
    CMstatus = Column(Integer, default=1)  # 状态: {0:显示, 1:删除 }

class Question(Base):
    """
    问题反馈记录表
    """
    __tablename__ = 'question'
    QUid = Column(String(64), primary_key=True)
    QUdate = Column(String(64))  # 反馈问题时间
    QUtext = Column(String(255), nullable=False)  # 问题详情

class Province(Base):
    """省"""
    __tablename__ = 'province'
    id = Column(Integer, primary_key=True, autoincrement=True)
    provincename = Column(String(20), nullable=False)
    provinceid = Column(String(8), nullable=False)


class City(Base):
    """市"""
    __tablename__ = 'city'
    id = Column(Integer, primary_key=True)
    cityid = Column(String(8), nullable=False)
    cityname = Column(String(20), nullable=False)
    provinceid = Column(String(8), nullable=False)


class Area(Base):
    """区县"""
    __tablename__ = 'area'
    id = Column(Integer, primary_key=True)
    areaname = Column(String(20), nullable=False)
    areaid = Column(String(8), nullable=False)
    cityid = Column(String(8), nullable=False)


class UserAddress(Base):
    """用户收货地址"""
    __tablename__ = 'useraddress'
    UAid = Column(String(64), primary_key=True)
    USid = Column(String(64), nullable=False)           # 用户
    UAname = Column(String(16), nullable=False)         # 收货人姓名
    UAphonenum = Column(String(16), nullable=False)     # 收货人电话
    UAdetails = Column(String(255), nullable=False)     # 具体地址
    UAdefault = Column(Boolean)          # 默认收获地址 1为默认
    UAstatus = Column(Boolean, default=True)           # 状态:{True: 在使用, False: 已删除}
    UAcreatetime = Column(String(14))                   # 创建时间
    areaid = Column(String(8))          # 关联的区域id
    cityid = Column(String(8))                          # 关联的城市id，没有区域id时有用

class IdentifyingCode(Base):
    """验证码"""
    __tablename__ = "identifyingcode"
    ICid = Column(String(64), primary_key=True)
    ICphonenum = Column(String(14), nullable=False)  # 获取验证码的手机号
    ICcode = Column(String(8), nullable=False)    # 获取到的验证码
    ICtime = Column(String(14), nullable=False)    # 获取的时间，格式为20180503100322

class AlreadyRead(Base):
    """
    已读消息记录表
    """
    __tablename__ = 'alreadyread'
    ARid = Column(String(64), primary_key=True)  # 已读消息id
    ARmessageid = Column(String(64))  # 消息id
    USid = Column(String(64))  # 已读消息用户id

class SowingMap(Base):
    """
    轮播图列表
    """
    __tablename__ = 'sowingmap'
    SMid = Column(String(64),primary_key=True) 
    SMurl = Column(String(512))  # url
    SMtype = Column(Integer)  # 轮播图类型 1，个人中心  2，商城
    SMstatus = Column(Boolean, default=False)  # True表示被获取了，False表示未被获取


class Comments(Base):
    """
    评论
    """
    __tablename__ = 'comments'
    CMid = Column(String(64), primary_key=True)
    USid = Column(String(64))
    USname = Column(String(64), nullable=False)  # 用户名
    USphonenum = Column(String(11))  # 用户手机号
    CMcontent = Column(String(512))  # 用户评论内容
    CMcreatetime = Column(String(14))  # 评论创建创建时间
    CMstatus = Column(Integer, default=1)  # 1未处理 2已处理

# class Test(Base):
#     __tablename__ = 'test'
#     id = Column(Integer, primary_key=True, autoincrement=True)
#     name = Column(String(32))

# Base.metadata.create_all(mysql_engine)