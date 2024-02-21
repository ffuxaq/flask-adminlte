# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""

from app_cdc.flask_adminlte.apps.home import blueprint
from flask import render_template, request
from flask_login import login_required
from jinja2 import TemplateNotFound
import app_cdc.flask_adminlte.apps.home.render_home as rendHome


# @blueprint.route('/index')
# @login_required
# def index():
#     return render_template('home/index.html', segment='index')
@blueprint.route('/index')
@blueprint.route('/index.html')
@login_required
def index():
   okTemplate = True
   return rendHome.render_index1('index.html',segment='index.html')

okTemplate = False
# @blueprint.route('/index')
# @login_required
# def index():
#     return render_template('home/index.html', segment='index')
@blueprint.route('/index1')
@blueprint.route('/index1.html')
@login_required
def index1():
   okTemplate = True
   return rendHome.render_index1('index1.html',segment='index1.html')

# @blueprint.route('/index')
# @login_required
# def index():
#     return render_template('home/index.html', segment='index')
@blueprint.route('/index3')
@blueprint.route('/index3.html')
@login_required
def index3():
   okTemplate = True
   return render_template('home/index3.html',segment='index3.html')

@blueprint.route('/index4')
@blueprint.route('/index4.html')
@login_required
def index4():
   okTemplate = True
   return rendHome.render_index4('index4.html',segment='index4.html')

@blueprint.route('/<template>')
@login_required
def route_template(template:str):
    if (okTemplate):
        return ""
    try:

        if not template.endswith('.html'):
            template += '.html'

        # Detect the current page
        seg = get_segment(request)

        # Serve the file (if exists) from app/templates/home/FILE.html
        return render_template('home/' + template, segment=seg)

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
