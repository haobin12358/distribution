# *- coding:utf8 *-

PARAMS_MISS = {
    "status": 405,
    "status_code": 405001,
    "message": "参数缺失"
}
PARAMS_ERROR = {
    "status": 405,
    "status_code": 405002,
    "message": "参数错误"
}
TOKEN_ERROR = {
    "status": 405,
    "status_code": 405003,
    "message": "token错误"
}
AUTHORITY_ERROR = {
    "status": 405,
    "status_code": 405004,
    "message": "没有权限"
}
NOT_FOUND_PHONENUM = {
    "status": 405,
    "status_code": 405005,
    "message": "没有找到该号码信息"
}
PHONE_OR_PASSWORD_WRONG = {
    "status": 405,
    "status_code": 405006,
    "message": "手机号或密码错误"
}
NOT_FOUND_IMAGE = {
    "status": 405,
    "status_code": 405007,
    "message": "图片未找到"
}
PASSWORD_WRONG = {
    "status": 405,
    "status_code": 405008,
    "message": "密码错误"
}
NOT_FOUND_USER = {
    "status": 405,
    "status_code": 405009,
    "message": "未找到该用户"
}
NO_ADDRESS = {
    "status": 405,
    "status_code": 405010,
    "message": "未找到地址"
}
INFORCODE_WRONG = {
    "status": 405,
    "status_code": 405011,
    "message": "验证码错误"
}
NOT_FOUND_ADDRESS = {
    "status": 405,
    "status_code": 405012,
    "message": "未找到收货地址"
}
BAD_ADDRESS = {
    "status": 405,
    "status_code": 405013,
    "message": "无效的地址代号"
}
NO_THIS_CATEGORY = {
    "status": 405,
    "status_code": 405014,
    "message": "没有此分类"
}
UPDATE_ADDRESS_FAIL = {
    "status": 405,
    "status_code": 405015,
    "message": "更新地址失败"
}
CHANGE_ADDRESS_FAIL = {
    "status": 405,
    "status_code": 405016,
    "message": "切换地址失败"
}
STOCK_NOT_ENOUGH = {
    "status": 405,
    "status_code": 405017,
    "message": "商品库存不足"
}
NO_ENOUGH_MOUNT = {
    "status": 405,
    "status_code": 405018,
    "message": "账户余额不足"
}
NO_BAIL = {
    "status": 405,
    "status_code": 405019,
    "message": "未缴纳保证金"
}
PRlogisticsfee_WRONG = {
    "status": 405,
    "status_code": 405020,
    "message": "运费金额核对出错"
}
TOTAL_PRICE_WRONG = {
    "status": 405,
    "status_code": 405021,
    "message": "商品总价核对出错"
}
NOT_FOUND_FILE = {
    "status": 405,
    "status_code": 405022,
    "message": "图片未找到"
}
DELETE_CODE_FAIL = {
    "status": 405,
    "status_code": 405023,
    "message": "删除二维码失败"
}
REMOVE_FILR_FAIL = {
    "status": 405,
    "status_code": 405024,
    "message": "删除文件失败"
}
NOT_FOUND_QRCODE = {
    "status": 405,
    "status_code": 405025,
    "message": "二维码不存在"
}
NO_PHONENUM_OR_PASSWORD = {
    "status": 405,
    "status_code": 405026,
    "message": "请输入账户名或密码"
}
SYSTEM_ERROR = {
    "status": 404,
    "status_code": 404027,
    "message": "系统错误"
}
HAS_REGISTER = {
    "status": 405,
    "status_code": 405028,
    "message": "手机号已注册"
}
NOT_FOUND_OPENID = {
    "status": 405,
    "status_code": 405029,
    "message": "该用户没有获取到openid"
}
NOT_FOUND_ORDER = {
    "status": 405,
    "status_code": 405030,
    "message": "未找到该订单"

}
NOT_FOUND_RECORD = {
    "status": 405,
    "status_code": 405031,
    "message": "未找到记录"
}
MONEY_ERROR = {
    "status": 405,
    "status_code": 405032,
    "message": "金额核对出错"
}
REPERT_NUMBER = {
    'status': 405,
    'status_code': 405033,
    'message': '达标件数重复，请检查数据！'
}
REPERT_COLOR = {
    'status': 405,
    'status_code': 405034,
    'message': '颜色已经存在!'
}
REPERT_SIZE = {
    'status': 405,
    'status_code': 405035,
    'message': '尺码已经存在!'
}
PRODUCT_STATUS_WRONG = {
    'status': 405,
    'status_code': 405036,
    'message': '商品状态异常!'
}
PRODUCT_OFFLINE = {
    'status': 405,
    'status_code': 405037,
    'message': '商品已下架!'
}
SKU_WRONG = {
    'status': 405,
    'status_code': 405038,
    'message': '商品规格发生变化!'
}
CANNOT_CANCEL = {
    'status': 405,
    'status_code': 405039,
    'message': '订单已分拣或已发货，不支持取消!'
}



ADMINNUM_ERROR = {
    "status": 405,
    "status_code": 405100,
    "message": "该用户号不存在"
}
ADMINNAME_ERROR = {
    "status": 405,
    "status_code": 405101,
    "message": "该用户名不存在"
}

PRODUCE_CATEGORY_EXIST = {
    "status": 405,
    "status_code": 405102,
    "message": "该商品分类已经存在"
}
PRODUCE_CATEGORY_NOT_EXIST = {
    "status": 405,
    "status_code": 405103,
    "message": "该商品分类不存在"   
}

PRODUCE_CATEGORY_HAS_PRODUCT = {
    'status': 405,
    'status_code': 405104,
    'message': '该商品分类下有商品，请先下架商品'
}
HAS_SECOND_CATEGORY = {
    'status': 405,
    'status_code': 405104,
    'message': '请先删除该分类下的二级分类'
}
CAN_NOT_CHANGE_LEVEL = {
    'status': 405,
    'status_code': 405104,
    'message': '编辑分类时不能修改商品级别'
}
