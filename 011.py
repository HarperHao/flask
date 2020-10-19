"""
Author   : HarperHao
TIME    ： 2020/10/19
FUNCTION:  JinJia2模版的使用
"""

from flask import Flask, render_template

app = Flask(__name__)


@app.route('/')
def index():
    my_name = 'HarperHao'
    my_list = [1, 2, 3, 4, 5]
    my_dict = {
        'name': 'HarperHao',
        'password': "123"

    }
    return render_template('index.html', my_name=my_name, my_list=my_list, my_dict=my_dict)


if __name__ == '__main__':
    app.run()
