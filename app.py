"""
Author   : HarperHao
TIME    ： 2020/10/17
FUNCTION:  测试调试功能，set FLASK_DEBUG=1
"""
from flask import Flask

app = Flask(__name__)


@app.route('/')
def hello_world():
    return 'Hello 638!'


if __name__ == "__main__":
    app.run(host='0.0.0.0')
