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

sg = Flask(__name__)
sg.config.from_object('config.setting')
api = flask_restful.Api(sg)

api.add_resource(AGoods, "/product/<string:product>")
api.add_resource(AUser, "/user/<string:user>")
api.add_resource(AMyCenter, "/mycenter/<string:mycenter>")
api.add_resource(AMessage, "/message/<string:message>")
api.add_resource(AOrder, "/order/<string:order>")
api.add_resource(AAdmin, "/admin/<string:admin>")
api.add_resource(AAccount, "/account/<string:account>")

'''
if __name__ == '__main__':
    sg.run('0.0.0.0', 443, debug=False, ssl_context=(
        "/etc/nginx/cert/1525609592348.pem"
    ))
    
'''
if __name__ == '__main__':
    sg.run('0.0.0.0', 7444, debug=False)

