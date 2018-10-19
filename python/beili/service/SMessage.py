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
        return self.session.query(AgentMessage).filter_by(USid=usid) \
            .order_by(AgentMessage.AMdate.desc()).offset((page - 1) * count).limit(count)

    @close_session
    def get_alreadyMessage_by_usid(self, usid):
        return self.session.query(AlreadyRead.ARid).filter_by(USid=usid).all()

    @close_session
    def get_comMessage_list(self, page, count):
        return self.session.query(ComMessage).order_by(ComMessage.CMdate.desc()).offset((page - 1) * count).limit(count)

    @close_session
    def get_commessage_num(self):
        return self.session.query(func.count(ComMessage.CMid))

    @close_session
    def get_commessage_details(self, cmid):
        return self.session.query(ComMessage).filter_by(CMid=cmid)

    @close_session
    def update_commessage_status(self, messageid, usid):
        record = AlreadyRead()
        record.ARid = messageid
        record.USid = usid
        self.session.add(record)

