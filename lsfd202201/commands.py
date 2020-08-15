import os
import sys
import unittest
import logging
import click
from flask import Flask
from .models import db, Admin, generate_password_hash

COVERAGE = None
if os.getenv('FLASK_COVERAGE', False):
    import coverage
    COVERAGE = coverage.coverage(branch=True, source='lsfd202201')
    COVERAGE.start()


def register_commands(app: Flask): # noqa
    @app.cli.command()
    @click.option('--coverage/--no-coverage', default=False, help='Run tests with coverage')
    def test(coverage: bool) -> None:
        """Run the unit tests."""
        if os.getenv("FLASK_COVERAGE", False):
            os.environ['FLASK_COVERAGE'] = '1'
            os.execvp(sys.executable, [sys.executable] + sys.argv)
        logging.disable(logging.CRITICAL)  # disable log
        tests = unittest.TestLoader().discover('tests')
        unittest.TextTestRunner(verbosity=2).run(tests)
        if COVERAGE:
            COVERAGE.stop()
            COVERAGE.save()
            print('Coverage Summary: ')
            COVERAGE.report()
            basedir = os.path.abspath(os.path.abspath(__file__))
            covdir = os.path.join(basedir, 'htmlcov')
            COVERAGE.html_report(directory=covdir)
            print(f'HTML Version: file://{covdir}/index.html')
            COVERAGE.erase()

    @app.cli.command()
    @click.option('--drop/--no-drop', default=False, help='Delete data.')
    def init_db(drop: bool) -> None:
        """Init database on a new development machine."""
        if drop:
            print("Your data will be deleted.")
            db.drop_all()
        db.create_all()

    @app.cli.command()
    @click.option('--name', prompt=True)
    @click.option('--password', prompt=True, hide_input=True)
    def create_admin(name, password):
        if Admin.query.count() < 2:
            admin = Admin(
                name=name,
                password_hash=generate_password_hash(password)
            )
            db.session.add(admin)
            db.commit()
        else:
            print("Exceeded the max number of admins: 2")

    @app.cli.command()
    @click.option('--articles', default=10, help='Generates fake articles')
    @click.option('--feedback', default=10, help='Generates fake feedbacks')
    @click.option('--admin', default=1, help='Generates fake admins')
    @click.option('--creator', default=5, help='Generates fake creators')
    @click.option('--user', default=10, help='Generates fake users')
    def forge(articles, feedback, admin, creator, user):
        """Generates fake data"""
        from . import fakes as f
        db.drop_all()
        db.create_all()
        f.generate_fake_articles(articles)
        f.generate_fake_feedback(feedback)
        f.generate_fake_admins(admin)
        f.generate_fake_creators(creator)
        f.generate_fake_users(user)
