from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_caching import Cache
from os import path
from flask_login import LoginManager
from cryptography.fernet import Fernet
import os



db = SQLAlchemy()
DB_NAME = "database.db"
cache = Cache(config={'CACHE_TYPE': 'simple'})

if 'CRYPTO_KEY' in os.environ:
    key = os.environ.get("CRYPTO_KEY")
else:
    raise ValueError("CRYPTO_KEY not found.")

cipher_suite = Fernet(key)

def create_app():
    app = Flask(__name__)
    if 'SECRET_KEY' in os.environ:
        app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY')
    else:
        raise ValueError("SECRET_KEY not found.")
    app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{DB_NAME}'
    db.init_app(app)
    cache.init_app(app)
    
    from .views import views
    from .auth import auth
    from .user import user

    app.register_blueprint(views, url_prefix='/')
    app.register_blueprint(auth, url_prefix='/')
    app.register_blueprint(user, url_prefix='/')

    from .models import User

    create_database(app)

    login_manager = LoginManager()
    login_manager.login_view = 'auth.login'
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(id):
        return User.query.get(int(id))
    
    return app


def create_database(app):
    if not path.exists('instance/' + DB_NAME):
        with app.app_context():
            db.create_all()
            print('Base de dados criada com sucesso!')
        