"""
Author   : HarperHao
TIME    ： 2020/10/20
FUNCTION:  《Flask入门》
"""
from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
import pymysql
import click

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


@app.route('/')
def index():
    movies = Movie.query.all()
    return render_template('index3.html', movies=movies)


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
