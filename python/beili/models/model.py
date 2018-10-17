# -*- coding:utf8 -*-
from sqlalchemy import Column, create_engine, Integer, String, Text, Float, Boolean, orm
from config import dbconfig as cfg
# from models.base_model import Base, auto_createtime
from base_model import Base

DB_PARAMS = "{0}://{1}:{2}@{3}/{4}?charset={5}".format(
    cfg.sqlenginename,
    cfg.username,
    cfg.password,
    cfg.host,
    cfg.database,
    cfg.charset)
print(DB_PARAMS)
mysql_engine = create_engine(DB_PARAMS, echo=True)

class User(Base):
    """
    普通用户
    """
    __tablename__ = 'user'
    USid = Column(String(64), primary_key=True)
    USname = Column(String(64), nullable=False)  # 用户名
    USpassword = Column(String(255))             # 密码
    USphonenum = Column(String(16), nullable=False)  # 手机号
    USheader = Column(String(255))               # 头像
    USage = Column(Integer)                      # 年龄
    USbail = Column(Boolean)                     # 是否缴纳保证金
    USmount = Column(Float)                      # 账户余额
    USqrcode = Column(String(255))               # 邀请二维码
    USlastlogin = Column(String(64))             # 用户上次登录时间
    UPPerd = Column(String(64), default=0)       # 上级
    openid = Column(String(64))                  # 微信唯一值
    unionid = Column(String(255))                # 绑定公众号会出现
    accesstoken = Column(String(255))            # 微信token
    subscribe = Column(Integer)                  # 是否关注公众号


class SuperUser(Base):
    """
    超级用户
    """
    __tablename__ = 'superuser'
    SUid = Column(String(64), primary_key=True)
    SUname = Column(String(64), nullable=False)  # 超级用户名
    SUpassword = Column(String(255), nullable=False)  # 密码
    SUheader = Column(String(255))  # 用户头像, 可以设置一个默认值
    SUlevel = Column(Integer, default=0)  # 用户类型{0: 客服, 1: 管理员, 2:超管}　
    SUcreatetime = Column(String(14))  # 创建时间
    SUidfreeze = Column(Boolean, default=False)  # 是否被冻结
    SUisdelete = Column(Boolean, default=False)  # 是否被删除

class ProductCategory(Base):
    """
    商品分类
    """
    __tablename__ = 'productcategory'
    PAid = Column(String(64), primary_key=True)
    PAname = Column(String(16))  # 类别名
    PAtype = Column(Integer)  # 类目级别{1 一级分类, 2 二级分类, 3 三级分类}
    Parentid = Column(String(64), default=0)  # 父类别id, 默认0

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
    USid = Column(String(64))  # 用户
    OItradenum = Column(String(125))  # 交易号, (如果有)
    """
    订单状态: {0:所有订单, 1: 支付成功, 2: 支付超时关闭（交易关闭）, 3:待发货, 4:已发货, 
    5:已取消, 6:已签收, 7:交易失败（退货）, 8:交易完成, 9:待评价, 10:退换货 } 根据需求无待支付状态
    """
    OIpaystatus = Column(Integer, default=0)
    OIleavetext = Column(String(255))  # 订单留言
    OImount = Column(Float)  # 金额
    OIpaytime = Column(String(14))  # 支付时间
    OIaddress = Column(String(255), nullable=False)  # 地址
    OIrecvname = Column(String(64), nullable=False)  # 收货人
    OIrecvphone = Column(String(16), nullable=False)  # 收货人电话
    OIcreatetime = Column(String(14))  # 订单创建时间
    OIisdelete = Column(Boolean, default=False)  # 是否删除

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


class OnlineDraw(Base):
    """
    微信线上提现记录表（如果需要）
    """
    __tablename__ = 'onlinedraw'
    ONDid = Column(String(64), primary_key=True)
    USid = Column(String(64))  # 用户
    ONDamount = Column(Float)  # 提现金额
    ONDwechatnum = Column(String(125))  # 提现微信账户
    ONDstatus = Column(Integer)  # 记录状态: {0: 全部, 1: 提现中, 2: 提现成功, 3: 提现失败}
    ONDcreatetime = Column(String(14))  # 创建时间
    ONDtradenum = Column(String(125))  # 交易号, (如果有)


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


class Product(Base):
    """
    商品表
    """
    __tablename__ = 'product'
    PRid = Column(String(64), primary_key=True)
    PRname = Column(String(64), nullable=False)  # 名称
    PRpic = Column(String(255), nullable=False)  # 商品图片
    PRoldprice = Column(Float)  # 原价
    PRprice = Column(Float, nullable=False)  # 显示价格
    PRstock = Column(Integer)  # 库存
    SUid = Column(String(64))  # 发布者, 创建人
    PRcreatetime = Column(String(14))  # 创建时间
    SUmodifyid = Column(String(64))  # 修改人id
    PRmodifytime = Column(String(14))  # 修改时间
    PRlogisticsfee = Column(Float)  # 物流费

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
    AMtype = Column(Boolean)  # 种类: {0: 订单信息, 1: 款项消息, 2: 代理信息}
    AMtext = Column(String(128), nullable=False)  # 消息详情

class ComMessage(Base):
    """
    公司消息表
    """
    __tablename__ = 'commessage'
    CMid = Column(String(64), primary_key=True)
    CMdate = Column(String(64))  # 消息发布时间
    CMtype = Column(Boolean)  # 种类: {0: 公告}
    CMtext = Column(String(128), nullable=False)  # 消息详情
    CMpic = Column(String(255), nullable=False)  # 附加图片

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
    id = Column(Integer, primary_key=True)
    name = Column(String(20), nullable=False)
    provinceid = Column(String(8), nullable=False)


class City(Base):
    """市"""
    __tablename__ = 'city'
    id = Column(Integer, primary_key=True)
    cityid = Column(String(8), nullable=False)
    name = Column(String(20), nullable=False)
    provinceid = Column(String(8), nullable=False)


class Area(Base):
    """区县"""
    __tablename__ = 'area'
    id = Column(Integer, primary_key=True)
    name = Column(String(20), nullable=False)
    areaid = Column(String(8), nullable=False)
    cityid = Column(String(8), nullable=False)


class UserAddress(Base):
    """用户收货地址"""
    __tablename__ = 'useraddress'
    UAid = Column(String(64), primary_key=True)
    USid = Column(String(64), nullable=False)           # 用户
    UAname = Column(String(16), nullable=False)         # 收货人姓名
    UAphone = Column(String(16), nullable=False)        # 收货人电话
    UAtext = Column(String(255), nullable=False)        # 具体地址
    UAdefault = Column(Boolean, default=False)          # 默认收获地址
    UAstatus = Column(Boolean, default=False)           # 状态
    UAcreatetime = Column(String(14))                   # 创建时间
    areaid = Column(String(8), nullable=False)          # 关联的区域id

class IdentifyingCode(Base):
    """验证码"""
    __tablename__ = "identifyingcode"
    ICid = Column(String(64), primary_key=True)
    ICphonenum = Column(String(14), nullable=False)  # 获取验证码的手机号
    ICcode = Column(String(8), nullable=False)    # 获取到的验证码
    ICtime = Column(String(14), nullable=False)    # 获取的时间，格式为20180503100322


Base.metadata.create_all(mysql_engine)