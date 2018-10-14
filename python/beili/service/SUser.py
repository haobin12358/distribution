# *- coding:utf8 *-
import sys
import os
from werkzeug.security import check_password_hash
from SBase import SBase, close_session
from models.model import User
sys.path.append(os.path.dirname(os.getcwd()))


class SUser(SBase):

    @close_session
    def getpasswd_by_phonenum(self, usphone):
        return self.session.query(User).filter_by(USphone=usphone).first()

