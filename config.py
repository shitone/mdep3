#!/usr/bin/env python
# -*- coding: utf-8 -*-


class Config(object):
    SECRET_KEY = 'hard to guess string'

    # DEBUG = True

    SQLALCHEMY_COMMIT_ON_TEARDOWN = True
    SQLALCHEMY_TRACK_MODIFICATIONS = True
    # SQLALCHEMY_DATABASE_URI = 'mysql+mysqlconnector://root:onceas@10.116.8.254/medp'
    SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://root:onceas@10.116.8.254/medp'
    # SQLALCHEMY_DATABASE_URI = 'sqlite:///D:/PycharmProjects/mdep/readline.db'

    @staticmethod
    def init_app(app):
        pass


class Basic(object):
    TASK_RMQ = 'amqp://xxzx:123456@10.116.32.197:5672'
    SOCKET_RMQ = 'amqp://xxzx:123456@10.116.32.197:5672'

