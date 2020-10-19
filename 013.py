"""
Author   : HarperHao
TIME    ： 2020/10/19
FUNCTION:  使用WTF实现表单
"""

from flask import Flask, request, render_template, flash
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, EqualTo

app = Flask(__name__)
app.secret_key = 'HarperHao'

 
class LoginForm(FlaskForm):
    username = StringField('用户名:', validators=[DataRequired()])
    password = PasswordField('密码：', validators=[DataRequired()])
    password2 = PasswordField('确认密码：', validators=[DataRequired(), EqualTo('password', '密码输入的不一致')])
    submit = SubmitField('提交')


@app.route('/', methods=['GET', 'POST'])
def index():
    login_form = LoginForm()

    if request.method == "POST":
        username = request.form.get('username')
        password = request.form.get('password')
        password2 = request.form.get('password2')
        print(username)
        print(password)
        print(password2)
        # 验证参数
        if login_form.validate_on_submit():
            flash('Success')
        else:
            flash('参数有误')
    return render_template('index2.html', login_form=login_form)


if __name__ == '__main__':
    app.run()
