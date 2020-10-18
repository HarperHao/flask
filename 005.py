"""
Author   : HarperHao
TIME    ： 2020/10/18
FUNCTION:  渲染模板
"""
from flask import render_template
from flask import Flask

app = Flask(__name__)


@app.route('/hello/')
@app.route('/hello/<name>')
def hello(name=None):
    return render_template('hello.html',name=name)
