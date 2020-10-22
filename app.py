"""
Author   : HarperHao
TIME    ： 2020/10/20
FUNCTION:  《Flask入门》
"""
from flask import Flask, render_template, request, url_for, redirect, flash
from flask_sqlalchemy import SQLAlchemy
import pymysql
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:root@127.0.0.1/WatchList'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.secret_key = 'HarperHao'

pymysql.install_as_MySQLdb()
db = SQLAlchemy(app)


# 构造数据库模型
class User(db.Model):
    # 表名
    __tablename__ = 'user'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20))
    username = db.Column(db.String(20))
    password_hash = db.Column(db.String(128))

    # 用来设置密码的方法
    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    # 用来验证密码的方法
    def validate_password(self, password):
        return check_password_hash(self.password_hash, password)


class Movie(db.Model):
    __tablename__ = 'movie'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(60))
    # 电影的年份
    year = db.Column(db.String(4))


# 模版上下文处理函数
@app.context_processor
def inject_user():
    user = User.query.first()
    # 返回{'user':'user'}
    return dict(user=user)


# 404错误处理函数
@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404


# 删除视图
@app.route('/movie/delete/<int:movie_id>', methods=["POST"])
def delete(movie_id):
    movie = Movie.query.get_or_404(movie_id)
    db.session.delete(movie)
    db.session.commit()
    flash('此电影被删除')
    return redirect(url_for('index'))


# 编辑视图
@app.route('/movie/edit/<int:movie_id>', methods=['GET', 'POST'])
def edit(movie_id):
    movie = Movie.query.get_or_404(movie_id)
    if request.method == 'POST':
        title = request.form.get('title')
        year = request.form.get('year')
        # 如果数据错误
        if not title or not year or len(year) > 4 or len(title) > 60:
            flash('无效输入!')
            return redirect(url_for('edit', movie_id=movie_id))
        # 如果输入没有问题，则更改数据库中的内容
        movie.title = title
        movie.year = year
        db.session.commit()
        flash('数据更新成功')
        # 数据更新成功，返回主界面
        return redirect(url_for('index'))

    return render_template('edit.html', movie=movie)


# 主视图
@app.route('/', methods=['GET', 'POST'])
def index():
    print('test')

    if request.method == 'POST':
        # 获取表单数据
        # 传入表单对应输入字段的name值
        # request.form是一个特殊的字典
        title = request.form.get('title')
        year = request.form.get('year')
        print(title)
        print(year)
        # 验证数据
        if not title or not year or len(year) > 4 or len(title) > 60:
            # 显示错误信息
            flash('Invalid input.')
            # 无效输入的话重定向到主页
            return redirect(url_for('index'))
        # 如果数据无误的话，将表单信息添加到数据库中
        else:
            movie_item = Movie(title=title, year=year)
            db.session.add(movie_item)
            db.session.commit()
            flash('成功添加')
            # 重定向回主界面
            return redirect(url_for('index'))
    user = User.query.first()
    movies = Movie.query.all()
    return render_template('index3.html', user=user, movies=movies)


db.drop_all()
db.create_all()
# 生成数据库数据
name = 'HarperHao'
movies = [
    {'title': 'My Neighbor Totoro', 'year': '1988'},
    {'title': 'Dead Poets Society', 'year': '1989'},
    {'title': 'A Perfect World', 'year': '1993'},
    {'title': 'Leon', 'year': '1994'},
    {'title': 'Mahjong', 'year': '1996'},
    {'title': 'Swallowtail Butterfly', 'year': '1996'},
    {'title': 'King of Comedy', 'year': '1999'},
    {'title': 'Devils on the Doorstep', 'year': '1999'},
    {'title': 'WALL-E', 'year': '2008'},
    {'title': 'The Pork of Music', 'year': '2012'},
]
# 创建user数据
user = User(name=name)
db.session.add(user)
db.session.commit()
# 创建books数据
for m in movies:
    movie = Movie(title=m['title'], year=m['year'])
    db.session.add(movie)

db.session.commit()
