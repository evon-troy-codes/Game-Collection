from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash

db = SQLAlchemy()

class Game(db.Model):
    __tablename__ = 'games'
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
    __tablename__ = 'users'
    user_id = db.Column(db.Integer, primary_key=True)
    password = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(75), nullable=False)
    dob = db.Column(db.Date)
    first_name = db.Column(db.String(40))
    last_name = db.Column(db.String(40))
    game_collections = db.relationship('GameCollection', backref='user', lazy=True)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)


class GameCollection(db.Model):
    __tablename__ = 'gamecollection'
    collection_id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.user_id'))
    items = db.relationship('GameCollectionItems', backref='gamecollection', lazy=True)


class GameCollectionItems(db.Model):
    __tablename__ = 'gamecollectionitems'
    collection_items_id = db.Column(db.Integer, primary_key=True)
    game_collection_id = db.Column(db.Integer, db.ForeignKey('gamecollection.collection_id'))
    game_id = db.Column(db.Integer, db.ForeignKey('game.game_id'))
    status = db.Column(db.String(20))
    UserRating = db.Column(db.Integer)
    favorite_games = db.Column(db.Boolean)
    total_play_time = db.Column(db.Integer)
