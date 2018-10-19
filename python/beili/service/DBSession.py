# *- coding:utf8 *-
import sys
import os
from sqlalchemy.orm import sessionmaker

from common.query_session import Session
from models import model
sys.path.append(os.path.dirname(os.getcwd()))


db_session = sessionmaker(bind=model.mysql_engine, class_=Session)


def get_session():
    try:
        session = db_session()
        status = True
    except Exception as e:
        print e.message
        session = None
        status = False
    finally:
        return session, status
