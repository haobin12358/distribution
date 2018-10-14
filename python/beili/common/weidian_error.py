# *- coding:utf8 *-
from common.base_error import BaseError


class dberror(BaseError):
    code = 200
    message = '数据库连接异常'
    status = 404
