# """
# Author   : HarperHao
# TIME    ： 2020/10/24
# FUNCTION:
# """
# from flask import Flask
# from flask_sqlalchemy import SQLAlchemy
# import views, commands
#
# app = Flask(__name__)
# app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:root@127.0.0.1/watchlist'
# app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
#
# db = SQLAlchemy(app)
