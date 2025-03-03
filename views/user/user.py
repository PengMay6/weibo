# import datetime
#
# from flask import Flask,session,render_template,redirect,Blueprint,request
# from utils.databaseManage import query
# import time
# from utils.errorResponse import errorResponse
# ub = Blueprint('user',__name__,url_prefix='/user',template_folder='templates')
#
# @ub.route('/login',methods=['GET','POST'])
# def login():
#     if request.method == 'GET':
#         return render_template('login.html')
#     else:
#         def filter_fn(user):
#             return request.form['username'] in user and request.form['password'] in user
#         users = query('select * from user', [], 'select')
#         login_success = list(filter(filter_fn,users))
#         if not len(login_success):return errorResponse('账号或密码错误')
#
#         session['username'] = request.form['username']
#         return redirect('/page/home')
#
# @ub.route('/register',methods=['GET','POST'])
# def register():
#     if request.method == 'GET':
#         return render_template('register.html')
#     else:
#         if request.form['password'] != request.form['checkPassword']:return errorResponse('两次密码不符合')
#         def filter_fn(user):
#             return request.form['username'] in user
#
#         users = query('select * from user',[],'select')
#         filter_list = list(filter(filter_fn,users))
#         if len(filter_list):
#             return errorResponse('该用户名已被注册')
#         else:
#             time_tuple = time.localtime(time.time())
#             query('''
#                 insert into user(username,password,createTime) values(%s,%s,%s)
#             ''',[request.form['username'],request.form['password'],str(time_tuple[0]) + '-' + str(time_tuple[1]) + '-' + str(time_tuple[2])])
#
#         return redirect('/user/login')
#
# @ub.route('/logOut')
# def logOut():
#         session.clear()
#         return redirect('/user/login')

import datetime
from flask import Flask, session, render_template, redirect, Blueprint, request
from utils.databaseManage import query
from werkzeug.security import generate_password_hash, check_password_hash
from utils.errorResponse import errorResponse

ub = Blueprint('user', __name__, url_prefix='/user', template_folder='templates')

# 检查用户名是否已存在
def is_username_exist(username):
    users = query('SELECT * FROM user WHERE username = %s', [username], 'select')
    return bool(users)

# 执行注册操作
def perform_registration(username, password):
    current_time = datetime.datetime.now().strftime('%Y-%m-%d')
    hashed_password = generate_password_hash(password)
    try:
        query('INSERT INTO user (username, password, createTime) VALUES (%s, %s, %s)',
              [username, hashed_password, current_time])
        return True
    except Exception as e:
        print(f"Database error during registration: {e}")
        return False

# 执行登录操作
def perform_login(username, password):
    user = query('SELECT * FROM user WHERE username = %s', [username], 'select')
    if user:
        stored_password = user[0][1]  # 假设密码在第二列
        if check_password_hash(stored_password, password):
            return True
    return False

@ub.route('/login', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'GET':
        return render_template('login.html', error=error)
    else:
        username = request.form.get('username')
        password = request.form.get('password')
        if perform_login(username, password):
            session['username'] = username
            return redirect('/page/home')
        else:
            error = '账号或密码错误'
            return render_template('login.html', error=error)

@ub.route('/register', methods=['GET', 'POST'])
def register():
    error = None
    if request.method == 'GET':
        return render_template('register.html', error=error)
    else:
        username = request.form.get('username')
        password = request.form.get('password')
        check_password = request.form.get('checkPassword')

        if password != check_password:
            error = '两次密码不符合'
        elif is_username_exist(username):
            error = '该用户名已被注册'
        else:
            if perform_registration(username, password):
                return redirect('/user/login')
            else:
                error = '注册失败，请稍后再试'

        return render_template('register.html', error=error)

@ub.route('/logOut')
def logOut():
    session.clear()
    return redirect('/user/login')