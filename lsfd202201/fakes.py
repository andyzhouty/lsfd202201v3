"""
Generates fake data for development use.
"""
from faker import Faker
from werkzeug.security import generate_password_hash
import click
from .models import db, Article, Feedback, Admin, Creator, User

fake = Faker('zh-CN')


def generate_fake_articles(count: int) -> None:
    """Generates fake articles."""
    for i in range(count):
        article = Article(
            title=fake.sentence(),
            author=fake.name(),
            date=fake.date_time_this_year().strftime("%Y-%m-%d"),
            content=fake.text(200),
            timestamp=fake.date_time_this_year()
        )
        db.session.add(article)
    db.session.commit()
    print(f"Generated {count} fake articles.")


def generate_fake_feedback(count: int) -> None:
    """Generates fake feedback."""
    for i in range(count):
        feedback = Feedback(
            author=fake.name(),
            body=fake.sentence(),
            timestamp=fake.date_time_this_year()
        )
        db.session.add(feedback)
    db.session.commit()
    print(f"Generated {count} fake feedbacks.")


def generate_fake_admins(count: int) -> None:
    for i in range(count):
        admin = Admin(
            name=fake.name(),
            password_hash=generate_password_hash(fake.password()),
        )
        db.session.add(admin)
    db.session.commit()
    click.echo(f"Generated {count} fake admins.")


def generate_fake_creators(count: int) -> None:
    for i in range(count):
        creator = Creator(
            name=fake.name(),
            email=fake.email(),
            member_since=fake.date_time_this_year(),
            password_hash=generate_password_hash(fake.password())
        )
        db.session.add(creator)
    db.session.commit()
    click.echo(f"Generated {count} fake creators.")


def generate_fake_users(count: int) -> None:
    for i in range(count):
        user = User(
            name=fake.name(),
            password_hash=generate_password_hash(fake.sentence())
        )
        db.session.add(user)
    db.session.commit()
    click.echo(f"Generated {count} fake users.")
