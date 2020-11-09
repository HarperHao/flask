"""
Author   : HarperHao
TIME    ： 2020/10/20
FUNCTION:  《Flask入门》
"""
from flask import Flask, render_template, request, url_for, redirect, flash
from flask_sqlalchemy import SQLAlchemy
import pymysql
from werkzeug.security import generate_password_hash, check_password_hash
import click
from flask_login import LoginManager, UserMixin, login_user, logout_user, login_required, current_user

app = Flask(__name__)

app.secret_key = 'HarperHao'
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:root@127.0.0.1/watchlist'
# app.config['SQLALCHEMY_DATABASE_URI'] = prefix + os.path.join(app.root_path, 'data.sqlite')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
pymysql.install_as_MySQLdb()
db = SQLAlchemy(app)
login_manager = LoginManager(app)


# 构造数据库模型
class User(db.Model, UserMixin):
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



# 编辑视图
@app.route('/movie/edit/<int:movie_id>', methods=['GET', 'POST'])
@login_required  # 登录保护
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


# 用户回调函数
@login_manager.user_loader
def load_user(user_id):
    # 用user_id作为主键去查询对应的用户
    user = User.query.get(int(user_id))
    return user


login_manager.login_view = 'login'


@app.route('/settings', methods=['GET', 'POST'])
@login_required
def settings():
    """支持登录用户name的修改"""
    if request.method == 'POST':
        name = request.form['name']

        if not name or len(name) > 20:
            flash("无效的输入")
            return redirect(url_for('settings'))

        current_user.name = name
        db.session.commit()
        flash('用户名已修改')
        return redirect(url_for('index'))

    return render_template('settings.html')


# 用户认证函数(登录函数)
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        # 判断是否为空输入
        if not username or not password:
            flash('无效的输入')
            return redirect(url_for('login'))
        # 输入格式正确
        else:
            user = User.query.first()
            # 验证用户名和密码是否一致
            if username == user.username and user.validate_password(password):
                login_user(user)
                flash('登录成功！')
                return redirect(url_for('index'))
            # 如果用户名和密码不一致
            else:
                flash('用户名或密码错误！')
                return redirect(url_for('login'))
    return render_template('login.html')


@app.route('/logout')
@login_required
def logout():
    logout_user()  # 登出用户
    flash('再见')
    return redirect(url_for('index'))


# 主视图
@app.route('/', methods=['GET', 'POST'])
def index():
    print('test')

    if request.method == 'POST':
        # 获取表单数据
        # 传入表单对应输入字段的name值
        # request.form是一个特殊的字典

        # 如果当前用户没有认证
        if not current_user.is_authenticated:
            return redirect(url_for('index'))

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


@app.cli.command()
@click.option('--username', prompt=True, help='The username used to login')
@click.option('--password', prompt=True, hide_input=True, confirmation_prompt=True, help='The password used to login')
def admin(username, password):
    """创建管理员用户"""
    db.create_all()

    user = User.query.first()
    print(user.username)
    print(user)
    flag=True
    if user is not None:
        user.username = username
        user.set_password(password)
        flag=False
    # 如果管理员还没有被创建，则创建一个管理员
    else:
        click.echo('Creating user...')
        user = User(username=username, name='Admin')
        user.set_password(password)
        db.session.add(user)
    # 提交会话
    db.session.commit()
    click.echo('创建管理员成功')
    print(flag)


@app.cli.command()
@click.option('--drop', is_flag=True, help="Create after drop")
def initdb(drop):
    if drop:
        db.drop_all()
    db.create_all()
    click.echo('初始化成功')


@app.cli.command()
def forge():
    """生成数据"""
    # db.create_all()到底有什么用，为什么每个函数都在用它
    db.create_all()
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
    # 创建books数据
    for m in movies:
        movie = Movie(title=m['title'], year=m['year'])
        db.session.add(movie)
    db.session.commit()
    click.echo('创建数据成功')


