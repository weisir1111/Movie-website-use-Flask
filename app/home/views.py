#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @project : flask构建微电影网站
# @File    : views.py
# @Time    : 2020/3/5 11:57
# @Author  : WeiHua
# @Software: PyCharm
import json
import os
import stat
from datetime import datetime

from flask import render_template, request, redirect, url_for, flash, session
from werkzeug.utils import secure_filename

from app import db, app
from app.home.decorators import user_login_required
from app.home.forms import RegisterForm, LoginForm, UserDetailForm, ChangePasswordField, CommentForm
from app.models import User, UserLog, Preview, Tag, Movie, Comment, MovieCol
from . import home
import uuid


# 会员登录
@home.route('/login/', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        data = form.data
        user = User.query.filter(User.name == data.get('name')).first()
        if not user.check_password(data.get('password')):
            flash('用户密码错误！', 'error')
            return redirect(url_for('home.login'))
        session['user'] = user.name
        session['user_id'] = user.id
        userlog = UserLog(
            user_id=user.id,
            ip=request.remote_addr,
        )
        db.session.add(userlog)
        db.session.commit()
        return redirect(url_for('home.index', page=1))
    return render_template('home/login.html', form=form)


# 会员登出
@home.route('/logout/', methods=['GET'])
def logout():
    del session['user']
    del session['user_id']
    return redirect(url_for('home.login'))


# 会员注册
@home.route('/register/', methods=['GET', 'POST'])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        data = form.data
        new_user = User(
            name=data['name'],
            password=data['password'],
            email=data['email'],
            phone=data['phone'],
            uuid=uuid.uuid4().hex
        )
        db.session.add(new_user)
        db.session.commit()
        flash('注册成功！', 'ok')
    return render_template('home/register.html', form=form)


# 修改文件名称
def change_filename(filename):
    file_info = os.path.splitext(filename)
    filename = datetime.now().strftime('%Y%m%d%H%M%S') + uuid.uuid4().hex + file_info[1]
    return filename


@home.route('/user/', methods=['GET', 'POST'])
@user_login_required
def user():
    form = UserDetailForm()
    user = User.query.get(int(session['user_id']))
    form.face.validators = []
    if request.method == 'GET':
        form.name.data = user.name
        form.email.data = user.email
        form.info.data = user.info
        form.phone.data = user.phone
    if form.validate_on_submit():
        data = form.data
        file_face = secure_filename(form.face.data.filename)
        if not os.path.exists(app.config['FACE_DIR']):
            os.makedirs(app.config['FACE_DIR'])
        os.chmod(app.config['FACE_DIR'], stat.S_IRWXU | stat.S_IRGRP | stat.S_IROTH)
        user.face = change_filename(file_face)
        form.face.data.save(os.path.join(app.config['FACE_DIR'], user.face))
        user.name = data['name']
        user.email = data['email']
        user.phone = data['phone']
        user.info = data['info']
        db.session.add(user)
        db.session.commit()
        flash('修改成功！', 'ok')
        return redirect(url_for('home.user'))
    return render_template('home/user.html', form=form, user=user)


# 修改密码
@home.route('/pwd/', methods=['GET', 'POST'])
@user_login_required
def pwd():
    form = ChangePasswordField()
    if form.validate_on_submit():
        data = form.data
        user = User.query.get(session['user_id'])
        user.password = data['new_password']
        db.session.add(user)
        db.session.commit()
        flash('修改密码成功，请重新登录！', 'ok')
        return redirect(url_for("home.login"))
    return render_template('home/pwd.html', form=form)


@home.route('/comments/<int:page>')
@user_login_required
def comments(page=None):
    if page is None:
        page = 1
    page_data = Comment.query.join(
        User
    ).join(
        Movie
    ).filter(
        Movie.id == Comment.movie_id,
        User.id == session['user_id']
    ).order_by(
        Comment.add_time.desc()
    ).paginate(page=page, per_page=10)
    return render_template('home/comments.html', page_data=page_data)


# 会员登录日志
@home.route('/loginlog/<int:page>/', methods=['GET'])
@user_login_required
def loginlog(page=None):
    if page is None:
        page = 1
    page_data = UserLog.query.filter(
        UserLog.user_id == int(session['user_id'])
    ).order_by(
        UserLog.add_time.desc()
    ).paginate(page=page, per_page=10)
    return render_template('home/loginlog.html', page_data=page_data)


# 添加电影收藏
@home.route('/moviecol/add', methods=['GET'])
@user_login_required
def moviecol_add():
    user_id = request.args.get('user_id')
    movie_id = request.args.get('movie_id')
    movicol = MovieCol.query.filter(
        MovieCol.movie_id == movie_id,
        MovieCol.user_id == user_id
    ).first()
    if movicol:
        data = dict(ok=0)
    else:
        moviecol = MovieCol(
            user_id=user_id,
            movie_id=movie_id
        )
        db.session.add(moviecol)
        db.session.commit()
        data = dict(ok=1)
    return json.dumps(data)


# 电影收藏
@home.route('/moviecol/<int:page>/')
@user_login_required
def moviecol(page=None):
    if page is None:
        page = 1
    page_data = MovieCol.query.join(Movie).join(User).filter(
        MovieCol.movie_id == Movie.id,
        User.id == int(session['user_id']),
    ).order_by(
        MovieCol.add_time.desc()
    ).paginate(page=page, per_page=10)
    return render_template('home/moviecol.html',page_data=page_data)


# 首页-标签筛选
@home.route('/<int:page>/', methods=['GET'])
def index(page=None):
    if page is None:
        page = 1
    tags = Tag.query.all()
    page_data = Movie.query
    # tag
    tid = request.args.get('tid', 0)
    if int(tid) != 0:
        page_data = page_data.filter(Movie.tag_id == int(tid))
    # 星级
    star = request.args.get('star', 0)
    if int(star) != 0:
        page_data = page_data.filter(Movie.star == int(star))
    # 时间排序
    time = request.args.get('time', 0)
    if int(time) != 0:
        if int(time) == 0:
            page_data = page_data.order_by(Movie.add_time.desc())
        else:
            page_data = page_data.order_by(Movie.add_time.asc())
    # 播放量排序
    play_num = request.args.get('play_num', 0)
    if int(play_num) != 0:
        if int(play_num) == 0:
            page_data = page_data.order_by(Movie.play_num.desc())
        else:
            page_data = page_data.order_by(Movie.play_num.asc())
    # 评论量排序
    comment_num = request.args.get('comment_num', 0)
    if int(comment_num) != 0:
        if int(comment_num) == 0:
            page_data = page_data.order_by(Movie.comment_num.desc())
        else:
            page_data = page_data.order_by(Movie.comment_num.asc())
    page_data = page_data.paginate(page=page, per_page=10)

    p = dict(
        tid=tid,
        star=star,
        time=time,
        play_num=play_num,
        comment_num=comment_num
    )
    return render_template('home/index.html', tags=tags, p=p, page_data=page_data)


# 上映预告
@home.route('/animation/')
def animation():
    data = Preview.query.all()
    print(len(data))
    return render_template('home/animation.html', data=data)


@home.route('/search/<int:page>/', methods=['GET'])
def search(page=None):
    if page is None:
        page = 1
    key = request.args.get('key', '')
    movie_count = Movie.query.filter(Movie.title.ilike('%' + key + '%')).count()
    page_data = Movie.query.filter(Movie.title.ilike('%' + key + '%')).order_by(
        Movie.add_time.desc()
    ).paginate(page=page, per_page=10)
    return render_template('home/search.html', key=key, page_data=page_data, movie_count=movie_count)


@home.route('/play/<int:id>/<int:page>/', methods=['GET', 'POST'])
def play(id=None, page=None):
    movie = Movie.query.join(Tag).filter(
        Tag.id == Movie.tag_id,
        Movie.id == int(id)
    ).first_or_404()
    if page is None:
        page = 1
    page_data = Comment.query.join(
        User
    ).join(
        Movie
    ).filter(
        Movie.id == movie.id,
    ).order_by(
        Comment.add_time.desc()
    ).paginate(page=page, per_page=10)
    movie.play_num += 1
    form = CommentForm()
    if "user" in session and form.validate_on_submit():
        data = form.data
        comment = Comment(
            content=data.get('content'),
            movie_id=movie.id,
            user_id=session['user_id']
        )
        db.session.add(comment)
        db.session.commit()
        movie.comment_num += 1
        db.session.add(movie)
        db.session.commit()
        flash('添加评论成功！', 'ok')
        return redirect(url_for('home.play', id=movie.id, page=1))
    db.session.add(movie)
    db.session.commit()
    return render_template('home/play.html/', movie=movie, form=form, page_data=page_data)
