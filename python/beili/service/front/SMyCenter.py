# *- coding:utf8 *-
import sys
import os
import uuid
from werkzeug.security import check_password_hash
from service.SBase import SBase, close_session
from models.model import User, IdentifyingCode
sys.path.append(os.path.dirname(os.getcwd()))


class SMyCenter(SBase):

    @close_session
    def get_uptime_by_usphonenum(self, usphonenum):
        return self.session.query(IdentifyingCode.ICtime).filter_by(ICphonenum=usphonenum) \
            .order_by(IdentifyingCode.ICtime.desc()).first()

    @close_session
    def update_user_by_uid(self, uid, users):
        self.session.query(User).filter_by(USid=uid).update(users)

    @close_session
    def get_inforcode_by_usphonenum(self, phonenum):
        return self.session.query(IdentifyingCode).filter_by(ICphonenum=phonenum).order_by( \
            IdentifyingCode.ICtime.desc()).first()

    @close_session
    def add_inforcode(self, usphonenum, code, time):
        new_infocode = IdentifyingCode()
        new_infocode.ICid = str(uuid.uuid1())
        new_infocode.ICphonenum = usphonenum
        new_infocode.ICcode = code
        new_infocode.ICtime = time
        self.session.add(new_infocode)
        self.session.commit()
        self.session.close()
        return True

