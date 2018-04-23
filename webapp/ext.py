#!/usr/bin/env python
# -*- coding: utf-8 -*-

from flask_moment import Moment
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_socketio import SocketIO
from flask_apscheduler import APScheduler
from flask_session import Session
from tasks.taskconfig import TaskConifg

sess = Session()
moment = Moment()
db = SQLAlchemy()
login_manager = LoginManager()
login_manager.session_protection = 'strong'
login_manager.login_view = 'main.login'
login_manager.refresh_view = 'main.login'
socketio = SocketIO()
scheduler = APScheduler()