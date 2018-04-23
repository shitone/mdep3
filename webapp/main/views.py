#!/usr/bin/env python
# -*- coding: utf-8 -*-
from flask import render_template, request, json, url_for, redirect, session
from . import main
from .. import db
from ..models import User, Department
from flask_login import login_user, login_required, logout_user, fresh_login_required
import urllib


@main.route('/')
@main.route('/index')
@fresh_login_required
def index():
    return render_template('index.html')


@main.route('/welcome')
def welcome():
    return render_template('iplogin.html')


@main.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password_md5 = request.form['password']
        remember = request.form['remember']
        user = User.query.filter_by(username=username).first()
        if user is not None and user.verify_password(password_md5):
            login_user(user, remember)
            return json.dumps(dict(succeed=True, ac=user.areacode))
        return json.dumps(dict(succeed = False))
    return render_template('login.html')


@main.route('/iplogin', methods=['GET', 'POST'])
def iplogin():
    ip = request.remote_addr
    f = urllib.urlopen('http://10.116.32.81/aws_cimiss/index.php/Api/getFocusFromIp/?ip=' + ip)
    data = json.loads(f.read())
    areacode = data['code'][0:4] + '00'
    user = User.query.filter_by(areacode=areacode).first()
    if user is not None:
        login_user(user, 0)
        return json.dumps(dict(succeed=True, un=user.username, ac=user.areacode))
    return json.dumps(dict(succeed = False))


@main.route('/logout')
@fresh_login_required
def logout():
    logout_user()
    return redirect(url_for('main.index'))


@main.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'GET':
        return render_template('register.html')
    if request.method == 'POST':
        username = request.form['username']
        password_md5 = request.form['password']
        truename = request.form['truename']
        department = request.form['department']
        phone = request.form['phone']
        user = User(username=username, password_md5=password_md5, truename=truename, department=department, phone=phone)
        db.session.add(user)
        db.session.commit()
        return json.dumps(dict(succeed=True))


@main.route('/department', methods=['GET', 'POST'])
def department():
    departments = Department.query.all()
    dpts = []
    for department in departments:
        dpt = {}
        dpt['id'] = department.id
        dpt['name'] = department.name
        dpts.append(dpt)
    return json.dumps(dict(dpts = dpts))