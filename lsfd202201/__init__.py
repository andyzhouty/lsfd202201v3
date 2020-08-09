import os
import unittest
import logging
from logging.handlers import RotatingFileHandler
from flask import Flask
from flask.logging import default_handler
from .extensions import (
    bootstrap, ckeditor, share, db, csrf, migrate, mail, moment
)
from .models import Article, Comment
from .settings import config
from .errors import register_error_handlers
from .commands import register_commands
from .blueprints.admin import admin_bp
from .blueprints.articles import articles_bp
from .blueprints.main import main_bp
from .blueprints.comments import comment_bp


def create_app(config_name=None) -> Flask:
    if config_name is None:
        config_name = os.getenv('FLASK_CONFIG', 'development')
    app = Flask('lsfd202201')
    app.config.from_object(config[config_name])
    register_logger(app)
    register_extensions(app)
    register_blueprints(app)
    register_commands(app)
    register_error_handlers(app)
    register_shell_context(app)
    return app


def register_logger(app: Flask):
    app.logger.setLevel(logging.INFO)

    formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s "
                                  "%(message)s")
    if app.debug:
        file_handler = RotatingFileHandler(
            filename="logs/lsfd202201.log",
            maxBytes=10 * 1024 * 1024,
            backupCount=10
        )
        file_handler.setFormatter(formatter)
        file_handler.setLevel(logging.INFO)
        app.logger.addHandler(file_handler)
    if not app.debug:
        default_handler.setLevel(logging.INFO)
        app.logger.addHandler(default_handler)


def register_extensions(app: Flask) -> None:
    bootstrap.init_app(app)
    share.init_app(app)
    db.init_app(app)
    csrf.init_app(app)
    ckeditor.init_app(app)
    migrate.init_app(app, db)
    mail.init_app(app)
    moment.init_app(app)


def register_blueprints(app: Flask) -> None:
    app.register_blueprint(main_bp)
    app.register_blueprint(admin_bp, url_prefix="/admin")
    app.register_blueprint(articles_bp, url_prefix="/articles")
    app.register_blueprint(comment_bp, url_prefix="/comments")


def register_shell_context(app: Flask) -> None:
    @app.shell_context_processor
    def make_shell_context():
        return dict(
            db=db,
            Article=Article,
            Comment=Comment
        )
