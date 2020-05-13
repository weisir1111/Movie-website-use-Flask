#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @project : flask构建微电影网站
# @File    : decorators.py
# @Time    : 2020/3/10 20:56
# @Author  : WeiHua
# @Software: PyCharm
from functools import wraps
from flask import session, redirect, url_for, request, abort

from app.models import Admin, Role, Auth


# 登录装饰器
def admin_login_required(func):
    @wraps(func)
    def inner(*args, **kwargs):
        if not session.get('admin'):
            return redirect(url_for('admin.login', next=request.url))
        return func(*args, **kwargs)
    return inner


# 权限控制装饰器
def admin_auth(func):
    @wraps(func)
    def inner(*args, **kwargs):
        admin = Admin.query.join(Role).filter(
            Admin.role_id == Role.id,
            Admin.id == session['admin_id']
        ).first()
        auths = admin.role.auths
        auths = list(map(lambda x: int(x), auths.split(',')))
        auth_list = Auth.query.all()
        urls = [v.url for v in auth_list for val in auths if val == v.id]
        rule = request.url_rule
        if str(rule) not in urls:
            abort(404)
        return func(*args, **kwargs)
    return inner
