from flask import Flask, request, jsonify, make_response
from flask_restful import Resource, Api
from flask_sqlalchemy import SQLAlchemy

# Create the application instance
app = Flask(__name__)

# Create the API
api = Api(app)

# Create the database instance
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://yourusername:yourpassword@localhost/gamesdatabase'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# sqlalchemy instance
db = SQLAlchemy(app)

# Create the database model
class User(db.Model):
    UserID = db.Column(db.Integer, primary_key=True)
    Password = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(75), nullable=False)
    DOB = db.Column(db.Date, default=None)

class Game(db.Model):
    GameID = db.Column(db.Integer, primary_key=True)
    Genre = db.Column(db.String(100))
    MetacriticRating = db.Column(db.Integer)
    ESRB = db.Column(db.String(5))
    Title = db.Column(db.String(100))
    Description = db.Column(db.Text)
    Developer = db.Column(db.String(100))
    ReleaseDate = db.Column(db.Date)
    AverageRating = db.Column(db.Float(precision=2))