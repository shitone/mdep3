#!/usr/bin/env python
# -*- coding: utf-8 -*-
import urllib, json, datetime
from . import cimiss
from flask_login import login_required, fresh_login_required
from flask import render_template
from ..ext import db
from ..models import AwsArrival, AwsSource, RegCenterArrival, AwsBattery
from sqlalchemy.sql import text


@cimiss.route('/awsarrival')
@fresh_login_required
def awsarrival():
    return render_template('awsarrival.html')


@cimiss.route('/awsarrivalc')
def awsarrivalc():
    return render_template('awsarrival_c.html', child_page=1)


@cimiss.route('/awsregsource')
@fresh_login_required
def awsregsource():
    return render_template('awsregsource.html')


@cimiss.route('/awsregsourcec')
def awsregsourcec():
    return render_template('awsregsource_c.html', child_page=1)


@cimiss.route('/regcenter')
@fresh_login_required
def regcenter():
    return render_template('regcenter.html')


@cimiss.route('/regcenterc')
def regcenterc():
    return render_template('regcenter_c.html', child_page=1)


@cimiss.route('/awsbattery')
@fresh_login_required
def awsbattery():
    return render_template('awsbattery.html')


@cimiss.route('/awsbatteryc')
def awsbatteryc():
    return render_template('awsbattery_c.html', child_page=1)


@cimiss.route('/awshistory')
@fresh_login_required
def awshistory():
    return render_template('awshistory.html')


@cimiss.route('/awshistoryc')
def awshistoryc():
    return render_template('awshistory_c.html', child_page=1)


@cimiss.route('/initaws', methods=['GET', 'POST'])
def initaws():
    now = datetime.datetime.utcnow()
    f = urllib.urlopen('http://10.116.32.88/stationinfo/index.php/Api/stationInfoLast?type=json')
    data = json.loads(f.read())
    filtersql = text("data_day=:data_day and " + "a" + now.strftime('%H') + "=1")
    arrivals = AwsArrival.query.filter(filtersql).params(data_day=now.date()).all()
    srecieves = []

    for arrival in arrivals:
        srecieve = {}
        if data.has_key(arrival.station_number):
            sinfo = data[arrival.station_number]
            srecieve["sno"] = sinfo["stationnum"]
            srecieve["sname"] = sinfo["stationname"]
            srecieve["areacode"] = sinfo["areacode"][0:4] + '00'
            srecieve["lon"] = sinfo["lontiude"]
            srecieve["lat"] = sinfo["lattiude"]
            srecieve["original"] = getattr(arrival, 'a'+ now.strftime('%H'))
            srecieve["pqc"] = getattr(arrival, 'p'+ now.strftime('%H'))
            srecieves.append(srecieve)
            del data[arrival.station_number]

    for key, sinfo in data.iteritems():
        srecieve = {}
        srecieve["sno"] = sinfo["stationnum"]
        srecieve["sname"] = sinfo["stationname"]
        srecieve["areacode"] = sinfo["areacode"][0:4] + '00'
        srecieve["lon"] = sinfo["lontiude"]
        srecieve["lat"] = sinfo["lattiude"]
        srecieve["original"] = 0
        srecieve["pqc"] = 0
        srecieves.append(srecieve)

    return json.dumps(srecieves)


@cimiss.route('/initawssource', methods=['GET', 'POST'])
def initawssource():
    f = urllib.urlopen('http://10.116.32.88/stationinfo/index.php/Api/stationInfoLast?type=json')
    data = json.loads(f.read())
    sources = AwsSource.query.all()
    awss = []

    for source in sources:
        aws = {}
        if data.has_key(source.station_number):
            sinfo = data[source.station_number]
            aws["sno"] = sinfo["stationnum"]
            aws["sname"] = sinfo["stationname"]
            aws["areacode"] = sinfo["areacode"][0:4] + '00'
            aws["lon"] = sinfo["lontiude"]
            aws["lat"] = sinfo["lattiude"]
            aws["machine"] = sinfo["machine"]
            aws["county"] = sinfo["county"]
            aws["nocenter"] = source.no_center
            awss.append(aws)

    return json.dumps(awss)


@cimiss.route('/initregcenter', methods=['GET', 'POST'])
def initregcenter():
    now = datetime.datetime.utcnow()
    f = urllib.urlopen('http://10.116.32.88/stationinfo/index.php/Api/stationInfoLast?type=json')
    data = json.loads(f.read())
    filtersql = text("data_day=:data_day and " + "a" + now.strftime('%H') + "=1")
    ctslist = []
    centerlist = []
    ctsarrivals = AwsArrival.query.filter(filtersql).params(data_day=now.date()).all()
    filtersql = text("data_day=:data_day and " + "c" + now.strftime('%H') + "=1")
    centerarrivals = RegCenterArrival.query.filter(filtersql).params(data_day=now.date()).all()
    for ca in ctsarrivals:
        ctslist.append(ca.station_number)
    for cta in centerarrivals:
        centerlist.append(cta.station_number)

    srecieves = []
    for key, sinfo in data.iteritems():
        srecieve = {}
        srecieve["sno"] = sinfo["stationnum"]
        srecieve["sname"] = sinfo["stationname"]
        srecieve["areacode"] = sinfo["areacode"][0:4] + '00'
        srecieve["lon"] = sinfo["lontiude"]
        srecieve["lat"] = sinfo["lattiude"]
        srecieve["cts_arrival"] = 0
        srecieve["center_arrival"] = 0
        if sinfo["stationnum"] in ctslist:
            srecieve["cts_arrival"] = 1
        if sinfo["stationnum"] in centerlist:
            srecieve["center_arrival"] = 1
        srecieves.append(srecieve)

    return json.dumps(srecieves)


@cimiss.route('/initawsbattery', methods=['GET', 'POST'])
def initawsbattery():
    now = datetime.datetime.utcnow()
    f = urllib.urlopen('http://10.116.32.88/stationinfo/index.php/Api/stationInfoLast?type=json')
    data = json.loads(f.read())
    filtersql = text("data_day=:data_day")
    batterys = AwsBattery.query.filter(filtersql).params(data_day=now.date()).all()
    srecieves = []

    for battery in batterys:
        srecieve = {}
        if data.has_key(battery.station_number):
            sinfo = data[battery.station_number]
            srecieve["sno"] = sinfo["stationnum"]
            srecieve["sname"] = sinfo["stationname"]
            srecieve["areacode"] = sinfo["areacode"][0:4] + '00'
            srecieve["lon"] = sinfo["lontiude"]
            srecieve["lat"] = sinfo["lattiude"]
            srecieve["machine"] = sinfo["machine"]
            srecieve["county"] = sinfo["county"]
            battery_value = getattr(battery, 'b'+ now.strftime('%H'))
            if battery_value==None:
                srecieve["battery_value"] = -1
            else:
                srecieve["battery_value"] = battery_value
            srecieves.append(srecieve)
            del data[battery.station_number]

    for key, sinfo in data.iteritems():
        srecieve = {}
        srecieve["sno"] = sinfo["stationnum"]
        srecieve["sname"] = sinfo["stationname"]
        srecieve["areacode"] = sinfo["areacode"][0:4] + '00'
        srecieve["lon"] = sinfo["lontiude"]
        srecieve["lat"] = sinfo["lattiude"]
        srecieve["machine"] = sinfo["machine"]
        srecieve["county"] = sinfo["county"]
        srecieve["battery_value"] = -1
        srecieves.append(srecieve)

    return json.dumps(srecieves)


@cimiss.route('/getawshistory/<daystr>', methods=['GET', 'POST'])
def getawshistory(daystr):
    now = datetime.datetime.strptime(daystr, '%Y-%m-%d')
    f = urllib.urlopen('http://10.116.32.88/stationinfo/index.php/Api/stationInfoLast?type=json')
    data = json.loads(f.read())
    filtersql = text("data_day=:data_day")
    arrivals = AwsArrival.query.filter(filtersql).params(data_day=now.date()).all()
    centerarrivals = RegCenterArrival.query.filter(filtersql).params(data_day=now.date()).all()
    batterys = AwsBattery.query.filter(filtersql).params(data_day=now.date()).all()
    historys = {}

    for key, sinfo in data.iteritems():
        cts_array = [0 for i in range(24)]
        pqc_array = [0 for i in range(24)]
        reg_array = [0 for i in range(24)]
        battery_array = [0 for i in range(24)]
        station_num = sinfo["stationnum"]
        station_info_dict = {}
        station_info_dict["sname"] =  sinfo["stationname"]
        station_info_dict["machine"] =  sinfo["machine"]
        station_info_dict["area"] =  sinfo["area"]
        station_info_dict["county"] =  sinfo["county"]
        station_info_dict["cts"] = cts_array
        station_info_dict["pqc"] = pqc_array
        station_info_dict["reg"] = reg_array
        station_info_dict["battery"] = battery_array
        historys[station_num] = station_info_dict

    for arrival in arrivals:
        sno = arrival.station_number
        if sno in data:
            historys[sno]["cts"] = arrival.get_array()[0]
            historys[sno]["pqc"] = arrival.get_array()[1]

    for center in centerarrivals:
        sno = center.station_number
        if sno in data:
            historys[sno]["reg"] = center.get_array()

    for battery in batterys:
        sno = battery.station_number
        if sno in data:
            historys[sno]["battery"] = battery.get_array()

    return json.dumps(historys)