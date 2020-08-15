"""
 models.py
 A python module for database storing
"""
from datetime import datetime
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from . import db


class Article(db.Model):
    """
    A model for articles
    """
    __tablename__ = 'articles'
    # initialize columns
    title = db.Column(db.String(64), index=True)
    author = db.Column(db.String(64))
    date = db.Column(db.String(64))
    content = db.Column(db.Text(2048))
    id = db.Column(db.Integer(), primary_key=True)
    timestamp = db.Column(db.DateTime, default=datetime.now, index=True)

    def __repr__(self) -> str:
        return f'<Article {self.title}>'

    def query_by_id(self, id: int) -> db.Model:
        return self.query.filter_by(id=id).first()

    def delete(self):
        if self in db.session:
            db.session.delete(self)
            db.session.commit()


class Feedback(db.Model):
    __tablename__ = 'feedback'
    id = db.Column(db.Integer(), primary_key=True)
    body = db.Column(db.String(200))
    author = db.Column(db.String(20))
    timestamp = db.Column(db.DateTime, default=datetime.utcnow, index=True)

    def __repr__(self):
        return f'<Feedback {self.body[:10]}...>'

    def query_by_id(self, id: int) -> db.Model:
        return self.query.filter_by(id=id).first()

    def delete(self):
        db.session.delete(self)
        db.session.commit()


class Admin(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20))
    password_hash = db.Column(db.String(128))

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def validate_password(self, password):
        return check_password_hash(self.password_hash, password)


class Creator(db.Model, UserMixin):
    id = db.Column(db.String(20), primary_key=True)

    name = db.Column(db.String(20), unique=True, index=True)
    email = db.Column(db.String(200), unique=True, index=True)
    password_hash = db.Column(db.String(128))
    member_since = db.Column(db.DateTime, default=datetime.utcnow)
    confirmed = db.Column(db.Boolean, default=False)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def validate_password(self, password):
        return check_password_hash(self.password_hash, password)


class User(db.Model, UserMixin):
    id = db.Column(db.String(20), primary_key=True)

    name = db.Column(db.String(20), unique=True, index=True)
    password_hash = db.Column(db.String(128))

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def validate_password(self, password):
        return check_password_hash(self.password_hash, password)
