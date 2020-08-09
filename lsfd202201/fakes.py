"""
Generates fake data for development use.
"""
from faker import Faker
from .models import db, Article, Comment

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


def generate_fake_comments(count: int) -> None:
    """Generates fake comments."""
    for i in range(count):
        comment = Comment(
            author=fake.name(),
            body=fake.sentence(),
            timestamp=fake.date_time_this_year()
        )
        db.session.add(comment)
    db.session.commit()
    print(f"Generated {count} fake comments.")
