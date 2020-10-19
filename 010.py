"""
Author   : HarperHao
TIME    ： 2020/10/18
FUNCTION:  定义路由参数
"""
from flask import Flask

app = Flask(__name__)


# 定义路由视图
# 支持get和post方法
@app.route('/', methods=['GET', 'POST'])
def index():
    return 'hello flask'


@app.route('/order/<int:order_id>')
def get_order_id(order_id):
    return 'your order id is {}'.format(order_id)


if __name__ == '__main__':
    app.run()
