#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @project : flask构建微电影网站
# @File    : __init__.py.py
# @Time    : 2020/3/5 11:56
# @Author  : WeiHua
# @Software: PyCharm


from flask import Blueprint


home = Blueprint('home', __name__)
from . import views