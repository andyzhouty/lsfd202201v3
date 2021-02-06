# flake8: noqa
from urllib.parse import urlparse, urljoin
from functools import wraps
import requests
from flask import redirect, session, url_for, current_app, request
from werkzeug.security import check_password_hash
from markdown import markdown
from .models import User


def check_article_password(password: str) -> bool:
    if check_password_hash(
        current_app.config["ARTICLE_PASSWORD_HASH"], password
    ) or check_password_hash(current_app.config["ADMIN_PASSWORD_HASH"], password):
        return True
    return False


def check_admin_login(password: str, name: str) -> bool:
    admin = User.query.filter_by(name=name).first()
    return admin.validate_password(password)


def get_html_from(filename: str) -> str:
    content = open(filename, "r").read()
    return markdown(content)


def is_safe_url(target):
    ref_url = urlparse(request.host_url)
    test_url = urlparse(urljoin(request.host_url, target))
    return test_url.scheme in ("http", "https") and ref_url.netloc == test_url.netloc


def redirect_back(default="main.main", **kwargs):
    for target in request.args.get("next"), request.referrer:
        if not target:
            continue
        if is_safe_url(target):
            return redirect(target)
    return redirect(url_for(default, **kwargs))
