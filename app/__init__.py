#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @project : flask构建微电影网站
# @File    : __init__.py
# @Time    : 2020/3/5 11:56
# @Author  : WeiHua
# @Software: PyCharm
import os

"""
注意：1、以后init文件中不要使用create_app的方式来返回app，否则造成插件未注册进去时就是调用models，出现错误
     2、SQLAlchemy的定义尽量放到init文件中，否则容易出现相互导入错误
     3、db的注册即db = SQLAlchemy(app)一定要放到注册蓝图前面，否则model里无法使用db模型，因为蓝图没注册时，意味着视图函数还未注册
"""

from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config.from_object('app.setting.DevelopmentConfig')
app.config.from_object('app.secure.DevelopmentConfig')

# 注册db
db = SQLAlchemy(app)

# 注册蓝图
from app.admin import admin as admin_blueprint
from app.home import home as home_blueprint
app.register_blueprint(home_blueprint)
app.register_blueprint(admin_blueprint, url_prefix='/admin')


# flask自带的处理页面错误的函数，必须定义在__init__中，不能放到视图函数中
@app.errorhandler(404)
def page_not_found(error):
    return render_template('home/404.html'), 404

