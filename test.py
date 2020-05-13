#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @project : flask构建微电影网站
# @File    : test.py
# @Time    : 2020/3/10 17:36
# @Author  : WeiHua
# @Software: PyCharm


#admin_user
insert into user(name,_password,email,info) values('鼠','1234','1234@qq.com','鼠');
insert into user(name,_password,email,info) values('牛','1234','12345@qq.com','牛');
insert into user(name,_password,email,info) values('兔','1234','12346@qq.com','兔');
insert into user(name,_password,email,info) values('龙','1234','12347@qq.com','龙');
insert into user(name,_password,email,info) values('蛇','1234','12348@qq.com','蛇');
insert into user(name,_password,email,info) values('马','1234','12349@qq.com','马');
insert into user(name,_password,email,info) values('羊','1234','123412@qq.com','羊');
insert into user(name,_password,email,info) values('猴','1234','1234121@qq.com','猴');
insert into user(name,_password,email,info) values('鸡','1234','1234124@qq.com','鸡');
insert into user(name,_password,email,info) values('狗','1234','1234345@qq.com','狗');
insert into user(name,_password,email,info) values('猪','1234','12345343@qq.com','猪');
insert into user(name,_password,email,info) values('驴','1234','123554324@qq.com','驴');
ALTER TABLE user auto_increment=1;


#评论
insert into comment(movie_id,user_id,content,add_time) values(7,9,"好看",now());
insert into comment(movie_id,user_id,content,add_time) values(7,10,"不错",now());
insert into comment(movie_id,user_id,content,add_time) values(7,11,"经典",now());
insert into comment(movie_id,user_id,content,add_time) values(7,12,"给力",now());
insert into comment(movie_id,user_id,content,add_time) values(8,13,"难看",now());
insert into comment(movie_id,user_id,content,add_time) values(8,14,"无聊",now());
insert into comment(movie_id,user_id,content,add_time) values(8,15,"乏味",now());
insert into comment(movie_id,user_id,content,add_time) values(8,16,"无感",now());
ALTER TABLE comment auto_increment=1;

#收藏
insert into moviecol(movie_id, user_id,add_time) values(10,8,now());
insert into moviecol(movie_id, user_id,add_time) values(10,9,now());
insert into moviecol(movie_id, user_id,add_time) values(11,10,now());
insert into moviecol(movie_id, user_id,add_time) values(12,11,now());
insert into moviecol(movie_id, user_id,add_time) values(13,12,now());
insert into moviecol(movie_id, user_id,add_time) values(14,13,now());
insert into moviecol(movie_id, user_id,add_time) values(12,14,now());
insert into moviecol(movie_id, user_id,add_time) values(13,15,now());
insert into moviecol(movie_id, user_id,add_time) values(11,16,now());

#会员登录日志
insert into userlog(user_id, ip, add_time) values(1,'192.168.0.12',now());
insert into userlog(user_id, ip, add_time) values(2,'192.168.0.13',now());
insert into userlog(user_id, ip, add_time) values(4,'192.168.0.14',now());
insert into userlog(user_id, ip, add_time) values(5,'192.168.0.15',now());
insert into userlog(user_id, ip, add_time) values(6,'192.168.0.16',now());
insert into userlog(user_id, ip, add_time) values(7,'192.168.0.17',now());
insert into userlog(user_id, ip, add_time) values(8,'192.168.0.18',now());
insert into userlog(user_id, ip, add_time) values(9,'192.168.0.19',now());
insert into userlog(user_id, ip, add_time) values(10,'192.168.0.20',now());
insert into userlog(user_id, ip, add_time) values(11,'192.168.0.121',now());
insert into userlog(user_id, ip, add_time) values(12,'192.168.0.123',now());