import os
import sys
from werkzeug.security import generate_password_hash

basedir = os.path.abspath(os.path.dirname(__file__))
WINDOWS = sys.platform.startswith('win')
if WINDOWS:
    sqlite_file = 'sqlite:///' + os.path.join(basedir, 'data.sqlite')
else:
    sqlite_file = 'sqlite:////' + os.path.join(basedir, 'data.sqlite')


class Base:
    SECRET_KEY = os.getenv('SECRET_KEY')

    PASSWORD = generate_password_hash(os.getenv('PASSWORD'))
    ADMIN_PASSWORD = generate_password_hash(os.getenv('ADMIN_PASSWORD'))

    SQLALCHEMY_DATABASE_URI = os.getenv("SQLALCHEMY_DATABASE_URI", sqlite_file)
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    MAIL_SERVER = os.getenv("MAIL_SERVER")
    MAIL_PORT = 587
    MAIL_USE_TLS = True
    MAIL_USERNAME = os.getenv("MAIL_USERNAME")
    MAIL_PASSWORD = os.getenv("MAIL_PASSWORD")
    MAIL_DEFAULT_SENDER = (
        os.getenv("DEFAULT_SENDER_NAME"),
        os.getenv("MAIL_USERNAME")
    )

    ADMIN_ONE_EMAIL = os.getenv('ADMIN_ONE_EMAIL')
    ADMIN_TWO_EMAIL = os.getenv('ADMIN_TWO_EMAIL')
    APP_MAIL_SUBJECT_PREFIX = "[LSFD202201]"
    DEFAULT_EMAIL_SENDER = os.getenv("DEFAULT_EMAIL_SENDER")
    BOOTSTRAP_SERVE_LOCAL = True


class Production(Base):
    DEBUG = False
    FLASK_CONFIG = 'production'


class Development(Base):
    DEBUG = True
    FLASK_CONFIG = 'development'


class Test(Base):
    TESTING = True
    WTF_SCRF_ENABLED = False
    SQLALCHEMY_DATABASE_URI = 'sqlite:///:memory:'


config = {
    'production': Production,
    'development': Development,
    'testing': Test
}
