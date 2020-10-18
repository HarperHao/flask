"""
Author   : HarperHao
TIME    ： 2020/10/18
FUNCTION:  Cookies
"""
from flask import request, Flask, make_response

app = Flask(__name__)


# 读取cookies
@app.route('/')
def index():
    username = request.cookies.get('username')


# 存储cookies
@app.route('/')
def index1():
    resp = make_response(render_template('hello.html'))
    resp.set_cookie('username', 'the username')
    return resp
