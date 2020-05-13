#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @project : flask构建微电影网站
# @File    : views.py
# @Time    : 2020/3/5 11:57
# @Author  : WeiHua
# @Software: PyCharm
import os
import stat
import uuid
from datetime import datetime
from functools import wraps

from flask import render_template, redirect, url_for, flash, session, request, abort
from werkzeug.utils import secure_filename

from app.admin.decorators import admin_login_required, admin_auth
from app.admin.forms import LoginForm, TagForm, MovieForm, PreviewForm, PasswordForm, AuthForm, RoleForm, AdminForm
from app.models import Admin, Tag, Movie, Preview, User, Comment, MovieCol, Oplog, AdminLog, UserLog, Auth, Role
from app import app, db
from . import admin


# 上下应用处理器
@admin.context_processor
def tpl_extra():
    data = dict(
        online_time=datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    )
    return data





# 首页
@admin.route('/')
@admin_login_required
def index():
    return render_template('admin/index.html')


# 登入
@admin.route('/login/', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        data = form.data
        name = data.get('account')
        password = data.get('pwd')
        admin = Admin.query.filter(Admin.name == name).first()
        if not admin.check_password(password):
            flash('密码错误！', 'error')
            return redirect(url_for('admin.login'))  # redirect不能带参数，但是flash是基于session的，因此不依赖于传参。
        session['admin'] = name
        session['admin_id'] = admin.id
        admin_log = AdminLog(
            admin_id=admin.id,
            ip=request.remote_addr
        )
        db.session.add(admin_log)
        db.session.commit()
        return redirect(request.args.get('next') or url_for('admin.index'))
    return render_template('admin/login.html', form=form)


# 登出
@admin.route('/logout/')
@admin_login_required
def logout():
    # session.pop('admin', None)   # 不要使用pop方式，使用下面的del方式，否则不管用
    del session['admin']
    del session['admin_id']
    return redirect(url_for('admin.login'))


# 编辑密码
@admin.route('/pwd/', methods=['GET', 'POST'])
@admin_login_required
def pwd():
    form = PasswordForm()
    if form.validate_on_submit():
        data = form.data
        admin = Admin.query.filter(Admin.name == session['admin']).first()
        new_password = data.get('new_password')
        admin.password = new_password
        db.session.add(admin)
        db.session.commit()
        flash('修改密码成功，请重新登录！', 'ok')
        return redirect(url_for('admin.logout'))
    return render_template('admin/pwd.html', form=form)


# 标签添加
@admin.route('/tag/add/', methods=['GET', 'POST'])
@admin_login_required
@admin_auth
def tag_add():
    form = TagForm()
    if form.validate_on_submit():
        data = form.data
        name = data.get('name')
        tag = Tag.query.filter(Tag.name == name).first()
        if tag:
            flash('标签已存在', 'error')
            return redirect(url_for('admin.tag_add'))
        tag = Tag(name=name)
        db.session.add(tag)
        db.session.commit()
        flash('添加标签成功！', 'ok')
        oplog = Oplog(
            admin_id=session['admin_id'],
            ip=request.remote_addr,
            reason='添加标签%s' % data['name']
        )
        db.session.add(oplog)
        db.session.commit()
        redirect(url_for('admin.tag_add'))
    return render_template('admin/tag_add.html', form=form)


# 标签列表
@admin.route('/tag/list/<int:page>/', methods=['GET'])
@admin_login_required
@admin_auth
def tag_list(page=None):
    if page is None:
        page = 1
    page_data = Tag.query.order_by(Tag.add_time.desc()).paginate(page=page, per_page=10)
    return render_template('admin/tag_list.html', page_data=page_data)


# 标签删除
@admin.route('/tag/del/<int:id>/')
@admin_login_required
@admin_auth
def tag_del(id=None):
    tag = Tag.query.get_or_404(id)
    db.session.delete(tag)
    db.session.commit()
    flash('删除标签成功', 'ok')
    return redirect(url_for('admin.tag_list', page=1))


# 标签编辑
@admin.route('/tag/edit/<int:id>/', methods=['GET', 'POST'])
@admin_login_required
@admin_auth
def tag_edit(id=None):
    form = TagForm()
    tag = Tag.query.get_or_404(id)
    if form.validate_on_submit():
        data = form.data
        name = data.get('name')
        tag_count = Tag.query.filter(Tag.name == name).count()
        if tag.name != name and tag_count != 0:
            flash('标签已存在', 'error')
            return redirect(url_for('admin.tag_edit', id=tag.id))
        tag.name = name
        db.session.add(tag)  # 这里不用使用update，因为使用update还需要根据tag.id查询一次tag。
        db.session.commit()  # 而使用add方法合适，因此tag中已经存储了主键id，只是改变了name。所以添加时会覆盖主键值形同的数据
        flash('修改标签成功！', 'ok')
        redirect(url_for('admin.tag_edit', id=tag.id))
    return render_template('admin/tag_edit.html', form=form, tag=tag)


# 修改文件名称
def change_filename(filename):
    file_info = os.path.splitext(filename)
    filename = datetime.now().strftime('%Y%m%d%H%M%S') + uuid.uuid4().hex + file_info[1]
    return filename


# 电影添加
@admin.route('/movie/add', methods=['GET', 'POST'])
@admin_login_required
@admin_auth
def movie_add():
    form = MovieForm()
    if form.validate_on_submit():
        data = form.data
        # 以下全都是为了设置文件的保存路径做的工作
        file_url = secure_filename(form.url.data.filename)
        file_logo = secure_filename(form.logo.data.filename)
        if not os.path.exists(app.config['UP_DIR']):
            os.makedirs(app.config['UP_DIR'])
        os.chmod(app.config['UP_DIR'], stat.S_IRWXU | stat.S_IRGRP | stat.S_IROTH)
        url = change_filename(file_url)
        logo = change_filename(file_logo)
        # 设置路径以及文件名称完毕
        form.url.data.save(os.path.join(app.config['UP_DIR'], url))
        form.logo.data.save(os.path.join(app.config['UP_DIR'], logo))
        movie = Movie(
            title=data['title'],
            url=url,
            info=data['info'],
            logo=logo,
            star=int(data['star']),
            play_num=0,
            comment_num=0,
            tag_id=int(data['tag_id']),
            area=data['area'],
            release_time=data['release_time'],
            length=data['length'],
        )
        db.session.add(movie)
        db.session.commit()
        flash('添加电影成功！', 'ok')
        return redirect(url_for('admin.movie_add'))
    return render_template('admin/movie_add.html', form=form)


# 电影列表
@admin.route('/movie/list/<int:page>/')
@admin_login_required
@admin_auth
def movie_list(page=None):
    if page is None:
        page = 1
    page_data = Movie.query.join(Tag).filter(
        Tag.id == Movie.tag_id
    ).order_by(
        Movie.add_time.desc()
    ).paginate(page=page, per_page=2)
    return render_template('admin/movie_list.html', page_data=page_data)


# 删除电影
@admin.route('movie/del/<int:id>/')
@admin_login_required
@admin_auth
def movie_del(id=None):
    movie = Movie.query.get_or_404(int(id))
    db.session.delete(movie)
    db.session.commit()
    flash('删除电影成功！', 'ok')
    return redirect(url_for('admin.movie_list', page=1))


# 编辑电影
@admin.route('movie/edit/<int:id>', methods=['GET', 'POST'])
@admin_login_required
@admin_auth
def movie_edit(id=None):
    form = MovieForm()
    movie = Movie.query.get_or_404(int(id))
    form.url.validators = []  # 即不对url进行表单验证
    form.logo.validators = []  # 不对logo进行表单验证
    if request.method == 'GET':
        form.info.data = movie.info
        form.star.data = movie.star
        form.tag_id.data = movie.tag_id
    if form.validate_on_submit():
        data = form.data
        count = Movie.query.filter(Movie.title == data.get('title')).count()
        if count == 1 and data['title'] != movie.title:
            flash('片名已经存在！', 'error')
            return redirect(url_for('admin.movie_edit', id=id))

        if not os.path.exists(app.config['UP_DIR']):
            os.makedirs(app.config['UP_DIR'])
            os.chmod(app.config['UP_DIR'], stat.S_IRWXU | stat.S_IRGRP | stat.S_IROTH)

        if form.url.data.filename != "":
            file_url = secure_filename(form.url.data.filename)
            movie.url = change_filename(file_url)
            form.url.data.save(os.path.join(app.config['UP_DIR'], movie.url))

        if form.logo.data.filename != "":
            file_logo = secure_filename(form.logo.data.filename)
            movie.logo = change_filename(file_logo)
            form.logo.data.save(os.path.join(app.config['UP_DIR'], movie.logo))

        movie.title = data['title']
        movie.info = data['info']
        movie.star = int(data['star'])
        movie.tag_id = int(data['tag_id'])
        movie.area = data['area']
        movie.release_time = data['release_time']
        movie.length = data['length']
        db.session.add(movie)
        db.session.commit()
        flash('修改电影成功！', 'ok')
        return redirect(url_for('admin.movie_edit', id=id))
    return render_template('admin/movie_edit.html', form=form, movie=movie)


# 预告电影添加
@admin.route('/preview/add/', methods=['GET', 'POST'])
@admin_login_required
@admin_auth
def preview_add():
    form = PreviewForm()
    if form.validate_on_submit():
        data = form.data
        file_logo = secure_filename(form.logo.data.filename)
        if not os.path.exists(app.config['UP_DIR']):
            os.makedirs(app.config['UP_DIR'])
        os.chmod(app.config['UP_DIR'], stat.S_IRWXU | stat.S_IRGRP | stat.S_IROTH)
        logo = change_filename(file_logo)
        form.logo.data.save(os.path.join(app.config['UP_DIR'], logo))
        preview = Preview(
            title=data.get('title'),
            logo=logo
        )
        db.session.add(preview)
        db.session.commit()
        flash('添加预告成功！', 'ok')
        return redirect(url_for('admin.preview_add'))
    return render_template('admin/preview_add.html', form=form)


# 预告电影列表
@admin.route('/preview/list/<int:page>/', methods=['GET'])
@admin_login_required
@admin_auth
def preview_list(page=None):
    if page is None:
        page = 1
    page_data = Preview.query.order_by(Preview.add_time.desc()).paginate(page=page, per_page=2)
    return render_template('admin/preview_list.html', page_data=page_data)


# 预告删除
@admin.route('preview/del/<int:id>/')
@admin_login_required
@admin_auth
def preview_del(id=None):
    preview = Preview.query.get_or_404(int(id))
    db.session.delete(preview)
    db.session.commit()
    flash('预告删除成功！', 'ok')
    return redirect(url_for('admin.preview_list', page=1))


# 预告编辑
@admin.route('preview/edit/<int:id>/')
@admin_login_required
@admin_auth
def preview_edit(id):
    form = PreviewForm()
    preview = Preview.query.get_or_404(int(id))
    form.logo.validators = []
    if request.method == 'GET':
        form.title.data = preview.title
    if form.validate_on_submit():
        data = form.data
        if form.logo.data.filename != "":
            file_logo = secure_filename(form.logo.data.filename)
            preview.logo = change_filename(file_logo)
            form.logo.data.save(os.path.join(app.config['UP_DIR'], preview.logo))
        preview.title = data.get('title')
        db.session.add(preview)
        db.session.commit()
        flash('预告修改成功！', 'ok')
        return redirect(url_for('admin.preview_edit', id=id))
    return render_template('admin/preview_edit.html', form=form, preview=preview)


# 会员列表
@admin.route('/user/list/<int:page>/', methods=['GET'])
@admin_login_required
@admin_auth
def user_list(page=None):
    if page is None:
        page = 1
    page_data = User.query.order_by(
        User.add_time.desc()
    ).paginate(page=page, per_page=10)
    return render_template('admin/user_list.html', page_data=page_data)


# 会员查看
@admin.route('/user/view/<int:id>/', methods=['GET', 'POST'])
@admin_login_required
@admin_auth
def user_view(id=None):
    user = User.query.get_or_404(int(id))
    return render_template('admin/user_view.html', user=user)


# 会员删除
@admin.route('/user.del/<int:id>/', methods=['GET'])
@admin_login_required
@admin_auth
def user_del(id=None):
    user = User.query.get_or_404(int(id))
    db.session.delete(user)
    db.session.commit()
    flash('删除会员成功！', 'ok')
    return redirect(url_for('admin.user_list', page=1))


# 评论列表
@admin.route('/comment/list/<int:page>/', methods=['GET'])
@admin_login_required
@admin_auth
def comment_list(page=None):
    if page is None:
        page = 1
    page_data = Comment.query.join(User).join(Movie).filter(
        Movie.id == Comment.movie_id,
        User.id == Comment.user_id
    ).order_by(Comment.add_time.desc()).paginate(page=page, per_page=3)
    return render_template('admin/comment_list.html', page_data=page_data)


# 删除评论
@admin.route('/comment/del/<int:id>/', methods=['GET'])
@admin_login_required
@admin_auth
def comment_del(id=None):
    comment = Comment.query.get_or_404(int(id))
    db.session.delete(comment)
    db.session.commit()
    flash('删除评论成功！', 'ok')
    return redirect(url_for('admin.comment_list', page=1))


# 电影收藏列表
@admin.route('/moviecol/list/<int:page>', methods=['GET'])
@admin_login_required
@admin_auth
def moviecol_list(page=None):
    if page is None:
        page = 1
    page_data = MovieCol.query.join(User).join(Movie).filter(
        MovieCol.user_id == User.id,
        MovieCol.movie_id == Movie.id
    ).order_by(
        MovieCol.add_time.desc()
    ).paginate(page=page, per_page=10)
    return render_template('admin/moviecol_list.html', page_data=page_data)


# 删除电影收藏
@admin.route('moviecol/del/<int:id>/', methods=['GET'])
@admin_login_required
@admin_auth
def moviecol_del(id=None):
    moviecol = MovieCol.query.get_or_404(int(id))
    db.session.delete(moviecol)
    db.session.commit()
    flash('删除收藏成功！', 'ok')
    return redirect(url_for('admin.moviecol_list', page=1))


# 操作日志列表
@admin.route('/oplog/list/<int:page>/', methods=['GET'])
@admin_login_required
@admin_auth
def oplog_list(page=None):
    if page is None:
        page = 1
    page_data = Oplog.query.join(Admin).filter(
        Admin.id == Oplog.admin_id).order_by(
        Oplog.add_time.desc()
    ).paginate(page=page, per_page=10)
    return render_template('admin/oplog_list.html', page_data=page_data)


# 用户登录日志列表
@admin.route('/userloginlog/list/<int:page>/', methods=['GET'])
@admin_login_required
@admin_auth
def userloginlog_list(page=None):
    if page is None:
        page = 1
    page_data = UserLog.query.join(User).filter(
        UserLog.user_id == User.id
    ).order_by(
        UserLog.add_time.desc()
    ).paginate(page=page, per_page=10)
    return render_template('admin/userloginlog_list.html', page_data=page_data)


# 管理员登录日志列表
@admin.route('/adminloginlog/list/<int:page>/', methods=['GET'])
@admin_login_required
@admin_auth
def adminloginlog_list(page=None):
    if page is None:
        page = 1
    page_data = AdminLog.query.join(Admin).filter(
        AdminLog.admin_id == Admin.id
    ).order_by(
        AdminLog.add_time.desc()
    ).paginate(page=page, per_page=10)
    return render_template('admin/adminloginlog_list.html', page_data=page_data)


# 添加权限
@admin.route('/auth/add', methods=['GET', 'POST'])
@admin_login_required
@admin_auth
def auth_add():
    form = AuthForm()
    if form.validate_on_submit():
        data = form.data
        auth = Auth(
            name=data.get('name'),
            url=data.get('url')
        )
        db.session.add(auth)
        db.session.commit()
        flash('添加权限成功！', 'ok')
        oplog = Oplog(
            admin_id=session['admin_id'],
            ip=request.remote_addr,
            reason='添加权限%s' % data['name']
        )
        db.session.add(oplog)
        db.session.commit()
        return redirect(url_for('admin.auth_add'))
    return render_template('admin/auth_add.html', form=form)


# 权限列表
@admin.route('/auth/list/<int:page>/', methods=['GET'])
@admin_login_required
@admin_auth
def auth_list(page=None):
    if page is None:
        page = 1
    page_data = Auth.query.order_by(
        Auth.add_time.desc()
    ).paginate(page=page, per_page=10)
    return render_template('admin/auth_list.html', page_data=page_data)


# 添加角色
@admin.route('/role/add/', methods=['GET', 'POST'])
@admin_login_required
@admin_auth
def role_add():
    form = RoleForm()
    print(request.method)
    if form.validate_on_submit():
        data = form.data
        print(data)
        role = Role(
            name=data['name'],
            auths=','.join(map(lambda x: str(x), data['auths']))
        )
        db.session.add(role)
        db.session.commit()
        flash('添加角色成功！', 'ok')
        return redirect(url_for('admin.role_add'))
    return render_template('admin/role_add.html', form=form)


# 角色列表
@admin.route('/role/list/<int:page>', methods=['GET'])
@admin_login_required
@admin_auth
def role_list(page=None):
    if page is None:
        page = 1
    page_data = Role.query.order_by(
        Role.add_time.desc()
    ).paginate(page=page, per_page=10)
    return render_template('admin/role_list.html', page_data=page_data)


# 删除角色
@admin.route('/role/del/<int:id>/', methods=['GET'])
@admin_login_required
@admin_auth
def role_del(id=None):
    role = Role.query.get_or_404(int(id))
    db.session.delete(role)
    db.session.commit()
    flash('删除角色成功！', 'ok')
    return redirect(url_for('admin.role_list', page=1))


# 编辑角色
@admin.route('/role/edit/<int:id>/', methods=['GET', 'POST'])
@admin_login_required
@admin_auth
def role_edit(id=None):
    form = RoleForm()
    role = Role.query.get_or_404(int(id))
    if request.method == 'GET':
        form.auths.data = list(map(lambda x: int(x), role.auths.split(',')))
    if form.validate_on_submit():
        data = form.data
        role.name = data.get('name')
        role.auths = ','.join(map(lambda x: str(x), data.get('auths')))
        db.session.add(role)
        db.session.commit()
        flash('修改角色成功！', 'ok')
        return redirect(url_for('admin.role_edit', id=id))
    return render_template('admin/role_edit.html', form=form, role=role)


# 权限删除
@admin.route('/auth/del/<int:id>/', methods=['GET'])
@admin_login_required
@admin_auth
def auth_del(id=None):
    auth = Auth.query.get_or_404(int(id))
    db.session.delete(auth)
    db.session.commit()
    flash('删除权限成功！', 'ok')
    return redirect(url_for('admin.auth_list', page=1))


# 编辑权限
@admin.route('/auth/edit/<int:id>/', methods=['GET', 'POST'])
@admin_login_required
@admin_auth
def auth_edit(id=None):
    form = AuthForm()
    auth = Auth.query.get_or_404(int(id))
    if form.validate_on_submit():
        data = form.data
        auth.name = data.get('name')
        auth.url = data.get('url')
        db.session.add(auth)
        db.session.commit()
        flash('修改权限成功！', 'ok')
        return redirect(url_for('admin.auth_edit', id=id))
    return render_template('admin/auth_edit.html', form=form, auth=auth)


# 管理员添加
@admin.route('/admin/add', methods=['GET', 'POST'])
@admin_login_required
@admin_auth
def admin_add():
    form = AdminForm()
    if form.validate_on_submit():
        data = form.data
        admin = Admin(
            name=data.get('name'),
            password=data.get('password'),
            role_id=data.get('role_id'),
            is_super=1
        )
        db.session.add(admin)
        db.session.commit()
        flash('添加管理员成功！', 'ok')
        return redirect(url_for('admin.admin_add'))
    return render_template('admin/admin_add.html', form=form)


# 管理员列表
@admin.route('/admin/list/<int:page>/', methods=['GET'])
@admin_login_required
@admin_auth
def admin_list(page=None):
    if page is None:
        page=1
    page_data = Admin.query.join(Role).filter(
        Admin.role_id == Role.id
    ).order_by(
        Admin.add_time.desc()
    ).paginate(page=page, per_page=10)
    return render_template('admin/admin_list.html', page_data=page_data)
