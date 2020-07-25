"""
 models.py
 A python module for database storing
"""
from datetime import datetime
from enum import unique
from flask import flash
from . import db


class Article(db.Model):
    """
    A class for storing articles
    """
    __tablename__ = 'articles'
    # initialize columns
    title = db.Column(db.String(64), index=True)
    author = db.Column(db.String(64))
    time = db.Column(db.String(64))
    content = db.Column(db.Text(2048))
    id = db.Column(db.Integer(), primary_key=True, unique=True)
    timestamp = db.Column(db.DateTime, default=datetime.now, index=True,
                          unique=True)

    def __repr__(self) -> str:
        return '<Article %r>' % self.title

    def query_one(self, id: int = 1) -> dict:
        return {'title': self.query.all()[id - 1].title,
                'author': self.query.all()[id - 1].author,
                'time': self.query.all()[id - 1].time,
                'content': self.query.all()[id - 1].content}

    def query_all(self) -> list:
        return self.query.all()

    def query_by_title(self, title: str) -> list:
        return self.query.filter_by(title=title).all()

    def query_by_id(self, id: int) -> db.Model:
        return self.query.filter_by(id=id).first()

    def delete_by_title(self, title: str) -> None:
        article_to_delete = self.query.filter_by(title=title).first()
        db.session.delete(article_to_delete)
        db.session.commit()
        try:
            flash("deleted")
        except Exception:
            pass

    def delete_by_id(self, id: int) -> None:
        article_to_delete = self.query.filter_by(id=id).first()
        db.session.delete(article_to_delete)
        db.session.commit()
