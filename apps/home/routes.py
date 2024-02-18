# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""

from app.flask_adminlte.apps.home import blueprint
from flask import render_template, request
from flask_login import login_required
from jinja2 import TemplateNotFound
import app.flask_adminlte.apps.home.render_home as rendHome


# @blueprint.route('/index')
# @login_required
# def index():
#     return render_template('home/index.html', segment='index')
@blueprint.route('/index')
@login_required
def index():
   return rendHome.render('home/index.html',segment='index.html')

@blueprint.route('/<template>')
@login_required
def route_template(template):

    try:

        if not template.endswith('.html'):
            template += '.html'

        # Detect the current page
        seg = get_segment(request)

        # Serve the file (if exists) from app/templates/home/FILE.html
        return rendHome.render(template, segment=seg)

    except TemplateNotFound:
        return render_template('home/page-404.html'), 404

    except:
        return render_template('home/page-500.html'), 500


# Helper - Extract current page name from request
def get_segment(request):

    try:

        segment = request.path.split('/')[-1]

        if segment == '':
            segment = 'index'

        return segment

    except:
        return None
