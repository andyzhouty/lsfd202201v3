import os
from flask import Flask
from .extensions import bootstrap, share, db, pagedown


basedir = os.path.abspath(os.path.dirname(__file__))
app = Flask('lsfd202201', template_folder=os.path.join(basedir, 'templates'))
app.config.from_object('mysite.config')
app.config['SQLALCHEMY_DATABASE_URI'] = \
    'sqlite:///' + os.path.join(basedir, 'data.sqlite')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
bootstrap.init_app(app)
share.init_app(app)
db.init_app(app)
pagedown.init_app(app)
