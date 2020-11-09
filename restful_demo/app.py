"""
Author   : HarperHao
TIME    ： 2020/11/2
FUNCTION:  flask_restful的学习
"""
from flask import Flask
from flask_restful import Api, Resource, reqparse, inputs

app = Flask(__name__)
api = Api(app)


class LoginView(Resource):
    def post(self):
        return {'username': 'HarperHao'}


api.add_resource(LoginView, '/login/')


# reqparse模块的学习
class IndexView(Resource):
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('name', type=str, help='用户名出错')
        parser.add_argument('age', type=inputs.int_range(12, 60), help='用户年龄出错')
        parser.add_argument('sex', type=str, choices=['male', 'female', 'secret'], help='性别输入错误')
        args = parser.parse_args()
        print(args)
        return {'code': '200'}


api.add_resource(IndexView, '/index/')


@app.route('/')
def hello_world():
    return 'Hello World!'


if __name__ == '__main__':
    app.run()
