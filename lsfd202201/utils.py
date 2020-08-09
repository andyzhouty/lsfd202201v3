from functools import wraps
from flask import redirect, session, url_for, current_app
from werkzeug.security import check_password_hash


def admin_required(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        if 'admin' not in session or not session['admin']:
            return redirect(url_for('admin.login'))
        return func(*args, **kwargs)

    return wrapper


def check_upload_password(password: str) -> bool:
    if (check_password_hash(current_app.config['UPLOAD_PASSWORD_HASH'], password) or  # noqa
            check_password_hash(current_app.config['ADMIN_PASSWORD_HASH'], password)):
        return True
    return False


def check_admin_login(password: str, name) -> bool:
    if (check_password_hash(current_app.config['ADMIN_PASSWORD_HASH'], password) and
            (name == 'ricezong' or name == 'andyzhou')):
        return True
    return False
