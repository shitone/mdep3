#!/usr/bin/env python
# -*- coding: utf-8 -*-


class TaskConifg(object):
    JOBS = [
        {
            'id': 'listenAwsPQC',
            'func': 'webapp.tasks.rabbit:listen_awspqc',
            'trigger': 'date'
        },
        {
            'id': 'recordAwsPQC',
            'func': 'webapp.tasks.rabbit:listen_awspqc_record',
            'trigger': 'date'
        },
        {
            'id': 'awsRegAlarm',
            'func': 'webapp.tasks.notice:aws_reg_alarm',
            'trigger': 'cron',
            'second': '*/5'
        },
        {
            'id': 'listenRegCenter',
            'func': 'webapp.tasks.rabbit:listen_regcenter',
            'trigger': 'date'
        },
        {
            'id': 'recordRegCenter',
            'func': 'webapp.tasks.rabbit:listen_regcenter_record',
            'trigger': 'date'
        }
    ]
    SCHEDULER_API_ENABLED = True