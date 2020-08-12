# flake8: noqa
from functools import wraps
import requests
from flask import redirect, session, url_for, current_app
from werkzeug.security import check_password_hash
from markdown import markdown


def admin_required(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        if 'admin' not in session or not session['admin']:
            return redirect(url_for('admin.login'))
        return func(*args, **kwargs)

    return wrapper


def check_article_password(password: str) -> bool:
    if (check_password_hash(current_app.config['ARTICLE_PASSWORD_HASH'], password) or
            check_password_hash(current_app.config['ADMIN_PASSWORD_HASH'], password)):
        return True
    return False


def check_admin_login(password: str, name) -> bool:
    if (check_password_hash(current_app.config['ADMIN_PASSWORD_HASH'], password) and
            (name == 'ricezong' or name == 'andyzhou')):
        return True
    return False


def get_html_from(url: str) -> str:
    response = requests.get(url)
    return markdown(response.text)
