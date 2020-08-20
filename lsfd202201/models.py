"""
 models.py
 A python module for database storing
"""
from datetime import datetime
from itertools import permutations
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

    @staticmethod
    def query_by_id(id: int) -> db.Model:
        return Article.query.filter_by(id=id).first()

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

    @staticmethod
    def query_by_id(self, id: int) -> db.Model:
        return self.query.filter_by(id=id).first()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

class Permission:
    FOLLOW = 1
    COMMENT = 2
    WRITE = 4
    MODERATE = 8
    ADMIN = 16


class Role(db.Model):
    __tablename__ = 'roles'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), unique=True)
    default = db.Column(db.Boolean, default=False, index=True)
    permissions = db.Column(db.Integer)
    users = db.relationship('User', back_populates='role')

    def __init__(self, **kwargs):
        super(Role, self).__init__(**kwargs)
        if self.permissions is None:
            self.permissions = 0

    def add_permission(self, perm):
        if not self.has_permission(perm):
            self.permissions += perm

    def remove_permission(self, perm):
        if self.has_permission(perm):
            self.permissions -= perm

    def reset_permissions(self):
        self.permissions = 0

    def has_permission(self, perm):
        """
        Check if a individual permission is in a combined permission
        """
        return self.permissions & perm == perm


class User(db.Model, UserMixin):
    id = db.Column(db.String(20), primary_key=True)

    name = db.Column(db.String(20), unique=True, index=True)
    password_hash = db.Column(db.String(128))
    role = db.relationship('Role', back_populates='users')
    role_id = db.Column(db.Integer, db.ForeignKey('roles.id'))

    @property
    def password(self):
        raise AttributeError('Password is not a readable property')

    @password.setter
    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def verify_password(self, password):
        return check_password_hash(self.password_hash, password)
