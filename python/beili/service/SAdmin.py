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
    def get_same_adnum(self,ADnum):
        return self.session.query(Admin.ADnum).filter_by(ADnum=ADnum).all()

    @close_session
    def get_same_adname(self,ADname):
        return self.session.query(Admin.ADname).filter_by(ADname=ADname).all()

    @close_session
    def add_admin(self, uaid, ADnum, ADname, ADpassword,Adheadering,ADlevel,time_str,ADisfreeze=False):
        admin = Admin()
        admin.ADid = uaid
        admin.ADnum = ADnum  # 管理员账号
        admin.ADname = ADname  # 管理员用户名
        admin.ADpassword = ADpassword  # 密码
        admin.ADheaderimg = Adheadering  # 用户头像, 可以设置一个默认值
        admin.ADlevel = ADlevel  # 用户级别{0: 一般管理员, 1: 超级管理员}　
        admin.ADcreatetime = time_str  # 创建时间
        admin.ADisfreeze = ADisfreeze
        self.session.add(admin)


