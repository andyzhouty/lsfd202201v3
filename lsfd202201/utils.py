from functools import wraps
from flask import redirect, session, url_for


def admin_reqired(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        if 'admin' not in session or not session['admin']:
            return redirect(url_for('admin.login'))
        return func(*args, **kwargs)
    return wrapper
