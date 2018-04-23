#!/usr/bin/env python
# -*- coding: utf-8 -*-
from .ext import db, login_manager
from flask_login import UserMixin


class User(UserMixin, db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), unique=True, index=True)
    password_md5 = db.Column(db.String(128))
    truename = db.Column(db.String(64))
    department = db.Column(db.Integer)
    phone = db.Column(db.String(20))
    areacode = db.Column(db.Integer)

    def verify_password(self, password_md5):
        return self.password_md5 == password_md5


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


class Department(db.Model):
    __tablename__ = 'departments'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64))
    province = db.Column(db.String(16))
    role = db.Column(db.Integer)


class AwsArrival(db.Model):
    __tablename__ = 'aws_arrival'
    data_day = db.Column(db.Date, primary_key=True)
    station_number = db.Column(db.String(6), primary_key=True)
    a00 = db.Column(db.Integer)
    a01 = db.Column(db.Integer)
    a02 = db.Column(db.Integer)
    a03 = db.Column(db.Integer)
    a04 = db.Column(db.Integer)
    a05 = db.Column(db.Integer)
    a06 = db.Column(db.Integer)
    a07 = db.Column(db.Integer)
    a08 = db.Column(db.Integer)
    a09 = db.Column(db.Integer)
    a10 = db.Column(db.Integer)
    a11 = db.Column(db.Integer)
    a12 = db.Column(db.Integer)
    a13 = db.Column(db.Integer)
    a14 = db.Column(db.Integer)
    a15 = db.Column(db.Integer)
    a16 = db.Column(db.Integer)
    a17 = db.Column(db.Integer)
    a18 = db.Column(db.Integer)
    a19 = db.Column(db.Integer)
    a20 = db.Column(db.Integer)
    a21 = db.Column(db.Integer)
    a22 = db.Column(db.Integer)
    a23 = db.Column(db.Integer)
    p00 = db.Column(db.Integer)
    p01 = db.Column(db.Integer)
    p02 = db.Column(db.Integer)
    p03 = db.Column(db.Integer)
    p04 = db.Column(db.Integer)
    p05 = db.Column(db.Integer)
    p06 = db.Column(db.Integer)
    p07 = db.Column(db.Integer)
    p08 = db.Column(db.Integer)
    p09 = db.Column(db.Integer)
    p10 = db.Column(db.Integer)
    p11 = db.Column(db.Integer)
    p12 = db.Column(db.Integer)
    p13 = db.Column(db.Integer)
    p14 = db.Column(db.Integer)
    p15 = db.Column(db.Integer)
    p16 = db.Column(db.Integer)
    p17 = db.Column(db.Integer)
    p18 = db.Column(db.Integer)
    p19 = db.Column(db.Integer)
    p20 = db.Column(db.Integer)
    p21 = db.Column(db.Integer)
    p22 = db.Column(db.Integer)
    p23 = db.Column(db.Integer)

    def init_from_dict(self, init_dic):
        for k in init_dic:
            self.__dict__[k] = init_dic[k]

    def get_array(self):
        cts_array = []
        pqc_array = []
        for i in range(24):
            s = "%02d" % i
            a = self.__dict__['a'+s]
            p = self.__dict__['p'+s]
            if a == None:
                cts_array.append(0)
            else:
                cts_array.append(int(a))
            if p == None:
                pqc_array.append(0)
            else:
                pqc_array.append(int(p))
        return cts_array, pqc_array

class AwsSource(db.Model):
    __tablename__ = 'aws_source'
    station_number = db.Column(db.String(6), primary_key=True)
    no_center = db.Column(db.Integer)


class RegCenterArrival(db.Model):
    __tablename__ = 'reg_center_arrival'
    data_day = db.Column(db.Date, primary_key=True)
    station_number = db.Column(db.String(6), primary_key=True)
    c00 = db.Column(db.Integer)
    c01 = db.Column(db.Integer)
    c02 = db.Column(db.Integer)
    c03 = db.Column(db.Integer)
    c04 = db.Column(db.Integer)
    c05 = db.Column(db.Integer)
    c06 = db.Column(db.Integer)
    c07 = db.Column(db.Integer)
    c08 = db.Column(db.Integer)
    c09 = db.Column(db.Integer)
    c10 = db.Column(db.Integer)
    c11 = db.Column(db.Integer)
    c12 = db.Column(db.Integer)
    c13 = db.Column(db.Integer)
    c14 = db.Column(db.Integer)
    c15 = db.Column(db.Integer)
    c16 = db.Column(db.Integer)
    c17 = db.Column(db.Integer)
    c18 = db.Column(db.Integer)
    c19 = db.Column(db.Integer)
    c20 = db.Column(db.Integer)
    c21 = db.Column(db.Integer)
    c22 = db.Column(db.Integer)
    c23 = db.Column(db.Integer)

    def init_from_dict(self, init_dic):
        for k in init_dic:
            self.__dict__[k] = init_dic[k]

    def get_array(self):
        reg_array = []
        for i in range(24):
            s = "%02d" % i
            c = self.__dict__['c'+s]
            if c == None:
                reg_array.append(0)
            else:
                reg_array.append(int(c))
        return reg_array


class AwsBattery(db.Model):
    __tablename__ = 'aws_battery'
    data_day = db.Column(db.Date, primary_key=True)
    station_number = db.Column(db.String(6), primary_key=True)
    b00 = db.Column(db.Float)
    b01 = db.Column(db.Float)
    b02 = db.Column(db.Float)
    b03 = db.Column(db.Float)
    b04 = db.Column(db.Float)
    b05 = db.Column(db.Float)
    b06 = db.Column(db.Float)
    b07 = db.Column(db.Float)
    b08 = db.Column(db.Float)
    b09 = db.Column(db.Float)
    b10 = db.Column(db.Float)
    b11 = db.Column(db.Float)
    b12 = db.Column(db.Float)
    b13 = db.Column(db.Float)
    b14 = db.Column(db.Float)
    b15 = db.Column(db.Float)
    b16 = db.Column(db.Float)
    b17 = db.Column(db.Float)
    b18 = db.Column(db.Float)
    b19 = db.Column(db.Float)
    b20 = db.Column(db.Float)
    b21 = db.Column(db.Float)
    b22 = db.Column(db.Float)
    b23 = db.Column(db.Float)


    def init_from_dict(self, init_dic):
        for k in init_dic:
            self.__dict__[k] = init_dic[k]

    def get_array(self):
        battery_array = []
        for i in range(24):
            s = "%02d" % i
            b = self.__dict__['b'+s]
            if b == None:
                battery_array.append(0)
            else:
                battery_array.append(int(b))
        return battery_array
