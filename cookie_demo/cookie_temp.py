"""
Author   : HarperHao
TIME    ： 2020/10/31
FUNCTION:  使用flask操作cookie
"""
from flask import request, Response, Flask
from datetime import datetime, timedelta

app = Flask(__name__)


@app.route('/')
def index():
    resp = Response('Cookie的使用')
    resp.set_cookie('name', 'HarperHao', max_age=60)
    return resp


@app.route('/del/')
def delete_cookie():
    resp = Response('删除Cookie')
    resp.delete_cookie('name')
    return resp


@app.route('/time/')
def cookie_expires():
    resp = Response('设置cookie的expires参数')
    expires = datetime(year=2020, month=12, day=31, hour=16, minute=0, second=0)
    resp.set_cookie('username', 'test', expires=expires)
    return resp


if __name__ == '__main__':
    app.run()
