# *- coding:utf8 *-
activity_type = {
    '0': '普通动态',
    '1': '满减',
    '2': '满赠',
    '3': '优惠券',
    '4': '砍价',
    '5': '拼团',
    '6': '单品优惠券',
    '7': '一元秒杀',
    '8': '前{0}分钟半价',
    '9': '限时抢',
    '10': 'x元x件',
}


complain_type = {
    '201': "客服态度差",
    '202': "商品质量问题",
    '203': "售后方案不合理",
    '204': "商品包装问题"
}

ORDER_STATUS = {

    '0': '全部',
    '1': '待支付',
    '2': '支付成功',
    '3': '支付超时关闭（交易关闭）',
    '4': '待发货',
    '5': '待收货',
    '6': '已取消',
    '7': '已完成',
    '8': '交易失败（退货）',
    '9': '交易完成',
    '10': '待评价',
    '11': '退换货',
}

BANK_MAP = {
    "ICBC": "工商银行",
    "ABC": "农业银行",
    "BOC": "中国银行",
    "PSBC": "邮政储蓄",
    "CCB":"中国建设银行",
    "NXS": "农村信用社",
}

TASK_TYPE = {
    '0': "观看视频",
    '1': "转发商品",
    '2': "售出商品",
    '3': "售出大礼包"
}

TASK_STATUS = {
    '0': "进行中",
    '1': "已完成",
    '2': "已暂停",
    '3': "已过期",
    '4': "已失效",
}

REWARD_TYPE = {
    '0': "满减",
    '1': "佣金加成",
    '2': "无门槛"
}

icon = {
           "name": '首页',
           "icon": 'https://daaiti.cn/imgs/WeiDian/icon/home.png',
           "active_icon": 'https://daaiti.cn/imgs/WeiDian/icon/home2.png',
           "url": 'index'
       }, {
           "name": '客服',
           "icon": 'https://daaiti.cn/imgs/WeiDian/icon/info.png',
           "active_icon": 'https://daaiti.cn/imgs/WeiDian/icon/info2.png',
           "url": 'service'
       }, {
           "name": '发现',
           "icon": 'https://daaiti.cn/imgs/WeiDian/icon/search2.png',
           "active_icon": 'https://daaiti.cn/imgs/WeiDian/icon/search.png',
           "url": 'discover'
       }, {
           "name": '购物车',
           "icon": 'https://daaiti.cn/imgs/WeiDian/icon/cart2.png',
           "active_icon": 'https://daaiti.cn/imgs/WeiDian/icon/cart.png',
           "url": 'shopping'
       }, {
           "name": '我的',
           "icon": 'https://daaiti.cn/imgs/WeiDian/icon/me.png',
           "active_icon": 'https://daaiti.cn/imgs/WeiDian/icon/me2.png',
           "url": 'personal'
       }

finished_pay_status = ['2', '4', '5', '7', '9', '10', '11']

HMSkipType = {'0': '无跳转类型', '1': '专题', '2': '商品', '3': '教程', '4': '公告'}
