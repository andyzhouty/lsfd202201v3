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
