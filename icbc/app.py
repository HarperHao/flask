"""
Author   : HarperHao
TIME    ： 2020/10/
FUNCTION:  
"""
from flask import Flask

app = Flask(__name__)


@app.route('/')
def hello_world():
    return 'Hello World!'


if __name__ == '__main__':
    app.run()
