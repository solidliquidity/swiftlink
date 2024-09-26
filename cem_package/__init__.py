from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from os import path
from werkzeug.utils import secure_filename
from flask_migrate import Migrate

db = SQLAlchemy()

UPLOAD_FOLDER = 'static/uploads/'

def create_app():
    app = Flask(__name__)
    migrate = Migrate(app, db)
    app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:Limehousecut!1@localhost/news_db'
    # 'postgresql://u9e2m3f8k4haus:pe1535ee06f2c70a21fdda370d0722bbe65e77168c826800fb8096602631d1fc4@cbec45869p4jbu.cluster-czrs8kj4isg7.us-east-1.rds.amazonaws.com:5432/d7htgdui5k0qms'  # Updated DB URL
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.secret_key = 'b8f3aabd290888870cc64c5ab34d0484'
    app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
    db.init_app(app)

    from cem_package.views import views
    app.register_blueprint(views, url_prefix='/')

    from .models import users, news

    with app.app_context():
        db.create_all()
    
    login_manager = LoginManager()
    login_manager.init_app(app)
    login_manager.login_view = 'views.login'

    @login_manager.user_loader
    def load_user(id):
        return users.query.get(int(id))

    return app


def create_database(app):
    db.create_all(app=app)
    print('Database created!')