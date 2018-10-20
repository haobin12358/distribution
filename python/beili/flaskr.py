# *- coding:utf8 *-
from flask import Flask
import flask_restful
from apis.front.AGoods import AGoods

sg = Flask(__name__)
api = flask_restful.Api(sg)

api.add_resource(AGoods, "/product/<string:product>")

'''
if __name__ == '__main__':
    sg.run('0.0.0.0', 443, debug=False, ssl_context=(
        "/etc/nginx/cert/1525609592348.pem"
    ))
    
'''
if __name__ == '__main__':
    sg.run('0.0.0.0', 7444, debug=False)

