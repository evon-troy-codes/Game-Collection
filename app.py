from flask import Flask
import os
from extensions import db, login_manager  # Import db and login_manager

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URI', 'mysql+pymysql://root:ealexan2@localhost/gamesdatabase')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.secret_key = os.environ.get('SECRET_KEY', 'default-secret-key')

db.init_app(app)
login_manager.init_app(app)
login_manager.login_view = 'views.login'

# Import models after initializing db but before defining user_loader
from models import User

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# Import views after defining user_loader
from views import views_blueprint
app.register_blueprint(views_blueprint, url_prefix='/')

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)
