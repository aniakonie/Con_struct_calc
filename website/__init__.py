from flask import Flask, send_file
from flask_sqlalchemy import SQLAlchemy
from os import path
from flask_login import LoginManager

db = SQLAlchemy()
DB_NAME = "database.db"



def create_app():
	app = Flask(__name__)
	#initializing flask, "__name__" refers to the name of the current file, 
	#this line tells Python 'turn this file into a Flask application'

	
	app.config['SECRET_KEY'] = 'ferfrfedf' 
	app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{DB_NAME}'
	db.init_app(app)


	from .views import views
	from .auth import auth
	from .views_zakotwienie import views_zakotwienie
	from .views_belka_zelbetowa import views_belka_zelbetowa


	app.register_blueprint(views, url_prefix='/')
	app.register_blueprint(auth, url_prefix='/')
	app.register_blueprint(views_zakotwienie, url_prefix='/')
	app.register_blueprint(views_belka_zelbetowa, url_prefix='/')


	from .models import User, Note

	with app.app_context():
		db.create_all()


	login_manager = LoginManager()
	login_manager.login_view = 'auth.login'
	login_manager.init_app(app)

	@login_manager.user_loader
	def load_user(id):
		return User.query.get(int(id))
		
	return app



		



