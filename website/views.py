from flask import Blueprint, render_template

views = Blueprint('views', __name__)

@views.route('/')
def home():
	return render_template('home.html')

@views.route('/about-us')
def about_us():
	return render_template('about_us.html')
