# *- coding:utf8 *-
import datetime


from itsdangerous import TimedJSONWebSignatureSerializer as Serializer, BadSignature, SignatureExpired
from flask import current_app, request

from service.DBSession import db_session


def usid_to_token(id, type='User', expiration=''):
    """生成令牌
    id: 用户id
    model: 用户类型(User 或者 SuperUser)
    expiration: 过期时间, 默认20个小时, 在common/setting中修改
    """
    if not expiration:
        expiration = current_app.config['TOKEN_EXPIRATION']
    s = Serializer(current_app.config['SECRET_KEY'], expires_in=expiration)
    time_now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    return s.dumps({
        'id': id,
        'type':type,
        'time': time_now,
    })


def token_to_usid(token):
    s = Serializer(current_app.config['SECRET_KEY'])
    try:
        data = s.loads(token)
    except BadSignature as e:
        print '不合法的token'
        return
    except SignatureExpired as e:
        print 'token is expired'
        return
    except Exception as e:
        raise e
    id = data['id']
    return id


def verify_token_decorator(func):
    """
    验证token装饰器, 并将用户对象放入request.user中
    """

    def inner(self, *args, **kwargs):
        parameter = request.args.to_dict()
        token = parameter.get('token')
        s = Serializer(current_app.config['SECRET_KEY'])
        try:
            data = s.loads(token)
        except BadSignature as e:
            # 签名出错的token
            return func(self, *args, **kwargs)
        except SignatureExpired as e:
            # 过期的token
            return func(self, *args, **kwargs)
        except Exception as e:
            # 无法解析的token
            return func(self, *args, **kwargs)
        id = data['id']
        time = data['time']
        type = data['type']
        if type != 'User' and type != 'SuperUser':
            return func(self, *args, **kwargs)
        sessions = db_session()
        try:
            if type == 'User':
                from models.model import User
                user = sessions.query(User).filter_by(USid=id).first()
                if not user:
                    # 不存在的用户
                    return func(self, *args, **kwargs)
                user.id = user.USid
                user.type = 'User'
            if type == 'SuperUser':
                from models.model import SuperUser
                user = sessions.query(SuperUser).filter_by(SUid=id).first()
                if not user:
                    # 不存在的管理
                    return func(self, *args, **kwargs)
                user.id = user.SUid
                user.type = 'SuperUser'
                user.level = user.SUlevel
            sessions.expunge_all()
            sessions.commit()
            if user:
                request.user = user
            return func(self, *args, **kwargs)
        finally:
            sessions.close()
    return inner


def is_ordirnaryuser():
    """普通用户"""
    return (hasattr(request, 'user') and request.user.scope == 'User')

def is_admin():
    """是否是管理员"""
    return (hasattr(request, 'user') and request.user.scope == 'SuperUser' and request.user.SUlevel == 0)

def is_superadmin():
    """是否是超级管理员"""
    return (hasattr(request, 'user') and request.user.scope == 'SuperUser' and request.user.SUlevel == 1)

def is_tourist():
    """游客，未登录"""
    return (not hasattr(request, 'user'))
# if __name__ == '__main__':
#     from WeiDian import create_app
#     app = create_app()
#     res = usid_to_token('6882ad09-bf5f-4607-8ad1-1cd46b6158e0', current_app=app)
#     print(res)
