# -*- coding:utf-8 -*-
from flask import render_template, Blueprint


main_bp = Blueprint('main', __name__)


@main_bp.route('/')
@main_bp.route('/index')
def index():
    return render_template('index.html')


@main_bp.route('/main')
def main():
    return render_template('main.html')


@main_bp.route('/members')
def members():
    return render_template('members.html')


@main_bp.route('/video')
def video():
    return render_template('video.html')


@main_bp.route('/about-zh')
def about_zh():
    return render_template("about_zh.html")


@main_bp.route('/about')
@main_bp.route('/about-en')
def about_en():
    return render_template("about_en.html")


@main_bp.route('/kzkt')
def kzkt():
    return render_template('kzkt.html')


@main_bp.errorhandler(404)
@main_bp.route('/hrtg')
def page_not_found(e="hrtg"):
    return render_template('coffin_dance.html'), 404


@main_bp.errorhandler(500)
def internal_server_error(e):
    return render_template('error.html',
                           error_message="500 INTERNAL SERVER ERROR"), 500


@main_bp.errorhandler(405)
def method_not_allowed(e):
    return render_template('error.html',
                           error_message="405 METHOD NOT ALLOWED"), 405
