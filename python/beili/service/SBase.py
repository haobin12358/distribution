# *- coding:utf8 *-
import sys
import os
import DBSession
from common.beili_error import dberror, stockerror
import models.model as models
# from models.base_model import BaseModel
sys.path.append(os.path.dirname(os.getcwd()))

def close_session(fn):
    def inner(self, *args, **kwargs):
        try:
            result = fn(self, *args, **kwargs)
            # self.session.expunge_all()
            self.session.commit()
            print type(result)
            return result
        except stockerror as e:
            print("stockerror" + e.message)
            self.session.rollback()
            raise stockerror('库存不足')
        except Exception as e2:
            print("dberror" + e2.message)
            self.session.rollback()
            raise dberror
        finally:
            self.session.close()
    return inner

# service 基础类
class SBase(object):
    def __init__(self):
        try:
            self.session = DBSession.db_session()
        except Exception as e:
            # raise e
            print(e.message)

    @close_session
    def add_model(self, model_name, **kwargs):
        print(model_name)
        if not getattr(models, model_name):
            print("model name = {0} error ".format(model_name))
            return
        model_bean = eval(" models.{0}()".format(model_name))
        for key in model_bean.__table__.columns.keys():
            if key in kwargs:
                setattr(model_bean, key, kwargs.get(key))
        self.session.add(model_bean)
