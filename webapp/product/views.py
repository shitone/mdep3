#!/usr/bin/env python
# -*- coding: utf-8 -*-
from . import product
from flask_login import login_required, fresh_login_required
from flask import render_template


@product.route('/surface/tmp')
@fresh_login_required
def tmp():
    return render_template('tmp.html')


@product.route('/surface/tmpc')
def tmpc():
    return render_template('tmp_c.html', child_page=1)


@product.route('/surface/wind')
@fresh_login_required
def wind():
    return render_template('wind.html')


@product.route('/surface/tmpc')
def windc():
    return render_template('wind_c.html', child_page=1)