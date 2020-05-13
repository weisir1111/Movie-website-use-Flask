#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @project : flask构建微电影网站
# @File    : decorators.py
# @Time    : 2020/3/17 11:15
# @Author  : WeiHua
# @Software: PyCharm
from functools import wraps

from flask import session, redirect, url_for, request


def user_login_required(func):
    @wraps(func)
    def inner(*args, **kwargs):
        if  not session.get('user'):
            return redirect(url_for('home.login', next=request.url))
        return func(*args, **kwargs)
    return inner