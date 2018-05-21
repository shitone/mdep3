#!/usr/bin/env python
# -*- coding: utf-8 -*-

from ..ext import socketio, db
import urllib, json, string, datetime, copy
from kombu import Connection, Queue
from ..models import AwsArrival, AwsSource, RegCenterArrival, AwsBattery
from config import Basic
from sqlalchemy.sql import text
import re


def listen_awspqc():
    awspqc_queue = Queue('awspqc')

    def _process_aws(body, message):
        message.ack()
        f = urllib.urlopen('http://10.116.32.88/stationinfo/index.php/Api/stationInfoLast?type=json')
        data = json.loads(f.read())
        timestamp=body['timestamp']
        aws=body['aws']
        inter=body['inter']
        nocenter = body['nocenter']
        intercenter = body['intercenter']
        srecieves = []
        for key, sinfo in data.iteritems():
            srecieve = {}
            srecieve["sno"] = sinfo["stationnum"]
            srecieve["areacode"] = sinfo["areacode"][0:4] + '00'
            srecieve["sname"] = sinfo["stationname"]
            srecieve["lon"] = sinfo["lontiude"]
            srecieve["lat"] = sinfo["lattiude"]
            srecieve["original"] = 0
            srecieve["county"] = sinfo["county"]
            srecieve["machine"] = sinfo["machine"]
            srecieve["pqc"] = 0
            if sinfo["stationnum"] in aws:
                srecieve["original"] = 1
                if sinfo["stationnum"] not in inter:
                    srecieve["pqc"] = 1
            if sinfo["stationnum"] in nocenter:
                srecieve["nocenter"] = 1
            elif sinfo["stationnum"] in intercenter:
                srecieve["nocenter"] = 3
            elif srecieve["original"] == 1:
                srecieve["nocenter"] = 0
            else:
                srecieve["nocenter"] = 2
            srecieves.append(srecieve)
        socketio.emit('aws_info',json.dumps(srecieves), namespace='/awspqc')

    with Connection(Basic.TASK_RMQ + '/cimiss') as conn:
        with conn.Consumer(awspqc_queue, accept=['json'], callbacks=[_process_aws]) as consumer:
            while True:
                try:
                    conn.drain_events()
                except Exception, e:
                    print e.message


def listen_awspqc_record():
    record_queue = Queue('awspqc_record')

    def _record_aws(body, message):
        message.ack()
        with db.app.app_context():
            timestamp = string.atof(body['timestamp'])
            now = datetime.datetime.utcfromtimestamp(timestamp)
            aws = body['aws']
            inter = body['inter']
            nocenter = body['nocenter']
            intercenter = body['intercenter']
            for aw in aws:
                init_dict = dict()
                init_dict['data_day'] = now.date()
                init_dict['station_number'] = aw
                init_dict['a'+ now.strftime('%H')] = 1
                if aw not in inter:
                    init_dict['p'+ now.strftime('%H')] = 1
                awsarrival = AwsArrival()
                awsarrival.init_from_dict(init_dict)
                db.session.merge(awsarrival)
            db.session.commit()

            f = urllib.urlopen('http://10.116.32.88/stationinfo/index.php/Api/stationInfoLast?type=json')
            data = json.loads(f.read())
            ass = AwsSource.query.all()
            for a in ass:
                if data.has_key(a.station_number):
                    if a.station_number in nocenter:
                        a.no_center = 1
                    elif a.station_number in intercenter:
                        a.no_center = 3
                    elif a.station_number not in aws:
                        a.no_center = 2
                    else:
                        a.no_center = 0
                    db.session.add(a)
                    del data[a.station_number]
                else:
                    db.session.delete(a)
            for key, sinfo in data.iteritems():
                no = 0
                if sinfo["stationnum"] in nocenter:
                    no = 1
                a = AwsSource(station_number=sinfo["stationnum"], no_center=no)
                db.session.add(a)
            db.session.commit()

    with Connection(Basic.TASK_RMQ + '/cimiss') as conn:
        with conn.Consumer(record_queue, accept=['json'], callbacks=[_record_aws]) as consumer:
            while True:
                try:
                    conn.drain_events()
                except Exception, e:
                    print e.message


def listen_regcenter():
    regaws_queue = Queue('regaws')

    def _process_regaws(body, message):
        message.ack()
        with db.app.app_context():
            f = urllib.urlopen('http://10.116.32.88/stationinfo/index.php/Api/stationInfoLast?type=json')
            data = json.loads(f.read())
            timestamp = string.atof(body['timestamp'])
            now = datetime.datetime.utcfromtimestamp(timestamp)
            carrival = body['isarr']
            battery = body['battery']
            sqlstr = text("data_day=:data_day and " + "a" + now.strftime('%H') + "=1")
            aas = AwsArrival.query.filter(sqlstr).params(data_day=now.date()).all()
            aanolist = []
            for aa in aas:
                aanolist.append(aa.station_number)
            srecieves = []
            btrs = []
            for key, sinfo in data.iteritems():
                srecieve = {}
                srecieve["sno"] = sinfo["stationnum"]
                srecieve["areacode"] = sinfo["areacode"][0:4] + '00'
                srecieve["sname"] = sinfo["stationname"]
                srecieve["lon"] = sinfo["lontiude"]
                srecieve["lat"] = sinfo["lattiude"]
                srecieve["county"] = sinfo["county"]
                srecieve["machine"] = sinfo["machine"]
                btr = copy.deepcopy(srecieve)
                srecieve["center_arrival"] = 0
                srecieve["cts_arrival"] = 0
                if sinfo["stationnum"] in carrival:
                    srecieve["center_arrival"] = 1
                if sinfo["stationnum"] in aanolist:
                    srecieve["cts_arrival"] = 1
                srecieves.append(srecieve)
                if sinfo["stationnum"] in battery:
                    btr["battery_value"] = battery[sinfo["stationnum"]]
                else:
                    battery["battery_value"] = -1
                btrs.append(btr)
            socketio.emit('reg_center',json.dumps(srecieves), namespace='/awspqc')
            socketio.emit('aws_battery', json.dumps(btrs), namespace='/awspqc')

    with Connection(Basic.TASK_RMQ + '/cimiss') as conn:
        with conn.Consumer(regaws_queue, accept=['json'], callbacks=[_process_regaws]) as consumer:
            while True:
                try:
                    conn.drain_events()
                except Exception, e:
                    print e.message


def listen_regcenter_record():
    record_queue = Queue('regaws_record')

    def _record_regaws(body, message):
        message.ack()
        with db.app.app_context():
            timestamp = string.atof(body['timestamp'])
            now = datetime.datetime.utcfromtimestamp(timestamp)
            carrivals = body['isarr']
            batterys = body['battery']
            for ca in carrivals:
                init_dict = dict()
                init_dict['data_day'] = now.date()
                init_dict['station_number'] = ca
                init_dict['c'+ now.strftime('%H')] = 1
                rcarrival = RegCenterArrival()
                rcarrival.init_from_dict(init_dict)
                db.session.merge(rcarrival)
            db.session.commit()
            for btr in batterys:
                init_dict = dict()
                init_dict['data_day'] = now.date()
                init_dict['station_number'] = btr
                if (batterys[btr] is None) or (not re.match(r'-?\d+(\.\d+)?', batterys[btr])):
                    init_dict['b'+ now.strftime('%H')] = -1.0
                else:
                    init_dict['b'+ now.strftime('%H')] = float(batterys[btr])
                abattery = AwsBattery()
                abattery.init_from_dict(init_dict)
                db.session.merge(abattery)
            db.session.commit()

    with Connection(Basic.TASK_RMQ + '/cimiss') as conn:
        with conn.Consumer(record_queue, accept=['json'], callbacks=[_record_regaws]) as consumer:
            while True:
                try:
                    conn.drain_events()
                except Exception, e:
                    print e.message
