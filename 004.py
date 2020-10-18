"""
Author   : HarperHao
TIME    ： 2020/10/18
FUNCTION:  使用不同的HTTP方法处理URL
"""
from flask import request
from flask import Flask

app = Flask(__name__)


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        return do_the_login()
    else:
        return show_the_login_form()


def do_the_login():
    pass


def show_the_login_form():
    pass
