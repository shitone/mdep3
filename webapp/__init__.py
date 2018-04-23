#!/usr/bin/env python
# -*- coding: utf-8 -*-

from flask import Flask
from config import Config, Basic
from webapp.tasks.taskconfig import TaskConifg
from ext import moment, db, login_manager, socketio, scheduler, sess
import logging

logging.basicConfig(level=logging.ERROR, format='%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s', datefmt='%Y-%m-%d %H:%M:%S', filename='log.txt', filemode='a')


def create_app():
    app = Flask(__name__)
    # app.config['CELERY_IMPORTS'] = ('backgroundtask.add', )
    # app.config['CELERY_BROKER_URL'] = 'redis://localhost:6379/0'
    # app.config['CELERY_RESULT_BACKEND'] = 'redis://localhost:6379/0'
    app.config.from_object(Config)
    app.config.from_object(TaskConifg)
    Config.init_app(app)
    # app.config['SESSION_TYPE'] = 'filesystem'
    # app.config['SESSION_FILE_DIR'] = tempfile.gettempdir()
    # app.permanent_session_lifetime = datetime.timedelta(days=1)
    # sess.init_app(app)
    moment.init_app(app)
    db.app = app
    db.init_app(app)
    login_manager.init_app(app)
    # celery.init_app(app)

    from .main import main as main_blueprint
    from .cimiss import cimiss as cimiss_blueprint
    from .product import product as product_blueprint
    from .page2 import page2 as page2_blueprint

    app.register_blueprint(main_blueprint)
    app.register_blueprint(cimiss_blueprint, url_prefix='/cimiss')
    app.register_blueprint(product_blueprint, url_prefix='/product')
    app.register_blueprint(page2_blueprint, url_prefix='/page2')
    socketio.init_app(app , async_mode='eventlet', message_queue=Basic.SOCKET_RMQ + '/socketio')

    scheduler.init_app(app)
    scheduler.start()
    return app

