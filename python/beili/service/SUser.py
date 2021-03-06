# *- coding:utf8 *-
import sys
import os
import uuid
from werkzeug.security import check_password_hash
from service.SBase import SBase, close_session
from models.model import User
from models.model import Qrcode
from models.model import InvitaRecord
from datetime import datetime
from common.timeformat import format_for_db
from sqlalchemy import func
sys.path.append(os.path.dirname(os.getcwd()))


class SUser(SBase):

    @close_session
    def getuser_by_phonenum(self, usphonenum):
        return self.session.query(User.USid, User.USpassword).filter_by(USphonenum=usphonenum).first()

    @close_session
    def getuserinfo_by_uid(self, id):
        return self.session.query(User.USname, User.USphonenum).filter(User.USid == id).first()

    @close_session
    def getuser_by_uid(self, usid):
        return self.session.query(User.USid, User.USpassword).filter_by(USid=usid).all()

    @close_session
    def update_user_by_uid(self, uid, users):
        self.session.query(User).filter_by(USid=uid).update(users)
        return True

    @close_session
    def update_user_by_state(self, state2, update):
        self.session.query(User).filter_by(state=state2).update(update)
        return True

    @close_session
    def getuser_by_preid(self, preid):
        return self.session.query(User.USname, User.USid, User.USagentid, User.USheadimg).filter(User.USpre == preid).all()

    @close_session
    def get_register_record(self, status):
        list = self.session.query(InvitaRecord.IRIid, InvitaRecord.IRIproof, InvitaRecord.IRIstatus, InvitaRecord.IRIcreatetime
                                  , InvitaRecord.IRIcardnum, InvitaRecord.IRIaccountname, InvitaRecord.IRIbankname
                                  , InvitaRecord.IRIalipaynum, InvitaRecord.IRIpaytime, InvitaRecord.IRIpayamount
                                  , InvitaRecord.IRIpaytype, InvitaRecord.IRIaddress, InvitaRecord.IRIarea, InvitaRecord.IRIcity
                                  , InvitaRecord.IRIwechat, InvitaRecord.IRIidcardnum, InvitaRecord.IRIname
                                  , InvitaRecord.IRIphonenum, InvitaRecord.IRIprephonenum, InvitaRecord.IRIprename
                                  ).order_by(InvitaRecord.IRIcreatetime.desc())
        if status > 0:
            list = list.filter(InvitaRecord.IRIstatus == status)
        list = list.all()
        return list

    @close_session
    def get_registerrecord_by_IRIid(self, id):
        list = self.session.query(InvitaRecord.IRIid, InvitaRecord.IRIproof, InvitaRecord.IRIstatus, InvitaRecord.IRIcreatetime
                                  , InvitaRecord.IRIcardnum, InvitaRecord.IRIaccountname, InvitaRecord.IRIbankname
                                  , InvitaRecord.IRIalipaynum, InvitaRecord.IRIpaytime, InvitaRecord.IRIpayamount
                                  , InvitaRecord.IRIpaytype, InvitaRecord.IRIaddress, InvitaRecord.IRIarea, InvitaRecord.IRIcity
                                  , InvitaRecord.IRIwechat, InvitaRecord.IRIidcardnum, InvitaRecord.IRIname, InvitaRecord.IRIpic
                                  , InvitaRecord.IRIphonenum, InvitaRecord.IRIpassword, InvitaRecord.IRIprephonenum, InvitaRecord.IRIprename
                                  ).filter(InvitaRecord.IRIid == id).first()
        return list

    @close_session
    def get_registerrecord_by_phonenum(self, phonenum):
        list = self.session.query(InvitaRecord.IRIid, InvitaRecord.IRIproof, InvitaRecord.IRIstatus,
                                  InvitaRecord.IRIcreatetime
                                  , InvitaRecord.IRIcardnum, InvitaRecord.IRIaccountname, InvitaRecord.IRIbankname
                                  , InvitaRecord.IRIalipaynum, InvitaRecord.IRIpaytime, InvitaRecord.IRIpayamount
                                  , InvitaRecord.IRIpaytype, InvitaRecord.IRIaddress, InvitaRecord.IRIarea,
                                  InvitaRecord.IRIcity
                                  , InvitaRecord.IRIwechat, InvitaRecord.IRIidcardnum, InvitaRecord.IRIname,
                                  InvitaRecord.IRIpic
                                  , InvitaRecord.IRIphonenum, InvitaRecord.IRIpassword, InvitaRecord.IRIprephonenum,
                                  InvitaRecord.IRIprename
                                  ).filter(InvitaRecord.IRIphonenum == phonenum).first()
        return list

    @close_session
    def update_register_record(self, id, update):
        self.session.query(InvitaRecord).filter(InvitaRecord.IRIid == id).update(update)
        return True

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

    def insertInvitate(self, session, data):
        record = InvitaRecord()
        record.IRIid = str(uuid.uuid4())
        record.IRIprename = data['preusername']
        record.IRIprephonenum = data['prephonenum']
        record.IRIname = data['username']
        record.IRIphonenum = data['phonenum']
        record.IRIpassword = data['password']
        record.IRIidcardnum = data['idcardnum']
        record.IRIwechat = data['wechat']
        record.IRIcity = data['cityid']
        record.IRIarea = data['areaid']
        record.IRIaddress = data['details']
        record.IRIpaytype = data['paytype']
        record.IRIpayamount = data['payamount']
        record.IRIpaytime = data['paytime']
        record.IRIpic = data['headimg']
        record.IRIalipaynum = data['alipaynum']
        record.IRIbankname = data['bankname']
        record.IRIproof = data['proof']
        record.IRIaccountname = data['accountname']
        record.IRIcardnum = data['cardnum']
        record.IRIstatus = 1
        record.IRIcreatetime = datetime.strftime(datetime.now(), format_for_db)
        session.add(record)
        return True

    @close_session
    def add_qrcode(self, id, usid, date, number):
        from models.model import Qrcode
        code = Qrcode()
        code.QRid = id
        code.USid = usid
        code.QRovertime = date
        code.QRnumber = number
        self.session.add(code)
        return True

    @close_session
    def get_qrcode_list(self, id):
        return self.session.query(Qrcode.QRovertime, Qrcode.QRnumber, Qrcode.QRid).filter(Qrcode.USid == id).\
            filter(Qrcode.QRstatus == 1).all()

    @close_session
    def delete_qrcode(self, id, codeid):
        update = {}
        update['QRstatus'] = 0
        self.session.query(Qrcode).filter(Qrcode.USid == id).filter(Qrcode.QRid == codeid).update(update)
        return True

    @close_session
    def get_arcode_details(self, id):
        return self.session.query(Qrcode.QRovertime, Qrcode.QRnumber, Qrcode.USid).filter(Qrcode.QRid == id).\
                filter(Qrcode.QRstatus == 1).first()

    @close_session
    def get_user_by_qrid(self, qrid):
        return self.session.query(Qrcode.USid).filter(Qrcode.QRid == qrid).first()

    @close_session
    def update_qrcode(self, qrid, update):
        self.session.query(Qrcode).filter(Qrcode.QRid == qrid).update(update)
        return True

    @close_session
    def get_qrcode_by_qrid(self, id):
        return self.session.query(Qrcode.QRovertime, Qrcode.QRnumber).filter(Qrcode.QRid == id).first()

    @close_session
    def get_qrcode_by_openid(self, id):
        return self.session.query(User.USmount, User.USid).filter(User.openid == id).first()

    @close_session
    def get_user_num(self):
        return self.session.query(func.count(User.USid)).scalar()

    @close_session
    def get_thismonth_agentnum(self, starttime, endtime):
        return self.session.query(func.count(User.USid)).filter(User.UScreatetime >= starttime).filter(User
                                                        .UScreatetime < endtime).scalar()

    @close_session
    def get_authorization(self, id):
        return self.session.query(User.authorization).filter(User.USid == id).first()

    @close_session
    def get_all_user_info(self):
        return self.session.query(User.USid, User.USagentid, User.USname, User.USheadimg).all()