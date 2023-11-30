from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
import os

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URI', 'mysql+pymysql://root:ealexan2@localhost'
                                                                       '/gamesdatabase')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.secret_key = os.environ.get('SECRET_KEY', 'default-secret-key')

db = SQLAlchemy()
login_manager = LoginManager()
login_manager.login_view = 'views.login'

from models import User
from views import views_blueprint

app.register_blueprint(views_blueprint, url_prefix='/')

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

if __name__ == '__main__':
    db.init_app(app)
    login_manager.init_app(app)
    with app.app_context():
        db.create_all()
    app.run(debug=True)
