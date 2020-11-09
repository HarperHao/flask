"""
Author   : HarperHao
TIME    ： 2020/11/9
FUNCTION:  Flask 内置的信号
访问index视图产生异常之前，钩子函数捕捉到此状态码的错误，抢先执行，进入到500.html
同时got_request_exception信号捕捉到异常，将此异常和此应用名写入到txt中去。
获取此应用的名字还使用了g全局对象和current_app以及上下文对象。
"""
from flask import Flask, got_request_exception, current_app, g, render_template

app = Flask(__name__)


def request_exception_fun(sender, exception):
    print(exception)
    with open('exception_log.txt', 'a', encoding='GBK')as f:
        log = "用户：{},异常信息：{}".format(g.username, exception)
        f.write(log + '\n')


got_request_exception.connect(request_exception_fun)


@app.route('/')
def index():
    g.username = current_app.name
    a = 1 / 0
    return 'Flask 内置信号'


@app.errorhandler(500)
def page_not_found(error):
    # print(error)
    return render_template('500.html'), 500


if __name__ == '__main__':
    app.run()
