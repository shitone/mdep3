#!/usr/bin/env python
# -*- coding: utf-8 -*-
from ..ext import socketio
from ..models import AwsArrival
from flask_socketio import emit
import urllib, json, time, datetime
from .. import db
import flask


@socketio.on('aws', namespace='/awspqc')
def test_message(message):
    a = dict()
    a['data_day']=datetime.datetime.utcnow().date()
    a['station_number']='J0003'
    a['a01']=1
    awsarrival = AwsArrival()
    awsarrival.init_from_dict(a)
    db.session.merge(awsarrival)
    db.session.commit()



@socketio.on('aws1', namespace='/awspqc')
def test_message(message):
    awsarrival = AwsArrival(data_day=datetime.datetime.utcnow().date(), station_number='J0003', a01=0)
    db.session.merge(awsarrival)
    db.session.merge_all()
    db.session.commit()


# def add():
#     while(True):
#         socketio.emit('mytask', {'data': 'yourtask'}, namespace='/awspqc')
#         time.sleep(5)