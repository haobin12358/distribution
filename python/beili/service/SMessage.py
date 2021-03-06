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
        list =  self.session.query(AgentMessage.USid, AgentMessage.AMdate, AgentMessage.AMid, \
                                  AgentMessage.AMcontent, AgentMessage.AMtype).filter_by(USid=usid) \
            .order_by(AgentMessage.AMdate.desc()).offset((page - 1) * count).limit(count)
        mount = self.session.query(func.count(AgentMessage.USid)).filter_by(USid=usid).scalar()
        return list, mount

    @close_session
    def create_agentmessage(self, session, usid, time, content, type):
        agent = AgentMessage()
        agent.AMid = str(uuid.uuid4())
        agent.USid = usid
        agent.AMdate = time
        agent.AMcontent = content
        agent.AMtype = type
        session.add(agent)
        return True


    @close_session
    def get_alreadyMessage_by_usid(self, usid):
        return self.session.query(AlreadyRead.ARid, AlreadyRead.ARmessageid).filter(AlreadyRead.USid == usid).all()

    @close_session
    def get_comMessage_list(self, page, count):
        return self.session.query(ComMessage.CMid, ComMessage.CMdate, ComMessage.CMtype, ComMessage.CMtitle, \
                                 ComMessage.CMfile).filter(ComMessage.CMstatus == 1).order_by(ComMessage.CMdate.desc()) \
            .offset((page - 1) * count).limit(count)

    @close_session
    def get_commessage_num(self):
        return self.session.query(func.count(ComMessage.CMid)).filter(ComMessage.CMstatus == 1).scalar()

    @close_session
    def get_commessage_details(self, cmid):
        return self.session.query(ComMessage.CMid, ComMessage.CMdate, ComMessage.CMtype, ComMessage.CMtitle, \
                                 ComMessage.CMfile).filter_by(CMid=cmid).first()

    @close_session
    def get_isread(self, messageid, usid):
        return self.session.query(AlreadyRead).filter(AlreadyRead.ARmessageid==messageid).filter(AlreadyRead.USid==usid).first()

    @close_session
    def insert_alreadyread(self, id, messageid, usid):
        record = AlreadyRead()
        record.ARid = id
        record.ARmessageid = messageid
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
        all = self.session.query(AlreadyRead).filter_by(ARmessageid=messageid)
        if all:
            all.delete()
        return True

    @close_session
    def update_status(self, id):
        from models.model import InvitaRecord
        update = {}
        update['IRIstatus'] = 2
        self.session.query(InvitaRecord).filter(InvitaRecord.IRIid == id).update(update)

