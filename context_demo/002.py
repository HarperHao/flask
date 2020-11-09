"""
Author   : HarperHao
TIME    ： 2020/11/8
FUNCTION:  应用上下文和请求上下文
"""
from flask import Flask, current_app

app = Flask(__name__)
app.test_request_context()

@app.route('/')
def index():
    print()
    app_context = app.app_context()
    #app_context.push()
    print(app.test_request_context())
    return 'hello flask'


if __name__ == '__main__':
    app.run()
