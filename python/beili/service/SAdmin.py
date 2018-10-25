# *- coding:utf8 *-
import sys
import os
from werkzeug.security import check_password_hash
from service.SBase import SBase, close_session
from models.model import User, Admin
sys.path.append(os.path.dirname(os.getcwd()))


class SAdmin(SBase):

    @close_session
    def getadmin_by_adnum(self, num):
        return self.session.query(Admin.ADid, Admin.ADlevel, Admin.ADpassword).filter_by(ADnum=num).first()

    @close_session
    def getadmin_by_adminid(self, adminid):
        return self.session.query(Admin).filter_by(ADid=adminid).first()

    @close_session
    def update_amdin_by_adminid(self, adminid, users):
        self.session.query(Admin).filter_by(ADid=adminid).update(users)

