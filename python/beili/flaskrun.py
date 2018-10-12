# *- coding:utf8 *-
from WeiDian import create_app
from WeiDian.common.base_error import BaseError
# from flask_socketio import SocketIO, emit


wd = create_app()

# socketio = SocketIO()
# socketio.init_app(wd)
# @socketio.on('request_for_response',namespace='/testnamespace')
# def give_response(data):
#     value = data.get('param')
#     import time
#     #进行一些对value的处理或者其他操作,在此期间可以随时会调用emit方法向前台发送消息
#     emit('response',{'code':'200','msg':'start to process...'})
#
#     time.sleep(5)
#     emit('response',{'code':'200','msg':'processed'})

# @wd.errorhandler(Exception)
# def framework_error(e):
#     if isinstance(e, BaseError):
#         return e
#     if not wd.config['DEBUG']:
#         raise BaseError()
#     raise e


if __name__ == '__main__':
    # socketio.run(wd, host='0.0.0.0', port=7443, debug=True)
    wd.run(host='0.0.0.0', port=7443, debug=True)
