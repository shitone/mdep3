#!/usr/bin/env python
# -*- coding: utf-8 -*-
from . import page2
from flask_login import login_required
from flask import render_template


@page2.route('/node1')
@login_required
def page21():
    return render_template('test2.html')


@page2.route('/node2')
@login_required
def page22():
    return render_template('test2.html')