from flask import Flask, request, jsonify, make_response, render_template, redirect, url_for, session, flash
from views import views as views_blueprint
from flask_restful import Resource, Api
from flask_sqlalchemy import SQLAlchemy
import mysql.connector
from flask_login import LoginManager, UserMixin

# Create the application instance
app = Flask(__name__)

# Create the database instance
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:ealexan2@localhost/gamesdatabase'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialize flask with db
db = SQLAlchemy(app)


class Game(db.Model):
    __tablename__ = 'game'
    game_id = db.Column(db.Integer, primary_key=True)
    genre = db.Column(db.String(100))
    MetacriticRating = db.Column(db.Integer)
    esrb = db.Column(db.String(5))
    title = db.Column(db.String(100))
    description = db.Column(db.Text)
    developer = db.Column(db.String(100))
    release_date = db.Column(db.Date)
    AverageRating = db.Column(db.Float(precision=2))


class User(db.Model, UserMixin):
    __tablename__ = 'user'
    user_id = db.Column(db.Integer, primary_key=True)
    password = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(75), nullable=False)
    dob = db.Column(db.Date)
    first_name = db.Column(db.String(40))
    last_name = db.Column(db.String(40))


class GameCollection(db.Model):
    __tablename__ = 'gamecollection'
    collection_id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.user_id'))


class GameCollectionItems(db.Model):
    __tablename__ = 'gamecollectionitems'
    collection_items_id = db.Column(db.Integer, primary_key=True)
    game_collection_id = db.Column(db.Integer, db.ForeignKey('gamecollection.collection_id'))
    game_id = db.Column(db.Integer, db.ForeignKey('game.game_id'))
    status = db.Column(db.String(20))
    UserRating = db.Column(db.Integer)
    favorite_games = db.Column(db.Boolean)
    total_play_time = db.Column(db.Integer)


login_manager = LoginManager(app)
login_manager.login_view = 'views.login'
# login_manager.init_app(app)

@login_manager.user_loader
def load_user(id):
    return User.query.get(int(id))

app.register_blueprint(views_blueprint, url_prefix='/')
app.secret_key = 'fdsagasggsdf gsdfdas'

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
        app.run(debug=True)
