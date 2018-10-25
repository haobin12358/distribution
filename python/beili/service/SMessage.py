# *- coding:utf8 *-
import sys
import os
import uuid
from werkzeug.security import check_password_hash
from service.SBase import SBase, close_session
from models.model import User, IdentifyingCode, AgentMessage, AlreadyRead, ComMessage
from sqlalchemy import func
sys.path.append(os.path.dirname(os.getcwd()))


class SMessage(SBase):

    @close_session
    def get_agentMessage_by_usid(self, usid, page, count):
        return self.session.query(AgentMessage.USid, AgentMessage.AMdate, AgentMessage.AMid, \
                                  AgentMessage.AMcontent, AgentMessage.AMtype).filter_by(USid=usid) \
            .order_by(AgentMessage.AMdate.desc()).offset((page - 1) * count).limit(count)

    @close_session
    def get_alreadyMessage_by_usid(self, usid):
        return self.session.query(AlreadyRead.ARid).filter(AlreadyRead.USid == usid).all()

    @close_session
    def get_comMessage_list(self, page, count):
        return self.session.query(ComMessage.CMid, ComMessage.CMdate, ComMessage.CMtype, ComMessage.CMtitle, \
                                 ComMessage.CMfile).filter(ComMessage.CMstatus == 0).order_by(ComMessage.CMdate.desc()) \
            .offset((page - 1) * count).limit(count)

    @close_session
    def get_commessage_num(self):
        return self.session.query(func.count(ComMessage.CMid)).filter(ComMessage.CMstatus == 0).scalar()

    @close_session
    def get_commessage_details(self, cmid):
        return self.session.query(ComMessage.CMid, ComMessage.CMdate, ComMessage.CMtype, ComMessage.CMtitle, \
                                 ComMessage.CMfile).filter_by(CMid=cmid)

    @close_session
    def insert_alreadyread(self, messageid, usid):
        record = AlreadyRead()
        record.ARid = messageid
        record.USid = usid
        self.session.add(record)

    @close_session
    def publish_commessage(self, id, date, type, title, url):
        commessage = ComMessage()
        commessage.CMid = id
        commessage.CMdate = date
        commessage.CMtype = type
        commessage.CMtitle = title
        commessage.CMfile = url
        self.session.add(commessage)

    @close_session
    def delete_commessage(self, messageid, upate_message):
        self.session.query(ComMessage).filter_by(CMid=messageid).update(upate_message)

    @close_session
    def delete_alreadyread(self, messageid):
        all = self.session.query(AlreadyRead).filter_by(ARid=messageid).all()
        self.session.delete(all)




