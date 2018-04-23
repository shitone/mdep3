#!/usr/bin/env python
# -*- coding: utf-8 -*-

import urllib2, sqlite3
from urllib2 import HTTPError, URLError
from apscheduler.schedulers.background import BackgroundScheduler
import urllib, json

# scheduler = BackgroundScheduler(daemon = False)
# scheduler.start()
#
#
# @scheduler.scheduled_job('cron', id='my_job_id', year='*', month='*', day='*', week='*', day_of_week='*', hour='*', minute=28, second=0)
# def job_function():
#     print "Hello World!"
#
#
# def httpdownload(url, savepath):
#     urllib2.socket.setdefaulttimeout(30)
#     out = False
#     try:
#         f = urllib2.urlopen(url)
#         out = open(savepath, 'wb')
#         while True:
#             data = f.read(1024*64)
#             if len(data) == 0:
#                 break
#             out.write(data)
#         print "Succeed."
#     except HTTPError:
#         print 'The Server could not fulfill the request.'
#     except URLError:
#         print 'Failed to reach the server.'
#     except IOError:
#         print 'The Disk is Wrong.'
#     except Exception:
#         print 'Unkown Error.'
#     finally:
#         if out:
#             out.close()

#{"stationname":"\u9646\u574a","stationnum":"J6318","lontiude":"116.8278","lattiude":"28.0061","height":"85.0","area":"\u629a\u5dde\u5e02","county":"\u91d1\u6eaa\u53bf","stationtype":"\u533a\u57df\u7ad9","ischeck":"1","r":"1","t":"1","w":"-1","h":"-1","p":"-1","userop":"\u6dfb\u52a0","status":"\u901a\u8fc7"}
def test():
    f = urllib.urlopen('http://10.116.32.88/stationinfo/index.php/Api/stationInfoLast?type=json')
    data = json.loads(f.read())
    srecieves = []
    for sinfo in data:
        srecieve = {}
        srecieve["sno"] = sinfo["stationnum"]
        srecieve["sname"] = sinfo["stationname"]
        srecieve["lon"] = sinfo["lontiude"]
        srecieve["lat"] = sinfo["lattiude"]
        srecieve["original"] = 1;
        srecieve["pqc"] = 1;
        srecieves.append(srecieve)

if __name__ == '__main__':
#     conn = sqlite3.connect('readline.db')
#     conn.close()
#     # url = "http://nomads.ncep.noaa.gov/pub/data/nccf/com/cfs/prod/cfs/cfs.20160624/00/6hrly_grib_01/flxf2016062400.01.2016062400.grb2"
#     # savepath = "a:\\flxf2016062400.01.2016062400.grb2"
#     #httpdownload(url, savepath)
    test()

#!/usr/bin/env python
# from flask import Flask, render_template, session, request
# from flask_socketio import SocketIO, emit, join_room, leave_room, \
#     close_room, rooms, disconnect
#
# # Set this variable to "threading", "eventlet" or "gevent" to test the
# # different async modes, or leave it set to None for the application to choose
# # the best option based on installed packages.
# async_mode = None
#
# app = Flask(__name__)
# app.config['SECRET_KEY'] = 'secret!'
# socketio = SocketIO(app, async_mode=async_mode)
# thread = None
#
#
# def background_thread():
#     """Example of how to send server generated events to clients."""
#     count = 0
#     while True:
#         socketio.sleep(10)
#         count += 1
#         socketio.emit('my_response',
#                       {'data': 'Server generated event', 'count': count},
#                       namespace='/test')
#
#
# @app.route('/')
# def index():
#     return render_template('index1.html', async_mode=socketio.async_mode)
#
#
# @socketio.on('my_event', namespace='/test')
# def test_message(message):
#     session['receive_count'] = session.get('receive_count', 0) + 1
#     emit('my_response',
#          {'data': message['data'], 'count': session['receive_count']})
#
#
# @socketio.on('my_broadcast_event', namespace='/test')
# def test_broadcast_message(message):
#     session['receive_count'] = session.get('receive_count', 0) + 1
#     emit('my_response',
#          {'data': message['data'], 'count': session['receive_count']},
#          broadcast=True)
#
#
# @socketio.on('join', namespace='/test')
# def join(message):
#     join_room(message['room'])
#     session['receive_count'] = session.get('receive_count', 0) + 1
#     emit('my_response',
#          {'data': 'In rooms: ' + ', '.join(rooms()),
#           'count': session['receive_count']})
#
#
# @socketio.on('leave', namespace='/test')
# def leave(message):
#     leave_room(message['room'])
#     session['receive_count'] = session.get('receive_count', 0) + 1
#     emit('my_response',
#          {'data': 'In rooms: ' + ', '.join(rooms()),
#           'count': session['receive_count']})
#
#
# @socketio.on('close_room', namespace='/test')
# def close(message):
#     session['receive_count'] = session.get('receive_count', 0) + 1
#     emit('my_response', {'data': 'Room ' + message['room'] + ' is closing.',
#                          'count': session['receive_count']},
#          room=message['room'])
#     close_room(message['room'])
#
#
# @socketio.on('my_room_event', namespace='/test')
# def send_room_message(message):
#     session['receive_count'] = session.get('receive_count', 0) + 1
#     emit('my_response',
#          {'data': message['data'], 'count': session['receive_count']},
#          room=message['room'])
#
#
# @socketio.on('disconnect_request', namespace='/test')
# def disconnect_request():
#     session['receive_count'] = session.get('receive_count', 0) + 1
#     emit('my_response',
#          {'data': 'Disconnected!', 'count': session['receive_count']})
#     disconnect()
#
#
# @socketio.on('my_ping', namespace='/test')
# def ping_pong():
#     emit('my_pong')
#
#
# @socketio.on('connect', namespace='/test')
# def test_connect():
#     global thread
#     if thread is None:
#         thread = socketio.start_background_task(target=background_thread)
#     emit('my_response', {'data': 'Connected', 'count': 0})
#
#
# @socketio.on('disconnect', namespace='/test')
# def test_disconnect():
#     print('Client disconnected', request.sid)
#
#
# if __name__ == '__main__':
#     socketio.run(app, debug=True)


