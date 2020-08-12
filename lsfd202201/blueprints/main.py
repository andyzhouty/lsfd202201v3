# -*- coding:utf-8 -*-
from flask import render_template, Blueprint
from ..utils import get_html_from

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


@main_bp.route("/about/")
@main_bp.route("/about/<language>/")
def about(language="en"):
    if language == "en":
        zh = False
        html = get_html_from("https://raw.githubusercontent.com/z-t-y/LSFD202201/master/README.md")
    else:
        zh = True
        html = get_html_from("https://raw.githubusercontent.com/z-t-y/LSFD202201/master/README_zh.md")
    return render_template('main/about.html', content=html, zh=zh)


@main_bp.route('/kzkt/')
def kzkt():
    return render_template('main/kzkt.html')
