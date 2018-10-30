# *- coding:utf8 *-
import sys
import os
from werkzeug.security import check_password_hash
from service.SBase import SBase, close_session
from models.model import User
from sqlalchemy import func
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
        return self.session.query(User.USname, User.USid, User.USagentid, User.USheadimg).filter(User.USpre == preid).all()

    @close_session
    def getusername_and_id_by_preid(self, preid):
        return self.session.query(User.USname, User.USid).filter(User.USpre == preid).all()

    @close_session
    def get_myself_name(self, id):
        return self.session.query(User.USname, User.USheadimg, User.USagentid).filter(User.USid == id).all()

    @close_session
    def getusername_by_preid(self, preid, page, count):
        return self.session.query(User.USname).filter(User.USpre == preid).offset((page - 1) * count).limit(count).all()

    @close_session
    def get_totaldirect(self, id):
        return self.session.query(func.count(User.USid)).filter_by(USpre=id).scalar()
