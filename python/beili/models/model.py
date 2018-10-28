# -*- coding:utf8 -*-
import sys
import os
sys.path.append(os.path.dirname(os.getcwd()))
from sqlalchemy import Column, create_engine, Integer, String, Text, Float, Boolean, orm
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
    USid = Column(String(64), primary_key=True)
    USname = Column(String(64), nullable=False)  # 用户名
    USpassword = Column(String(255))             # 密码
    USphonenum = Column(String(16), nullable=False)  # 手机号
    USheadimg = Column(String(255))               # 头像
    USbail = Column(Float)                       # 保证金余额
    USmount = Column(Float)                      # 账户余额
    USpre = Column(String(64))                   # 上级代理id
    openid = Column(String(64))                  # 微信唯一值
    unionid = Column(String(255))                # 绑定公众号会出现
    accesstoken = Column(String(255))            # 微信token
    subscribe = Column(Integer)                  # 是否关注公众号

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
    ADisdelete = Column(Boolean, default=False)  # 是否被删除


class ProductCategory(Base):
    """
    商品分类
    """
    __tablename__ = 'productcategory'
    PAid = Column(String(64), primary_key=True)
    PAname = Column(String(16))  # 类别名
    PAtype = Column(Integer)  # 类目级别{1 一级分类, 2 二级分类, 3 三级分类}
    Parentid = Column(String(64), default=0)  # 父类别id, 默认0

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
    PRstock = Column(Integer)  # 库存
    PRprofit = Column(Integer)  # 每件的收益，即销售折扣
    PRcreatetime = Column(String(14))  # 创建时间
    PRlogisticsfee = Column(Float)  # 物流费
    PRstatus = Column(Integer)     # 商品状态，1出售中，2已售罄，3已下架
    PAid = Column(String(64))      # 分类id，用于绑定商品类目，空值表示未绑定分类

class InvitaLink(Base):
    """
    邀请链接
    """
    __tablename__ = 'invitalink'
    ILid = Column(String(64), primary_key=True)
    USid = Column(String(64))  # 用户id
    ILpic = Column(String(255))  # 邀请链接二维码图片地址
    ILcreatetime = Column(String(14))  # 创建时间
    ILendtime = Column(String(14))  # 失效时间
    ILtimes = Column(String(64))  # 有效次数

    """
class InvitaRecordInfo(Base):
    
    邀请记录详情(人工审核)
    
    __tablename__ = 'invitarecordinfo'
    IRIid = Column(String(64), primary_key=True)
    ILid = Column(String(64))  # 邀请链接id
    IRIname = Column(String(64))  # 被邀请人姓名
    IRIphonenum = Column(String(64))  # 被邀请人电话号码
    IRIpassword = Column(String(64))  # 被邀请人秘密
    IRIwechat = Column(String(64))   # 被邀请人微信号
    IRIcountry = Column(String(64))  # 被邀请人国家及地区
    IRIprovince = Column(String(64))  # 被邀请人省份
    IRIcity = Column(String(64))  # 被邀请人城市
    IRIarea = Column(String(64))  # 被邀请人区县
    IRIaddress = Column(String(64))  # 被邀请人详细地址
    IRIpaytype = Column(String(64))  # 打款方式: {0: 微信, 1: 支付宝, 2:银行转账}
    IRIpayamount = Column(String(64))  # 付款金额
    IRIpaytime = Column(String(14))  # 打款时间
    IRIpic = Column(String(255))  # 被邀请人头像
    IRIproof = Column(String(255))  # 被邀请人凭证
    IRIstatus = Column(String(64))  # 邀请状态:{0:待审核, 1:审核通过, 2:审核不通过}
    IRIcreatetime = Column(String(14))  # 记录创建时间
    """
class InvitaOfAlipay(Base):
    """
    支付宝打款邀请详情
    """
    __tablename__ = 'invitaofalipay'
    IOAid = Column(String(64), primary_key=True)
    IRIod = Column(String(64))  # 对应邀请记录id
    IOAnum = Column(String(64))  # 支付宝账户

class InvitaOfBank(Base):
    """
    银行卡打款邀请详情
    """
    __tablename__ = 'invitaofbank'
    IOBid = Column(String(64), primary_key=True)
    IRIod = Column(String(64))  # 对应邀请记录id
    IOBbankname = Column(String(64))  # 开户银行
    IOBacconame = Column(String(64))  # 银行户名
    IOBcardnum = Column(String(64))  # 银行卡号


class InvitaRecordInfoo(Base):
    """
    邀请记录详情(线上审核，如果需要)
    """
    __tablename__ = 'invitarecordinfoo'
    IRIod = Column(String(64), primary_key=True)
    ILid = Column(String(64))  # 邀请链接id
    IRIname = Column(String(64))  # 被邀请人姓名
    IRIphonenum = Column(String(64))  # 被邀请人电话号码
    IRIpassword = Column(String(64))  # 被邀请人秘密
    IRIwechat = Column(String(64))   # 被邀请人微信号
    IRIcountry = Column(String(64))  # 被邀请人国家及地区
    IRIprovince = Column(String(64))  # 被邀请人省份
    IRIcity = Column(String(64))  # 被邀请人城市
    IRIarea = Column(String(64))  # 被邀请人区县
    IRIaddress = Column(String(64))  # 被邀请人详细地址
    IRIpaytype = Column(String(64))  # 打款方式: {0: 微信, 1: 支付宝, 2:银行转账}
    IRIpayamount = Column(String(64))  # 付款金额
    IRIpaytime = Column(String(14))  # 打款时间
    IRIpic = Column(String(255))  # 被邀请人头像
    IRIproof = Column(String(255))  # 被邀请人凭证
    IRIstatus = Column(String(64))  # 邀请状态:{0:待审核, 1:审核通过, 2:审核不通过}
    IRIcreatetime = Column(String(14))  # 记录创建时间


class OrderInfo(Base):
    """订单信息"""
    __tablename__ = 'orderinfo'
    OIid = Column(String(64), primary_key=True)
    OIsn = Column(String(64))  # 订单号
    USid = Column(String(64))  # 用户id
    """
    订单状态: {0:所有订单, 1:待发货, 2:已发货, 3:交易完成 } 根据需求无待支付状态
    """
    OIstatus = Column(Integer, default=1)
    OInote = Column(String(255))  # 订单留言
    OImount = Column(Float)  # 金额
    UAid = Column(String(255), nullable=False)  # 地址id
    OIcreatetime = Column(String(14))  # 订单创建时间
    OIlogisticsfee = Column(Float)  # 订单运费

class OrderProductInfo(Base):
    """订单商品详情, 多个订单商品详情对应一个订单"""
    __tablename__ = 'orderproductinfo'
    OPIid = Column(String(64), primary_key=True)
    OIid = Column(String(64), nullable=False)  # 订单
    PRid = Column(String(64), nullable=False)  # 商品id
    PRprice = Column(Float, nullable=False)   # 商品价格(购买时候的价格)
    PRname = Column(String(64))  # 商品的名字(购买之时的)
    PRimage = Column(String(255))  # 商品主图
    PRnum = Column(Integer)  # 购买数量

class LoanRecharge(Base):
    """
    贷款充值记录表(人工充值，与线上微信充值对立)
    """
    __tablename__ = 'loanrecharge'
    LRid = Column(String(64), primary_key=True)
    USid = Column(String(64))  # 用户
    LRpaytype = Column(Integer)  # 充值方式:{0:支付宝, 1:银行转账}
    LRpayamount = Column(Float)  # 充值金额
    LRpaydate = Column(String(14))  # 充值日期
    LRremark = Column(String(64))  # 充值备注
    LRcreatetime = Column(String(14))  # 记录创建时间

class AlipyRecharge(Base):
    """
    贷款充值记录表，通过支付宝打款的详情
    """
    __tablename__ = 'alipyrecharge'
    ARid = Column(String(64), primary_key=True)
    LRid = Column(String(64))  # 贷款充值记录id
    ARacount = Column(String(64))  # 支付宝账户

class BankRecharge(Base):
    """
    贷款充值记录表，通过银行卡转账的详情
    """
    __tablename__ = 'bankrecharge'
    BRid = Column(String(64), primary_key=True)
    LRid = Column(String(64))  # 贷款充值记录id
    BRbankname = Column(String(64))  # 银行名称
    BRaccountname = Column(String(64))  # 开户名称
    BRcardnum = Column(String(64))  # 银行卡账户

class Bail(Base):
    """
    保证金
    """
    __tablename__ = 'bail'
    BAid = Column(String(64), primary_key=True)
    USid = Column(String(64))  # 用户id
    BAamount = Column(String(64))  # 保证金金额



class OnlineRecharge(Base):
    """
    微信线上充值记录表(如果需要)
    """
    __tablename__ = 'onlinerecharge'
    ONRid = Column(String(64), primary_key=True)
    USid = Column(String(64))  # 用户
    ONRamount = Column(Float)  # 充值金额
    ONRwechatnum = Column(String(125))  # 充值微信账户
    ONRstatus = Column(Integer)  # 记录状态: {0: 全部, 1: 充值中, 2: 充值成功, 3: 充值失败}
    ONDcreatetime = Column(String(14))  # 创建时间
    ONDtradenum = Column(String(125))  # 交易号, (如果有)

"""
class OnlineDraw(Base):
    
    微信线上提现记录表（如果需要）
    
    __tablename__ = 'onlinedraw'
    ONDid = Column(String(64), primary_key=True)
    USid = Column(String(64))  # 用户
    ONDamount = Column(Float)  # 提现金额
    ONDwechatnum = Column(String(125))  # 提现微信账户
    ONDstatus = Column(Integer)  # 记录状态: {0: 全部, 1: 提现中, 2: 提现成功, 3: 提现失败}
    ONDcreatetime = Column(String(14))  # 创建时间
    ONDtradenum = Column(String(125))  # 交易号, (如果有)
"""

class OfflineDraw(Base):
    """
    银行卡线下提现记录表
    """
    __tablename__ = 'offlinedraw'
    OFDid = Column(String(64), primary_key=True)
    USid = Column(String(64))  # 用户
    OFDamount = Column(Float)  # 提现金额
    OFDbankname = Column(String(64), nullable=False)     # 银行名称
    OFDbranchname = Column(String(64), nullable=False)     # 支行名称
    OFDcardnum = Column(String(19), nullable=False)      # 银行卡号
    OFDaccountname = Column(String(64), nullable=False)     # 开户名称
    OFDstatus = Column(Integer)  # 提现状态: {0: 全部, 1: 待审核, 2: 待打款, 3: 已打款 4: 未通过}
    SUid = Column(String(64))  # 操作员
    OFDcreatetime = Column(String(14))  # 创建时间
    OFDtradenum = Column(String(125))  # 交易号, (如果有)

class Reward(Base):
    """
    奖金表
    """
    __tablename__ = 'reward'
    REid = Column(String(64), primary_key=True)
    IRIod = Column(String(64))   # 邀请记录id
    RErefid = Column(String(64))  # 推荐人id
    REberefid = Column(String(64))  # 被推荐人id
    REamount = Column(Float)  # 奖金金额

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
    QUtext = Column(String(128), nullable=False)  # 问题详情

class UserLoginTime(Base):
    """
    用来记录用户的登录时间
    """
    __tablename__ = 'userlogintime'
    ULTid = Column(String(64), primary_key=True)
    USid = Column(String(64), nullable=False)  # 用户id
    USTcreatetime = Column(String(14))  # 登录时间
    USTip = Column(String(64))  # 登录ip地址

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
    ARid = Column(String(64))  # 已读消息id
    USid = Column(String(64))  # 已读消息用户id


# Base.metadata.create_all(mysql_engine)