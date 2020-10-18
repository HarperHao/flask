"""
Author   : HarperHao
TIME    ： 2020/10/18
FUNCTION:  重定向和错误
"""
from flask import abort, redirect, url_for, Flask

app = Flask(__name__)


@app.route('/')
def index():
    return redirect(url_for('login'))


@app.route('/login')
def login():
    abort(401)
    this_is_never_executed()

