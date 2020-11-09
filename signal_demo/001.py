"""
Author   : HarperHao
TIME    ： 2020/11/9
FUNCTION:  信号
"""

from blinker import Namespace
from datetime import datetime
from flask import request, g, Flask

app = Flask(__name__)
namespace = Namespace()
# 创建一个信号
login_signal = namespace.signal('login_signal')


def login_fun(sender):
    now = datetime.now()
    ip = request.remote_addr
    log_line = "{username}-------{now}--------{ip}".format(username=g.username, now=now, ip=ip)
    with open('login_log.txt', 'a') as f:
        f.write(log_line + '\n')


# 监听一个信号
login_signal.connect(login_fun)


@app.route('/')
def index():
    return 'Hello Signal1'


@app.route('/login/')
def login():
    # 得有查询字符串才可以
    username = request.args.get('username')
    if username:
        g.username = username
        login_signal.send()
        return 'Hello Signal2'
    else:
        return '请输入用户名'


if __name__ == '__main__':
    app.run()
