#!/usr/bin/env python

''' flask module to create app for PyQ Decay interface. This module
then will import more configuration from auth and views module.'''

import os

from flask import Flask


path = os.getcwd()
UPLOAD_FOLDER = os.path.join(path, 'uploads')
WEB_FOLDER = os.path.join(path, 'website')
STATIC_FOLDER = os.path.join(WEB_FOLDER, 'static')
if not os.path.isdir(UPLOAD_FOLDER):
	os.mkdir(UPLOAD_FOLDER)

def create_app():
	app = Flask(__name__)
	app.config['SECRET KEY'] = 'xbahaxuahsbxaysx sabjhsxbajshax'
	app.secret_key = 'xbahaxuahsbxaysx sabjhsxbajshax'
	app.config['MAX_CONTENT_LENGHT'] = 100 * 1024 * 1024

	global UPLOAD_FOLDER
	app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
	#ALLOWED_EXTENSIONS = set(['txt','csv','xls','jpg','jpeg','png'])


	from .views import views
	from .auth import auth


	app.register_blueprint(views, url_prefix='/')
	app.register_blueprint(auth, url_prefix='/')

	return app

