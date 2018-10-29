# *- coding:utf8 *-
import sys
import os
from werkzeug.security import check_password_hash
from service.SBase import SBase, close_session
from models.model import User
sys.path.append(os.path.dirname(os.getcwd()))


class SUser(SBase):

    @close_session
    def getuser_by_phonenum(self, usphonenum):
        return self.session.query(User.USid, User.USpassword).filter_by(USphonenum=usphonenum).first()

    @close_session
    def getuser_by_uid(self, usid):
        return self.session.query(User.USid, User.USpassword).filter_by(USid=usid).all()

    @close_session
    def update_user_by_uid(self, uid, users):
        self.session.query(User).filter_by(USid=uid).update(users)

    @close_session
    def getuser_by_preid(self, preid):
        return self.session.query(User.USid).filter(User.USpre == preid).all()

