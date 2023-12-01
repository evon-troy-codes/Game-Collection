from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_user, logout_user, current_user, login_required
from models import User, GameCollection, GameCollectionItems, Games
from datetime import datetime
from extensions import db  # Import the db instance

views_blueprint = Blueprint('views', __name__)


@views_blueprint.route('/')
def home():
    return redirect(url_for('views.games'))


@views_blueprint.route('/login/', methods=['POST', 'GET'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')

        user = User.query.filter_by(email=email).first()
        if user and user.password == password:
            flash('Logged in successfully.')
            login_user(user, remember=True)
            return redirect(url_for('views.profile'))
        else:
            flash('Incorrect email or password.', category='error')

    return render_template('login.html', user=current_user)


@views_blueprint.route('/profile/', methods=['GET', 'POST'])
@login_required
def profile():
    if request.method == 'POST':
        new_first_name = request.form.get('first_name')
        new_last_name = request.form.get('last_name')
        new_email = request.form.get('email')
        new_dob = request.form.get('dob')

        updated = False
        if new_first_name and new_first_name != current_user.first_name:
            current_user.first_name = new_first_name
            updated = True

        if new_last_name and new_last_name != current_user.last_name:
            current_user.last_name = new_last_name
            updated = True

        if new_email and new_email != current_user.email:
            current_user.email = new_email
            updated = True

        if new_dob:
            try:
                new_dob = datetime.strptime(new_dob, '%Y-%m-%d')
                if new_dob != current_user.dob:
                    current_user.dob = new_dob
                    updated = True
            except ValueError:
                flash('Invalid date format.')

        if updated:
            db.session.commit()
            flash('Profile updated successfully.')
        else:
            flash('No changes were made.')

    return render_template('profile.html', user=current_user)


@views_blueprint.route('/sign-up/', methods=['POST', 'GET'])
def sign_up():
    if current_user.is_authenticated:
        flash('You are already logged in.')
        return redirect(url_for('views.profile'))

    if request.method == 'POST':
        email = request.form.get('email')
        first_name = request.form.get('first_name')
        last_name = request.form.get('last_name')
        password1 = request.form.get('password1')
        password2 = request.form.get('password2')
        dob = request.form.get('dob')

        user = User.query.filter_by(email=email).first()

        if user:
            flash('Email already exists.', category='error')
        elif len(email) > 40:
            flash('Email must be less than 40 characters', category='error')
        elif password1 != password2:
            flash('Passwords don\'t match', category='error')
        elif len(password1) < 3 or len(password1) > 50:
            flash('Password must be between 3 and 50 characters', category='error')
        else:
            new_user = User(email=email, first_name=first_name, last_name=last_name, password=password1, dob=dob)
            db.session.add(new_user)
            db.session.commit()
            flash('Account created', category='success')
            return redirect(url_for('views.login'))

    return render_template('sign_up.html')


@views_blueprint.route('/logout/')
@login_required
def logout():
    logout_user()
    flash('You have been logged out.')
    return redirect(url_for('views.login'))


@views_blueprint.route('/games/')
def games():
    return render_template('games.html')


@views_blueprint.route('/collection/')
@login_required
def collection():
    return render_template('collection.html', user=current_user.first_name)
