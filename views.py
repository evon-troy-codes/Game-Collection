from flask import Blueprint, request, render_template, redirect, url_for, session, flash
from models import db, Users
from flask_login import login_user, login_required, logout_user, current_user

views = Blueprint(__name__, 'views')


@views.route('/')
def home():
    return redirect(url_for('views.games'))


@views.route('/login/', methods=['POST', 'GET'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')

        user = Users.query.filter_by(email=email).first()
        if user:
            if user and user.password == password:
                flash('Logged in successfully.')
                login_user(user, remember=True)
                return redirect(url_for('views.profile'))
            else:
                flash('Incorrect password, try again.')
        else:
            flash('Email does not exist.', category='error')

    return render_template('login.html', user=current_user)


# for now to make sure POST is working in the login page
@views.route('/profile/')
@login_required
def profile():
        email = current_user.email
        password = current_user.password
        first_name = current_user.first_name
        last_name = current_user.last_name
        return render_template('profile.html', user=current_user.first_name)

@views.route('/sign-up/', methods=['POST', 'GET'])
def sign_up():
    if current_user.is_authenticated:
        flash('You are already logged in. ')
        return redirect(url_for('views.profile'))

    if request.method== 'POST':
        email = request.form.get('email')
        first_name = request.form.get('first_name')
        last_name = request.form.get('last_name')
        password1 = request.form.get('password1')
        password2 = request.form.get('password2')
        dob = request.form.get('dob')


        user = Users.query.filter_by(email=email).first()

        # category will be used when bootstrap is added.
        if user:
            flash('Email already exists.', category ='error')
        elif len(email) > 40:
            flash('Email must be at least 40 characters', category='error')
        elif password1 != password2:
            flash('Passwords don\'t match', category='error')
        elif len(password1) > 50:
            flash('Password at most can be 50 characters', category='error')
        else:
            new_user = Users(email=email, first_name=first_name,last_name=last_name, password=password1, dob=dob)
            db.session.add(new_user)
            db.session.commit()
            flash('Account created', category='success')

            return redirect(url_for('views.login'))

    return render_template('sign_up.html')


@views.route('/logout/')
@login_required
def logout():
    user = current_user.first_name
    logout_user()
    flash(f'{user} logged out successfully', category='success')
    return redirect(url_for('views.login'))


@views.route('/games/')
def games():
    return render_template('games.html')


@views.route('/collection/')
@login_required
def collection():
        return render_template('collection.html', user=current_user.first_name)


