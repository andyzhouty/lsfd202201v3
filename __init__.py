import os
from flask import Flask
from .extensions import bootstrap, share, db, pagedown


app = Flask('lsfd202201')
basedir = os.path.abspath(os.path.dirname(__file__))
app.config.from_pyfile('config.py')
app.config['SQLALCHEMY_DATABASE_URI'] = \
    'sqlite:///' + os.path.join(basedir, 'data.sqlite')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
bootstrap.init_app(app)
share.init_app(app)
db.init_app(app)
pagedown.init_app(app)
