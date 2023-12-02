from flask import Flask, request, jsonify, make_response, render_template, redirect, url_for, session, flash
from views import views as views_blueprint
from models import db, Users
from flask_restful import Resource, Api
from flask_sqlalchemy import SQLAlchemy
import mysql.connector
from flask_login import LoginManager, UserMixin

# Create the application instance
app = Flask(__name__)

# Create the database instance
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:mysqlt3!Group@localhost/gamesdatabase'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialize flask with db
db.init_app(app)

login_manager = LoginManager(app)
login_manager.login_view = 'views.login'
login_manager.init_app(app)


@login_manager.user_loader
def load_user(id):
    return Users.query.get(int(id))


app.register_blueprint(views_blueprint, url_prefix='/')
app.secret_key = 'fdsagasggsdf gsdfdas'

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
        app.run(debug=True)
