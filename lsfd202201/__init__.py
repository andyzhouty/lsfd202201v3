import os
import unittest
import logging
from logging.handlers import RotatingFileHandler
from flask import Flask
from flask.logging import default_handler
import pymysql
from .extensions import (
    bootstrap, ckeditor, share, db, csrf, migrate, mail, moment
)
from .settings import config
from .blueprints.admin import admin_bp
from .blueprints.articles import articles_bp
from .blueprints.main import main_bp
from .blueprints.comments import comment_bp


def create_app(config_name=None) -> Flask:
    if config_name is None:
        config_name = os.getenv('FLASK_CONFIG', 'development')
    pymysql.install_as_MySQLdb()
    app = Flask('lsfd202201')
    app.config.from_object(config[config_name])
    register_logger(app)
    register_extensions(app, db)
    register_blueprints(app)
    register_commands(app, db)
    return app


def register_logger(app: Flask):
    app.logger.setLevel(logging.INFO)

    formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s "
                                  "%(message)s")
    file_handler = RotatingFileHandler(
        filename="logs/lsfd202201.log",
        maxBytes=10 * 1024 * 1024,
        backupCount=10
    )
    file_handler.setFormatter(formatter)
    file_handler.setLevel(logging.INFO)
    default_handler.setLevel(logging.INFO)
    app.logger.addHandler(file_handler)
    if not app.debug:
        app.logger.addHandler(file_handler)
        app.logger.addHandler(default_handler)


def register_extensions(app: Flask, db) -> None:
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


def register_commands(app: Flask, db):
    @app.cli.command()
    def test():
        """Run the unit tests."""
        tests = unittest.TestLoader().discover('tests')
        unittest.TextTestRunner(verbosity=1).run(tests)

    @app.cli.command()
    def initdb():
        """Init database on a new machine."""
        db.create_all()
