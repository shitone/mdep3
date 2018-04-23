#!/usr/bin/env python
# -*- coding: utf-8 -*-
from . import socketio
from flask_socketio import emit
import urllib, json


@socketio.on('message', namespace='/test')
def handle_message(message):
    print ('received message: ' + message)
    emit('this')


@socketio.on('my_event', namespace='/test')
def test_message(message):
    print('re message: ' + str(message))
    emit('my_song')
