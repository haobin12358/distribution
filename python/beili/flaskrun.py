# *- coding:utf8 *-
# 引用python类
from flask import Flask as _Flask
from flask.wrappers import Request as _Request
from flask.json import JSONEncoder as _JSONEncoder
from common.base_error import BaseError


class JSONEncoder(_JSONEncoder):
    """重写对象序列化, 当默认jsonify无法序列化对象的时候将调用这里的default"""
    def default(self, o):
        if hasattr(o, 'keys') and hasattr(o, '__getitem__'):
            res = dict(o)
            for k in res.keys():
                if k[0].isupper():
                    # 字段转小写
                    res[k.lower()] = res[k]
                    res.pop(k)
            return res
        if isinstance(o, date):
            # 也可以序列化时间类型的对象
            return o.strftime('%Y-%m-%d')
        if isinstance(o, type):
            raise o()
        if isinstance(o, HTTPException):
            raise o
        raise Exception(o + 'is not jsonserializer')

class Request(_Request):
    @property
    def detail(self):
        return str({
            'url': self.url,
            'method': self.method,
            'args': self.args.to_dict(),
            'data': self.data,
        })

from werkzeug.exceptions import HTTPException

#class Flask(_Flask):
#    json_encoder = JSONEncoder
#    request_class = Request

# 引用项目类
from apis.front.AUser import AUser
from apis.back.AAdmin import AAdmin
from apis.front.AMyCenter import AMyCenter
from apis.front.AGoods import AGoods


# 定义实际接口
def register_route(app):
    """添加路由"""
    app.add_url_rule('/user/<string:user>', view_func=AUser.as_view('user'))
    app.add_url_rule('/admin/<string:user>', view_func=AAdmin.as_view('admin'))
    #app.add_url_rule('/mycenter/<string:mycenter>', view_func=AMyCenter.as_view('mycenter'))
    app.add_url_rule('/mycenter/<string:mycenter>', view_func=AMyCenter.as_view('mycenter'))
    app.add_url_rule('/product/<string:product>', view_func=AGoods.as_view('product'))

def create_app():
    app = _Flask(__name__)
    app.config.from_object('config.setting')
    # from raven.contrib.flask import Sentry
    #sentry = Sentry(app, dsn='http://5ffc9de0629a4a58a7e76958dd4c6a2a:edc93accdb934ad1b7e16cf7fbb407e2@s.wkt.ooo:7443/3')
    # ws = GeventWebSocket(app)
    register_route(app)   # 对app进行路由设置
    # create_test_url(app)  # 测试用
    # CORS(app, supports_credentials=True)
    return app

# 实例化flask启动器
app = create_app()

# socketio = SocketIO()
# socketio.init_app(app)
# @socketio.on('request_for_response',namespace='/testnamespace')
# def give_response(data):
#     value = data.get('param')
#     import time
#     #进行一些对value的处理或者其他操作,在此期间可以随时会调用emit方法向前台发送消息
#     emit('response',{'code':'200','msg':'start to process...'})
#
#     time.sleep(5)
#     emit('response',{'code':'200','msg':'processed'})

#@app.errorhandler(Exception)
#def framework_error(e):
#    if isinstance(e, BaseError):
#         return e
#    if not app.config['DEBUG']:
#         raise BaseError()
#    return e

# 启动方法
if __name__ == '__main__':
    app.run('0.0.0.0', 7443, debug=True)

