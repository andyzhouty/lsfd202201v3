import click
import unittest
import logging
from flask import Flask
from .extensions import db


def register_commands(app: Flask):
    @app.cli.command()
    def test() -> None:
        """Run the unit tests."""
        logging.disable(logging.CRITICAL)  # disable log
        tests = unittest.TestLoader().discover('tests')
        unittest.TextTestRunner(verbosity=1).run(tests)

    @app.cli.command()
    @click.option('-d', '--drop', default=False, help='Delete data.')
    def init_db(drop: bool) -> None:
        """Init database on a new development machine."""
        if drop:
            print("Your data will be deleted.")
            db.drop_all()
        db.create_all()

    # generates fake data
    @app.cli.command()
    @click.option('--articles', default=10, help='Generates Fake Articles')
    @click.option('--comments', default=10, help='Generates Fake Comments')
    def forge(articles, comments):
        from .fakes import db, generate_fake_articles, generate_fake_comments
        db.drop_all()
        db.create_all()
        generate_fake_articles(articles)
        generate_fake_comments(comments)
