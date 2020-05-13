#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @project : flask构建微电影网站
# @File    : forms.py
# @Time    : 2020/3/5 11:57
# @Author  : WeiHua
# @Software: PyCharm
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, FileField, TextAreaField, SelectField, DateField, \
    SelectMultipleField
from wtforms.validators import DataRequired, ValidationError, EqualTo
from app.models import Admin, Tag, Auth, Role


class LoginForm(FlaskForm):
    """管理员登录表单"""
    account = StringField(
        label='账号',
        validators=[
            DataRequired('请输入账号')
        ],
        description='账号',
        render_kw={  # StringField、PasswordField等可以直接定义render_kw将值传到前端
            "class": "form-control",  # 若render_kw中不包含name或者id，则自动生成
            "placeholder": "请输入账号！",
        }
    )
    pwd = PasswordField(
        label='密码',
        validators=[
            DataRequired('请输入密码！')
        ],
        description='密码',
        render_kw={
            "class": "form-control",
            "placeholder": "请输入密码！",
        }

    )
    submit = SubmitField(
        label='提交',
        render_kw={
            'class': 'btn btn-primary btn-block btn-flat',
            'formnovalidate': ''  # formnovalidate用来阻止html5的自动校验require
        }
    )

    def validate_account(self, field):
        account = field.data
        admin = Admin.query.filter(Admin.name == account).first()
        if not admin:
            raise ValidationError('账号不存在')


class TagForm(FlaskForm):
    name = StringField(
        label='名称',
        validators=[
            DataRequired('请输入标签！')
        ],
        description='标签',
        render_kw={
            "class": "form-control",
            "id": "input_name",
            "placeholder": "请输入标签名称！",
        }
    )
    submit = SubmitField(
        label='编辑',
        render_kw={
            "type": "submit",
            "class": "btn btn-primary",
            'formnovalidate': ''
        }
    )


class MovieForm(FlaskForm):
    title = StringField(
        label='片名',
        validators=[
            DataRequired('请输入片名！')
        ],
        description='片名',
        render_kw={
            "class": "form-control",
            "id": "input_title",
            "placeholder": "请输入片名！"
        }
    )
    url = FileField(
        label='文件',
        validators=[
            DataRequired('请上传文件！')
        ],
        description='文件'
    )
    info = TextAreaField(
        label='简介',
        validators=[
            DataRequired('请输入电影简介！')
        ],
        description='简介',
        render_kw={
            "class": "form-control",
            "rows": "10",
            "id": "input_info",
        }
    )
    logo = FileField(
        label='封面',
        validators=[
            DataRequired('请上传封面！')
        ],
        description='封面',
        render_kw={
            'type': 'file',
            'id': 'input_logo'
        }
    )
    star = SelectField(
        label='星级',
        validators=[
            DataRequired('请选择星级！')
        ],
        coerce=int,
        choices=[(1, "1星"), (2, "2星"), (3, "3星"), (4, "4星"), (5, "5星")],
        description='星级',
        render_kw={
            "class": "form-control",
            "id": "input_star"
        }
    )
    tag_id = SelectField(
        label='标签',
        validators=[
            DataRequired('请为电影选择标签！')
        ],
        coerce=int,
        choices=[(v.id, v.name) for v in Tag.query.all()],
        render_kw={
            "class": "form-control",
            "id": "input_tag_id"
        }
    )

    area = StringField(
        label='上映地区',
        validators=[
            DataRequired('请输入上映地区！')
        ],
        description='上映地区',
        render_kw={
            "class": "form-control",
            "id": "input_area",
            "placeholder": "请输入上映地区！"
        }
    )
    length = StringField(
        label='影片时长',
        validators=[
            DataRequired('请输入电影时长！')
        ],
        description='上映时间',
        render_kw={
            "class": "form-control",
            "id": "input_length",
            "placeholder": "请输入片长！"
        }
    )
    release_time = DateField(
        label='上映时间',
        validators=[
            DataRequired('请选择上映时间！')
        ],
        description='上映时间',
        render_kw={
            "class": "form-control",
            "id": "input_release_time",
            "placeholder": "请选择上映时间！"
        }
    )
    submit = SubmitField(
        label='提交',
        render_kw={
            "type": "submit",
            "class": "btn btn-primary",
            'formnovalidate': ''
        }
    )


class PreviewForm(FlaskForm):
    title = StringField(
        label='预告标题',
        validators=[
            DataRequired('请输入预告标题！')
        ],
        description='预告标题',
        render_kw={
            "class": "form-control",
            "id": "input_title",
            "placeholder": "请输入预告标题！"
        }
    )
    logo = FileField(
        label='预告封面',
        validators=[
            DataRequired('请上传预告封面！')
        ],
        description='预告封面',
        render_kw={
            "type": "file",
            "id": "input_logo"
        }
    )
    submit = SubmitField(
        label='提交',
        render_kw={
            "class": "btn btn-primary",
            'formnovalidate': ''
        }
    )


class PasswordForm(FlaskForm):
    old_password = PasswordField(
        label='旧密码',
        validators=[
            DataRequired('请输入旧密码！')
        ],
        description='旧密码',
        render_kw={
            "class": "form-control",
            "id": "input_pwd",
            "placeholder": "请输入旧密码！"

        }
    )
    new_password = PasswordField(
        label='新密码',
        validators=[
            DataRequired('请输入新密码！')
        ],
        description='新密码',
        render_kw={
            "class ": "form-control",
            "id": "input_newpwd",
            "placeholder": "请输入新密码！"
        }
    )
    submit = SubmitField(
        label='提交',
        render_kw={
            "class ": "btn btn-primary",
            'formnovalidate': ''
        }
    )

    def validate_old_password(self, field):
        from flask import session
        password = field.data
        name = session['admin']
        print(name)
        admin = Admin.query.filter(Admin.name == name).first()
        if not admin.check_password(password):
            raise ValidationError('旧密码不正确！')


class AuthForm(FlaskForm):
    name = StringField(
        label='权限名称',
        validators=[
            DataRequired('请输入权限名称！')
        ],
        description='权限名称',
        render_kw={
            "class": "form-control",
            "id": "input_name",
            "placeholder": "请输入权限名称！"
        }
    )
    url = StringField(
        label='权限地址',
        validators=[
            DataRequired('请输入权限地址！')
        ],
        description='权限地址',
        render_kw={
            "class": "form-control",
            "id": "input_url",
            "placeholder": "请输入权限地址！"
        }
    )
    submit = SubmitField(
        label='提交',
        render_kw={
            "class": "btn btn-primary",
            'formnovalidate': ''
        }
    )


class RoleForm(FlaskForm):
    name = StringField(
        label='角色名称',
        validators=[
            DataRequired('请输入角色名称！')
        ],
        description='角色名称',
        render_kw={
            "class": "form-control",
            "id": "input_name",
            "placeholder": "请输入角色名称！"
        }
    )
    auths = SelectMultipleField(
        label='权限列表',
        validators=[
            DataRequired('请选择权限列表！')
        ],
        description='权限列表',
        coerce=int,
        choices=[(v.id, v.name) for v in Auth.query.all()],
        render_kw={
            "class": "form-control"
        }
    )
    submit = SubmitField(
        label='提交',
        render_kw={
            "class": "btn btn-primary",
            'formnovalidate': ''
        }
    )


class AdminForm(FlaskForm):
    name = StringField(
        label='管理员名称',
        validators=[
            DataRequired('请输入管理员名称！')
        ],
        description='管理员名称',
        render_kw={
            "class": "form-control",
            "id": "input_name",
            "placeholder": "请输入管理员名称！"
        }
    )
    password = PasswordField(
        label='密码',
        validators=[
            DataRequired('请输入管理员密码！')
        ],
        description='密码',
        render_kw={
            "class": "form-control",
            "id": "input_pwd",
            "placeholder": "请输入管理员密码！"
        }
    )
    re_password = PasswordField(
        label='重复密码',
        validators=[
            DataRequired('请输入管理员重复密码！'),
            EqualTo('password', message='两次密码不一致！')
        ],
        description='重复密码',
        render_kw={
            "class": "form-control",
            "id": "input_re_pwd",
            "placeholder": "请输入管理员重复密码！"
        }
    )
    role_id = SelectField(
        label='所属角色',
        validators=[
            DataRequired('请选择所属角色！')
        ],
        coerce=int,
        choices=[(v.id, v.name) for v in Role.query.all()],
        render_kw={
            "class": "form-control",
            "id": "input_role_id"
        }
    )
    submit = SubmitField(
        label='提交',
        render_kw={
            "class": "btn btn-primary",
            'formnovalidate': ''
        }
    )
