from extensions import db
from flask_login import UserMixin


class User(db.Model, UserMixin):
    __tablename__ = 'users'
    user_id = db.Column(db.Integer, primary_key=True)
    password = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(75), nullable=False)
    dob = db.Column(db.Date, nullable=True)
    first_name = db.Column(db.String(40))
    last_name = db.Column(db.String(40))
    game_collections = db.relationship('GameCollection', backref='user', lazy=True)

    def get_id(self):
        return str(self.user_id)


class GameCollection(db.Model):
    __tablename__ = 'gamecollection'
    collection_id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'))
    items = db.relationship('GameCollectionItems', backref='gamecollection', lazy=True)


class GameCollectionItems(db.Model):
    __tablename__ = 'gamecollectionitems'
    collection_items_id = db.Column(db.Integer, primary_key=True)
    game_collection_id = db.Column(db.Integer, db.ForeignKey('gamecollection.collection_id'))
    game_id = db.Column(db.Integer, db.ForeignKey('games.game_id'))
    status = db.Column(db.String(20))
    UserRating = db.Column(db.Integer)
    favorite_games = db.Column(db.Boolean)
    total_play_time = db.Column(db.Integer)


class Games(db.Model):
    __tablename__ = 'games'
    game_id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100))
    description = db.Column(db.Text)
    genre = db.Column(db.String(100))
    MetaCriticRating = db.Column(db.Integer)
    esrb = db.Column(db.String(5))
    developer = db.Column(db.String(100))
    release_date = db.Column(db.Date)
    AverageRating = db.Column(db.Numeric(3, 2))
