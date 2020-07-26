import os
from flask import Flask
from .extensions import bootstrap, ckeditor, share, db, csrf
from .settings import config
from .blueprints.admin import admin_bp
from .blueprints.articles import articles_bp
from .blueprints.main import main_bp


def create_app(config_name=None) -> Flask:
    if config_name is None:
        config_name = os.getenv('FLASK_CONFIG', 'development')

    basedir = os.path.abspath(os.path.dirname(__file__))
    app = Flask('lsfd202201', template_folder=os.path.join(
        basedir, 'templates'))
    app.config.from_object(config[config_name])
    register_extensions(app)
    register_blueprints(app)
    return app


def register_extensions(app: Flask) -> None:
    bootstrap.init_app(app)
    share.init_app(app)
    db.init_app(app)
    csrf.init_app(app)
    ckeditor.init_app(app)


def register_blueprints(app: Flask) -> None:
    app.register_blueprint(main_bp)
    app.register_blueprint(admin_bp, url_prefix="/admin")
    app.register_blueprint(articles_bp, url_prefix="/articles")
