# *- coding:utf8 *-
from flask import Flask
import flask_restful
from apis.AGoods import AGoods
from apis.AUser import AUser
from apis.AMyCenter import AMyCenter
from apis.AMessage import AMessage
from apis.AOrder import AOrder
from apis.AAdmin import AAdmin
from apis.AAccount import AAccount
from flask_cors import CORS


sg = Flask(__name__)
sg.config.from_object('config.setting')
api = flask_restful.Api(sg)
@sg.route('/index')
def index():
    return "Hello,World!"
api.add_resource(AGoods, "/apis/product/<string:product>")
api.add_resource(AUser, "/apis/user/<string:user>")
api.add_resource(AMyCenter, "/apis/mycenter/<string:mycenter>")
api.add_resource(AMessage, "/apis/message/<string:message>")
api.add_resource(AOrder, "/apis/order/<string:order>")
api.add_resource(AAdmin, "/apis/admin/<string:admin>")
api.add_resource(AAccount, "/apis/account/<string:account>")

# '''
if __name__ == '__main__':
    CORS(sg, supports_credentials=True)
    sg.run('0.0.0.0', 443, debug=False, ssl_context=(
        "/usr/local/nginx/cert/1571716_www.beiliyuncang.com.pem"
    ))

'''
if __name__ == '__main__':
    CORS(sg, supports_credentials=True)
    sg.run('0.0.0.0', 7444, debug=False)
'''