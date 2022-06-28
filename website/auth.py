#!/usr/bin/env python

''' The auth module of flask for PyQ Deacy user interface.'''

import os

from flask import (
	Blueprint,
	render_template,
	request,
	redirect,
	flash,
	send_file,
	url_for
	)
from werkzeug.utils import secure_filename
from . import UPLOAD_FOLDER, STATIC_FOLDER
from .module import main



auth = Blueprint('auth', __name__)

@auth.route('/eq-decay/input-data', methods=['GET','POST'])
def input_data():
	#UPLOAD TO SERVER#
	if request.method == 'POST':
		freq = int(request.form.get('freq'))
		file = request.files['file']
		if file :
			filename = secure_filename(file.filename)
			file.save(os.path.join(UPLOAD_FOLDER,filename))
			fname = os.path.join(UPLOAD_FOLDER,filename)
			image_list = main(
				filename=fname,
				frequency=freq,
				save_folder=STATIC_FOLDER
				)

			flash('File Uploaded!', category='success')
			return render_template('output.html',imagelist=image_list)

	return render_template('input_data.html')