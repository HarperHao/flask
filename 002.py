"""
Author   : HarperHao
TIME    ： 2020/10/18
FUNCTION:  唯一的ＵＲＬ/重定向行为
"""

from flask import Flask

app = Flask(__name__)


@app.route('/')
def projects():
    return 'The project page'


@app.route('/about')
def about():
    return 'The about page'
