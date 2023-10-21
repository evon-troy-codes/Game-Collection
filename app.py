from flask import Flask, request, jsonify, make_response
from flask_restful import Resource, Api
from flask_sqlalchemy import SQLAlchemy

# Create the application instance
app = Flask(__name__)

# Create the API
api = Api(app)

# Create the database instance
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

#sqlalchemy instance
db = SQLAlchemy(app)

# Create the database model
