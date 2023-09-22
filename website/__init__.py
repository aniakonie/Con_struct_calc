from flask import Flask, send_file
from os import path


def create_app():
	app = Flask(__name__)

	from .views import views
	from .views_RC_beam_design import views_RC_beam_design

	app.register_blueprint(views, url_prefix='/')
	app.register_blueprint(views_RC_beam_design, url_prefix='/')
		
	return app



		



