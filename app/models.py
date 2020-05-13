#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @project : flask构建微电影网站
# @File    : models.py
# @Time    : 2020/3/5 13:23
# @Author  : WeiHua
# @Software: PyCharm
from datetime import datetime

from werkzeug.security import generate_password_hash, check_password_hash

from app import db


class User(db.Model):
    """会员字段"""
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True)        # id
    name = db.Column(db.String(100), unique=True)       # name
    _password = db.Column(db.String(100))               # password
    email = db.Column(db.String(100), unique=True)      # email
    phone = db.Column(db.String(11), unique=True)       # phone
    info = db.Column(db.Text)                           # 简介
    face = db.Column(db.String(255), unique=True)       # 头像地址
    add_time = db.Column(db.DateTime, index=True, default=datetime.now)
    uuid = db.Column(db.String(255), unique=True)       # 唯一标识
    user_logs = db.relationship('UserLog', backref='user')   # 会员日志外键关系关联
    comments = db.relationship('Comment', backref='user')   # 评论的外键关联
    movie_col = db.relationship('MovieCol', backref='user')

    def __repr__(self):
        return "<User %r>" % self.name

    @property
    def password(self):
        return self._password

    @password.setter
    def password(self, raw_password):
        self._password = generate_password_hash(raw_password)

    def check_password(self, raw_password):
        return check_password_hash(self.password, raw_password)


class UserLog(db.Model):
    """会员登录日志"""
    __tablename__ = 'userlog'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    ip = db.Column(db.String(100))
    add_time = db.Column(db.DateTime, index=True, default=datetime.now)

    def __repr__(self):
        return "<UserLog %r>" % self.id


class Tag(db.Model):
    """标签模型"""
    __tablename__ = 'tag'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), unique=True)
    add_time = db.Column(db.DateTime, index=True, default=datetime.now)
    tag_movies = db.relationship('Movie', backref='tag')    # 电影外键关系关联

    def __repr__(self):
        return "<Tag %r>" % self.name


class Movie(db.Model):
    """电影模型"""
    __tablename__ = 'movie'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255), unique=True)      # 标题
    url = db.Column(db.String(255), unique=True)        # 电影链接
    info = db.Column(db.Text)                           # 电影简介
    logo = db.Column(db.String(255), unique=True)       # 封面
    star = db.Column(db.SmallInteger)                   # 星级
    play_num = db.Column(db.BigInteger)                 # 播放量
    comment_num = db.Column(db.BigInteger)              # 评论两
    tag_id = db.Column(db.Integer, db.ForeignKey('tag.id')) #所属标签
    area = db.Column(db.String(255))                    # 上映地区
    release_time = db.Column(db.DateTime)               # 上映时间
    length = db.Column(db.String(100))                  # 播放时长
    add_time = db.Column(db.DateTime, index=True, default=datetime.now)     # 添加时间
    comments = db.relationship('Comment', backref='movie')       # 评论外键关系关联
    movie_col = db.relationship('MovieCol', backref='movie')     # 收藏外键关联

    def __repr__(self):
        return "<Movie %s>" % self.title


class Preview(db.Model):
    """预告电影"""
    __tablename__ = 'preview'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255), unique=True)      # 标题
    logo = db.Column(db.String(255), unique=True)       # 封面
    add_time = db.Column(db.DateTime, index=True, default=datetime.now)

    def __repr__(self):
        return "<Preview %s>" % self.title


class Comment(db.Model):
    """电影评论"""
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.Text)                # 内容
    movie_id = db.Column(db.Integer, db.ForeignKey('movie.id'))     # 所属电影
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))       # 所属用户
    add_time = db.Column(db.DateTime, index=True, default=datetime.now)     # 添加时间

    def __repr__(self):
        return "<Preview %s>" % self.id


class MovieCol(db.Model):
    """电影收藏"""
    __tablename__ = 'moviecol'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    movie_id = db.Column(db.Integer, db.ForeignKey('movie.id'))
    add_time = db.Column(db.DateTime, index=True, default=datetime.now)

    def __repr__(self):
        return "<Movie %r>" % self.id


class Auth(db.Model):
    """权限模型"""
    __tablename__ = 'auth'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), unique=True)
    url = db.Column(db.String(255), unique=True)
    add_time = db.Column(db.DateTime, index=True, default=datetime.now)

    def __repr__(self):
        return "<Auth %r>" % self.name      # %r用于__repr__中， %s用于__str__中


class Role(db.Model):
    """角色模型"""
    __tablename__ = 'role'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), unique=True)   # 权限名称
    auths = db.Column(db.String(600))  # 权限列表
    add_time = db.Column(db.DateTime, index=True, default=datetime.now)
    admins = db.relationship('Admin', backref='role')

    def __repr__(self):
        return "<Role %r>" % self.name      # %r用于__repr__中， %s用于__str__中


class Admin(db.Model):
    """管理员"""
    __tablename__ = 'admin'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), unique=True)
    _password = db.Column(db.String(100), nullable=False)
    is_super = db.Column(db.SmallInteger)       # 是否为超级管理员， 0为超级管理员
    role_id = db.Column(db.Integer, db.ForeignKey('role.id'))   # 所属角色
    add_time = db.Column(db.DateTime, index=True, default=datetime.now)
    adminlogs = db.relationship('AdminLog', backref='admin')
    oplogs = db.relationship('Oplog', backref='admin')

    def __repr__(self):
        return "<Admin %r>" % self.name      # %r用于__repr__中， %s用于__str__中

    @property
    def password(self):
        return self._password

    @password.setter
    def password(self, raw_password):
        self._password = generate_password_hash(raw_password)

    def check_password(self, raw_password):
        return check_password_hash(self._password, raw_password)


class AdminLog(db.Model):
    """管理员登录日志"""
    __tablename__ = 'adminlog'
    id = db.Column(db.Integer, primary_key=True)
    admin_id = db.Column(db.Integer, db.ForeignKey('admin.id'))
    ip = db.Column(db.String(100))
    add_time = db.Column(db.DateTime, index=True, default=datetime.now)

    def __repr__(self):
        return "<AdminLog %r>" % self.id      # %r用于__repr__中， %s用于__str__中


class Oplog(db.Model):
    """管理员操作日志"""
    __tablename__ = 'oplog'
    id = db.Column(db.Integer, primary_key=True)
    admin_id = db.Column(db.Integer, db.ForeignKey('admin.id'))
    ip = db.Column(db.String(100))
    reason = db.Column(db.String(255))           # 操作的原因
    add_time = db.Column(db.DateTime, index=True, default=datetime.now)

    def __repr__(self):
        return "<Oplog %r>" % self.id      # %r用于__repr__中， %s用于__str__中


if __name__ == '__main__':
    from manager import app
    with app.app_context():
        db.create_all(app=app)
