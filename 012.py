"""
Author   : HarperHao
TIME    ： 2020/10/19
FUNCTION:  处理web表单
1.获取post参数
2.判断用户名和密码是否为空
3.判断两次密码输入是否一样
4.上述都成立后返回success
5.flash,给模板传递消息
"""
from flask import Flask, request, render_template, flash

app = Flask(__name__)
app.secret_key = 'HarperHao'


@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == "POST":
        username = request.form.get('username')
        password = request.form.get('password')
        password2 = request.form.get('password2')
        print(username)
        print(password)
        print(password2)
        if not all([username, password, password2]):
            flash(u"参数不完整")
        elif password != password2:
            flash(u"两次输入的密码不一致")
        else:
            flash("Success")
    return render_template('index1.html')


if __name__ == '__main__':
    app.run()
