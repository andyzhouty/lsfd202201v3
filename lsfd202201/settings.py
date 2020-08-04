# flake8: noqa
import os
import sys
from werkzeug.security import generate_password_hash

basedir = os.path.abspath(os.path.dirname(__file__))
WINDOWS = sys.platform.startswith('win')
if WINDOWS:
    sqlite_file = 'sqlite:///' + os.path.join(basedir, 'data.sqlite')
    sqlite_file_articles = 'sqlite:///' + os.path.join(basedir, 'articles.sqlite')
    sqlite_file_comments = 'sqlite:///' + os.path.join(basedir, 'comments.sqlite')
else:
    sqlite_file = 'sqlite:///' + os.path.join(basedir, 'data.sqlite')
    sqlite_file_articles = 'sqlite:///' + os.path.join(basedir, 'articles.sqlite')
    sqlite_file_comments = 'sqlite:///' + os.path.join(basedir, 'comments.sqlite')


class Base:
    SECRET_KEY = os.getenv('SECRET_KEY')

    PASSWORD = generate_password_hash(os.getenv('PASSWORD'))
    ADMIN_PASSWORD = generate_password_hash(os.getenv('ADMIN_PASSWORD'))

    SQLALCHEMY_DATABASE_URI = os.getenv("SQLALCHEMY_DATABASE_URI", sqlite_file)
    SQLALCHEMY_BINDS = {
        'articles': os.getenv("DATABASE_ARTICLES"),
        'comments': os.getenv("DATABASE_COMMENTS")
    }
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    MAIL_SERVER = os.getenv("MAIL_SERVER")
    MAIL_PORT = 587
    MAIL_USE_TLS = True
    MAIL_USERNAME = os.getenv("MAIL_USERNAME")
    MAIL_PASSWORD = os.getenv("MAIL_PASSWORD")
    MAIL_DEFAULT_SENDER = os.getenv("DEFAULT_EMAIL_SENDER")

    ADMIN_ONE_EMAIL = os.getenv('ADMIN_ONE_EMAIL')
    ADMIN_TWO_EMAIL = os.getenv('ADMIN_TWO_EMAIL')
    ADMIN_EMAIL_LIST = [
        ADMIN_ONE_EMAIL,
        ADMIN_TWO_EMAIL
    ]
    BOOTSTRAP_SERVE_LOCAL = True


class Production(Base):
    DEBUG = False
    FLASK_CONFIG = 'production'
    EMAIL_ADMIN = True


class Development(Base):
    DEBUG = True
    FLASK_CONFIG = 'development'
    EMAIL_ADMIN = False
    ADMIN_EMAIL_LIST = [os.getenv("ADMIN_TWO_EMAIL")]


class Test(Base):
    TESTING = True
    WTF_CSRF_ENABLED = False
    SQLALCHEMY_DATABASE_URI = 'sqlite:///:memory:'
    SQLALCHEMY_BINDS = {
        'articles': sqlite_file_articles,
        'comments': sqlite_file_comments
    }
    MAIL_DEFAULT_SENDER = os.getenv("DEFAULT_EMAIL_SENDER")
    EMAIL_ADMIN = False
    ADMIN_EMAIL_LIST = [os.getenv("ADMIN_TWO_EMAIL")]


config = {
    'production': Production,
    'development': Development,
    'testing': Test
}
