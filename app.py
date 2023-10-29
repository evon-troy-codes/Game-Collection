from flask import Flask, request, jsonify, make_response, render_template, redirect, url_for, session, flash
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


# HTML routing
app.secret_key = 'testing_key'


@app.route("/")
def home():
    # return render_template("index.html")
    return redirect(url_for("user"))


@app.route("/login/", methods = ["POST", "GET"])
def login():
    if request.method == "POST":
        user = request.form["em"]
        # temp_pw = request.form["pw"]
        session["user"] = user
        return redirect(url_for("user"))
    else:
        if "user" in session:
            return redirect(url_for("user"))
        return render_template("login.html")


# for now to make sure POST is working in the login page
@app.route("/profile/")
def user():
    if "user" in session:
        user = session["user"]
        # return f"<h1>{user}</h1>"
        return render_template("profile.html", user=user)
    else:
        return redirect(url_for("login"))

@app.route("/logout/")
def logout():
    if "user" in session:
        user = session["user"]
        flash(f"{user} Logged out successfully")
    session.pop("user", None)
    return redirect(url_for("login"))

@app.route("/games/")
def games():
    return render_template("games.html")

@app.route("/collection/")
def collection():
    if "user" in session:
        user = session["user"]
        # return f"<h1>{user}</h1>"
        return render_template("collection.html", user=user)
    else:
        return redirect(url_for("login"))


if __name__ == "__main__":
    app.run(debug=True)
