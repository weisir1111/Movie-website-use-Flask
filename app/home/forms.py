#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @project : flask构建微电影网站
# @File    : forms.py
# @Time    : 2020/3/5 11:57
# @Author  : WeiHua
# @Software: PyCharm
from flask import session
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, FileField, TextAreaField
from wtforms.validators import DataRequired, EqualTo, Email, Regexp, ValidationError

from app.models import User


class RegisterForm(FlaskForm):
    name = StringField(
        label='昵称',
        validators=[
            DataRequired("请输入昵称！")
        ],
        description='昵称',
        render_kw={
            "class ": "form-control input-lg",
            "placeholder": "昵称",
            "autofocus": ""
        }
    )
    email = StringField(
        label='邮箱',
        validators=[
            DataRequired('请输入邮箱！'),
            Email('邮箱格式不正确！')
        ],
        description='邮箱',
        render_kw={
            "id": "input_email",
            "class": "form-control input-lg",
            "placeholder": "邮箱",
            "autofocus": ""
        }
    )
    phone = StringField(
        label='手机',
        validators=[
            DataRequired('请输入手机号！'),
            Regexp('1[3458]\d{9}', message='手机格式不正确！')  # 正则验证器
        ],
        description='手机',
        render_kw={
            "id": "input_phone",
            "class ": "form-control input-lg",
            "placeholder": "手机",
            "autofocus": ""
        }
    )
    password = PasswordField(
        label='密码',
        validators=[
            DataRequired('请输入密码！')
        ],
        description='密码',
        render_kw={
            "id": "input_password",
            "class ": "form-control input-lg",
            "placeholder": "密码",
            "autofocus": ""
        }
    )
    repassword = PasswordField(
        label='确认密码',
        validators=[
            DataRequired('请重新输入密码！'),
            EqualTo('password', message='两次密码不一致！')
        ],
        description='确认密码',
        render_kw={
            "id": "input_repassword",
            "class": "form-control input-lg",
            "placeholder": "确认密码",
            "autofocus": ""
        }
    )
    submit = SubmitField(
        label='注册',
        render_kw={
            "class": "btn btn-lg btn-success btn-block",
            'formnovalidate': ''
        }
    )

    def validate_name(self, field):
        name = field.data
        count = User.query.filter(User.name == name).count()
        if count == 1:
            raise ValidationError('昵称已被注册！')

    def validate_email(self, field):
        email = field.data
        count = User.query.filter(User.email == email).count()
        if count == 1:
            raise ValidationError('邮箱已被注册！')

    def validate_phone(self, field):
        phone = field.data
        count = User.query.filter(User.phone == phone).count()
        if count == 1:
            raise ValidationError('手机号已被注册！')


class LoginForm(FlaskForm):
    name = StringField(
        label='账号',
        validators=[
            DataRequired('请输入用户名！')
        ],
        description='账号',
        render_kw={
            "id": "input_contact",
            "class": "form-control input-lg",
            "placeholder": "用户名/邮箱/手机号码",
            "autofocus": ""
        }
    )
    password = PasswordField(
        label='密码',
        validators=[
            DataRequired('请输入密码！')
        ],
        description='密码',
        render_kw={
            "id": "input_password",
            "class": "form-control input-lg",
            "placeholder": "密码"
        }
    )
    submit = SubmitField(
        label='登录',
        render_kw={
            "class": "btn btn-lg btn-success btn-block",
            'formnovalidate': ''
        }
    )

    def validate_name(self, field):
        name = field.data
        count = User.query.filter(User.name == name).count()
        if count == 0:
            raise ValidationError('用户名不存在！')


class UserDetailForm(FlaskForm):
    name = StringField(
        label='昵称',
        validators=[
            DataRequired('请输入昵称！')
        ],
        description='账号',
        render_kw={
            "id": "input_contact",
            "class": "form-control",
            "placeholder": "用户名/邮箱/手机号码",
            "autofocus": ""
        }
    )
    email = StringField(
        label='邮箱',
        validators=[
            DataRequired('请输入邮箱！'),
            Email('邮箱格式不正确！')
        ],
        description='邮箱',
        render_kw={
            "id": "input_email",
            "class": "form-control",
            "placeholder": "邮箱",
            "autofocus": ""
        }
    )
    phone = StringField(
        label='手机',
        validators=[
            DataRequired('请输入手机号！'),
            Regexp('1[3458]\d{9}', message='手机格式不正确！')  # 正则验证器
        ],
        description='手机',
        render_kw={
            "id": "input_phone",
            "class ": "form-control",
            "placeholder": "手机",
            "autofocus": ""
        }
    )
    face = FileField(
        label='头像',
        validators=[
            DataRequired('请上传头像')
        ],
        description='头像'
    )
    info = TextAreaField(
        label='简介',
        validators=[
            DataRequired('请输入简介！')
        ],
        description='简介',
        render_kw={
            "class": 'form-control',
            "rows": "10"
        }
    )
    submit = SubmitField(
        label='保存修改',
        render_kw={
            "class ": "btn btn-success",
            'formnovalidate': ''
        }
    )

    def validate_name(self, field):
        name = field.data
        count = User.query.filter(User.name == name).count()
        if name != session['user'] and count == 1:
            raise ValidationError('昵称已存在！')

    def validate_email(self, field):
        email = field.data
        user = User.query.get(int(session['user_id']))
        count = User.query.filter(User.email == email).count()
        if email != user.email and count == 1:
            raise ValidationError('邮箱已被注册！')

    def validate_phone(self, field):
        phone = field.data
        user = User.query.get(int(session['user_id']))
        count = User.query.filter(User.phone == phone).count()
        if phone != user.phone and count == 1:
            raise ValidationError('号码已被注册！')


class ChangePasswordField(FlaskForm):
    old_password = PasswordField(
        label='旧密码',
        validators=[
            DataRequired('请输入旧密码！')
        ],
        render_kw={
            "id": "input_oldpwd",
            "class": "form-control",
            "placeholder": "旧密码"
        }
    )
    new_password = PasswordField(
        label='新密码',
        validators=[
            DataRequired('请输入新密码！')
        ],
        render_kw={
            "id": "input_newpwd",
            "class": "form-control",
            "placeholder": "新密码"
        }
    )
    submit = SubmitField(
        label='修改密码',
        render_kw={
            "class": "btn btn-success",
            'formnovalidate': ''
        }
    )

    def validate_old_password(self, field):
        password = field.data
        user = User.query.get(int(session['user_id']))
        if not user.check_password(password):
            raise ValidationError('旧密码不正确！')


class CommentForm(FlaskForm):
    content = TextAreaField(
        label="内容评论",
        validators=[
            DataRequired('请输入内容！')
        ],
        render_kw={
            "id": "input_content"
        }
    )
    submit = SubmitField(
        label="提交评论",
        render_kw={
            "class ": "btn btn-success",
            "id": "btn-sub",
            'formnovalidate': ''
        }
    )
