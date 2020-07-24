import os
from flask import Flask
from .extensions import bootstrap, ckeditor, share, db, csrf
from .settings import config

def create_app(config_name=None):
    if config_name is None:
        config_name = os.getenv('FLASK_CONFIG', 'development')

    basedir = os.path.abspath(os.path.dirname(__file__))
    app = Flask('lsfd202201', template_folder=os.path.join(basedir, 'templates'))
    app.config.from_object(config[config_name])
    app.config['SQLALCHEMY_DATABASE_URI'] = \
        'sqlite:///' + os.path.join(basedir, 'data.sqlite')
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    bootstrap.init_app(app)
    share.init_app(app)
    db.init_app(app)
    csrf.init_app(app)
    ckeditor.init_app(app)
    return app
