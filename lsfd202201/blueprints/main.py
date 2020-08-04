# -*- coding:utf-8 -*-
from flask import render_template, Blueprint
from flask_wtf.csrf import CSRFError


main_bp = Blueprint('main', __name__)


@main_bp.route('/')
@main_bp.route('/index/')
def index():
    return render_template('main/index.html')


@main_bp.route('/main/')
def main():
    return render_template('main/main.html')


@main_bp.route('/members/')
def members():
    return render_template('main/members.html')


@main_bp.route('/video/')
def video():
    return render_template('main/video.html')


@main_bp.route('/about-zh/')
def about_zh():
    return render_template('main/about_zh.html')


@main_bp.route('/about/')
@main_bp.route('/about-en/')
def about_en():
    return render_template('main/about_en.html')


@main_bp.route('/kzkt/')
def kzkt():
    return render_template('main/kzkt.html')


@main_bp.app_errorhandler(400)
@main_bp.app_errorhandler(CSRFError)
def bad_request(e):
    return render_template('main/error.html',
                           error_message="400 Bad Request"), 400


@main_bp.app_errorhandler(404)
def page_not_found(e):
    # special easter egg :P
    return render_template('main/404.html',
                           error_message="404 Not Found"), 404


@main_bp.app_errorhandler(405)
def method_not_allowed(e):
    return render_template('main/error.html',
                           error_message="405 Method Not Allowed"), 405


@main_bp.app_errorhandler(500)
def internal_server_error(e):
    return render_template('main/error.html',
                           error_message="500 Internal Server Error"), 500
