"""
Author   : HarperHao
TIME    ： 2020/10/20
FUNCTION:  图书管理系统
1.配置数据库
2.添加书和作者的模型(数据库模型)
3.添加数据
4.使用模版显示数据库查询的数据
5.使用WTF显示表单
6.实现相关的增删逻辑
"""

from flask import Flask, render_template, flash, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
import pymysql
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:root@127.0.0.1/flask_books'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.secret_key = 'HarperHao'

pymysql.install_as_MySQLdb()
db = SQLAlchemy(app)


# 自定义表单类
class AuthorForm(FlaskForm):
    author = StringField('作者', validators=[DataRequired()])
    book = StringField('书籍', validators=[DataRequired()])
    submit = SubmitField('提交')


# 定义书和作者的模型
# 作者模型
class Author(db.Model):
    # 表名
    __tablename__ = 'authors'

    # 字段
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(16), unique=True)

    # 关系引用
    # books是给自己(Author模型)用的, author是给Book模型用的
    books = db.relationship('Book', backref='author')

    def __repr__(self):
        return 'Author: %s' % self.name


# 书籍模型
class Book(db.Model):
    __tablename__ = 'books'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(16), unique=True)
    author_id = db.Column(db.Integer, db.ForeignKey('authors.id'))

    def __repr__(self):
        return 'Book: %s %s' % (self.name, self.author_id)


# 删除书籍
@app.route('/delete_book/<book_id>')
def delete_book(book_id):
    # 查询数据库是否有该id的书
    book = Book.query.get(book_id)
    print('删除时的book:'.format(book))
    # 如果有的话就删除
    if book:
        try:
            db.session.delete(book)
            db.session.commit()
        except Exception as e:
            print(e)
            flash("删除书籍错误")
            db.session.rollback()
    # 如果没的话提示错误
    else:
        flash('书籍找不到')

    return redirect(url_for('index'))


# 删除作者
@app.route('/delete_author/<author_id>')
def delete_author(author_id):
    # 查询数据库，是否有该ID的作者，如果有的话就删除（先删除书，再删除作者），没有的话提示错误
    author = Author.query.get(author_id)
    # 如果有的话就删除
    if author:
        try:
            # 删除书籍
            Book.query.filter_by(author_id=author_id).delete()
            # 删除作者
            db.session.delete(author)
            db.session.commit()
        except Exception as e:
            print(e)
            flash("删除作者出错")
            db.session.rollback()
    # 如果作者不存在
    else:
        flash('作者找不到')
    # 重定向
    return redirect(url_for('index'))


@app.route('/', methods=["GET", "POST"])
def index():
    # 创建表单类
    author_form = AuthorForm()
    """
    验证逻辑
    1.调用WTF的函数实现验证（验证有没有错误）
    2.获取数据
    3.判断作者是否存在
    4.作者存在的话，判断书籍是否存在，书籍不存在的话就添加数据，书籍存在的话就提示错误
    5.作者不存在的话，添加作者和书籍
    6.验证不通过的话就提示错误
    """
    # 如果参数方面没有错误
    if author_form.validate_on_submit():
        # 获取数据
        author_name = author_form.author.data
        book_name = author_form.book.data
        # 判断作者是否存在
        author = Author.query.filter_by(name=author_name).first()
        # 如果作者存在
        if author:
            # 判断书籍是否存在
            book = Book.query.filter_by(name=book_name).first()
            print("book:".format(book))
            # 如果书籍已经存在
            if book:
                flash("已存在同名书籍")
            # 如果书籍不存在,添加书籍
            else:
                try:
                    new_book = Book(name=book_name, author_id=author.id)
                    db.session.add(new_book)
                    db.session.commit()
                except Exception as e:
                    print(e)
                    flash("添加书籍失败")
                    db.session.rollback()
        # 如果作者不存在，添加作者和书籍
        else:
            try:
                new_author = Author(name=author_name)
                db.session.add(new_author)
                db.session.commit()
                new_book = Book(name=book_name, author_id=new_author.id)
                db.session.add(new_book)
                db.session.commit()
            except Exception as e:
                print(e)
                flash('添加作者和书籍失败')
                db.session.rollback()
    # 如果参数方面有错误，flash
    else:
        if request.method == "POST":
            flash("参数有误！")
    # 查询所有作者的信息，让信息传递给模板
    authors = Author.query.all()
    print(authors)

    return render_template('books.html', authors=authors, form=author_form)


db.drop_all()
db.create_all()

# 生成数据
au1 = Author(name='千峰')
au2 = Author(name='百战')
au3 = Author(name='黑马')

# 把数据提交给用户会话
db.session.add_all([au1, au2, au3])
# 提交会话
db.session.commit()

bk1 = Book(name='Python入门', author_id=au1.id)
bk2 = Book(name='Flask入门', author_id=au1.id)
bk3 = Book(name='Java基础', author_id=au2.id)
bk4 = Book(name='数据库原理', author_id=au2.id)
bk5 = Book(name='数据采集', author_id=au2.id)
bk6 = Book(name='C程序设计', author_id=au3.id)
db.session.add_all([bk1, bk2, bk3, bk4, bk5, bk6])
db.session.commit()
app.run()
