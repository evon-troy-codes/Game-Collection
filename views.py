from flask import Blueprint, request, render_template, redirect, url_for, session, flash

views = Blueprint(__name__,"views")


@views.route("/")
def home():
    # return render_template("index.html")
    return redirect(url_for("views.user"))


@views.route("/login/", methods = ["POST", "GET"])
def login():
    if request.method == "POST":
        user = request.form["em"]
        # temp_pw = request.form["pw"]
        session["user"] = user
        return redirect(url_for("views.user"))
    else:
        if "user" in session:
            return redirect(url_for("views.user"))
        return render_template("login.html")


# for now to make sure POST is working in the login page
@views.route("/profile/")
def user():
    if "user" in session:
        user = session["user"]
        # return f"<h1>{user}</h1>"
        return render_template("profile.html", user=user)
    else:
        return redirect(url_for("views.login"))

@views.route("/logout/")
def logout():
    if "user" in session:
        user = session["user"]
        flash(f"{user} Logged out successfully")
    session.pop("user", None)
    return redirect(url_for("views.login"))

@views.route("/games/")
def games():
    return render_template("games.html")

@views.route("/collection/")
def collection():
    if "user" in session:
        user = session["user"]
        # return f"<h1>{user}</h1>"
        return render_template("collection.html", user=user)
    else:
        return redirect(url_for("views.login"))