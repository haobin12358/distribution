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

    @close_session
    def get_all_adnum(self):
        return self.session.query(Admin.ADnum).all()

    @close_session
    def get_all_adname(self):
        return self.session.query(Admin.ADname).all()

    @close_session
    def add_admin(self, uaid, ADnum, ADname, ADpassword, ADlevel, time_str, Adheadering='www.baidu.com'):
        admin = Admin()

        admin.ADid = uaid
        admin.ADnum = ADnum
        admin.ADname = ADname
        admin.ADpassword = ADpassword
        admin.ADheaderimg = Adheadering
        admin.ADlevel = ADlevel
        admin.ADcreatetime = time_str

        self.session.add(admin)
        return True

