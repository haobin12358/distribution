# *- coding:utf8 *-
from common.base_error import BaseError


class dberror(BaseError):
    code = 404001
    message = '数据库连接异常'
    status = 404

class stockerror(Exception):
    def __init__(self, message):
        self.message = message