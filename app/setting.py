#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @project : flask构建微电影网站
# @File    : setting.py
# @Time    : 2020/3/5 12:13
# @Author  : WeiHua
# @Software: PyCharm
import os


class BaseConfig(object):
    UP_DIR = os.path.join(os.path.abspath(os.path.dirname(__file__)), 'static', 'uploads')  # 图片信息保存路径
    FACE_DIR = os.path.join(os.path.abspath(os.path.dirname(__file__)), 'static', 'uploads','users')  # 图片信息保存路径


class DevelopmentConfig(BaseConfig):
    DEBUG = True
    pass


class ProductionConfig(BaseConfig):
    pass
