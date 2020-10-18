"""
Author   : HarperHao
TIME    ： 2020/10/18
FUNCTION:  路由的学习
"""
from flask import Flask

app = Flask(__name__)


@app.route('/user/<username>')
def show_user_profile(username):
    return "User %s" % escape(username)


@app.route('/post/<int:post_id>')
def show_post(post_id):
    return 'Post %d' % post_id


@app.route('/path/<path:subpath>')
def show_subpath(subpath):
    return 'Subpath %s' % escape(subpath)


@app.route('/hello')
def hello():
    return 'Hello World!'


