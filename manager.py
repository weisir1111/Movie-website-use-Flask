#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @project : flask构建微电影网站
# @File    : manager.py
# @Time    : 2020/3/5 11:47
# @Author  : WeiHua
# @Software: PyCharm
from flask_migrate import MigrateCommand
from flask_script import Manager, Server

from app import app, db
from app.models import User, Admin


manager = Manager(app)
manager.add_command('db', MigrateCommand)       # 可以用db关联到init、migrate、upgrade等命令
manager.add_command('runserver', Server())      # 用来关联server的启动，Server()可以设置host、port等参数


@manager.option('-n', '--name', dest='name')
@manager.option('-p', '--password', dest='password')
@manager.option('-e', '--email', dest='email')
def create_user(name, password, email, phone):
    user = User(name=name, password=password, email=email)
    db.session.add(user)
    db.session.commit()
    print('添加用户成功')


@manager.option('-n', '--name', dest='name')
@manager.option('-p', '--password', dest='password')
@manager.option('-i', '--is_super', dest='is_super')
@manager.option('-r', '--role_id', dest='role_id')
def create_admin(name, password, is_super, role_id):
    admin = Admin(name=name, password=password, is_super=is_super, role_id=role_id)
    db.session.add(admin)
    db.session.commit()
    print('添加管理员成功')


if __name__ == '__main__':
    # manager.run()       # 这里必须为manager.run()
    app.run()
