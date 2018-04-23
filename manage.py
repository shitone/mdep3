#!/usr/bin/env python
# -*- coding: utf-8 -*-

import eventlet
eventlet.monkey_patch()


from webapp import socketio, create_app


app = create_app()


if __name__ == '__main__':
    socketio.run(app, host='0.0.0.0')