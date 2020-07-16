# -*- coding:utf-8 -*-
import os
from flask import (Flask, render_template, request, flash, 
                   escape, redirect, url_for, session)
from flask.helpers import url_for
from flask_bootstrap import Bootstrap
from flask_share import Share
from flask_sqlalchemy import SQLAlchemy

# basic configurations
app = Flask(__name__)
basedir = os.path.abspath(os.path.dirname(__file__))
app.config.from_object('config')
app.config['SQLALCHEMY_DATABASE_URI'] =\
    'sqlite:///' + os.path.join(basedir, 'data.sqlite')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# use bootstrap and flask-share
bootstrap = Bootstrap(app)
share = Share(app)

# import defined classes
from forms import UploadForm, AdminForm
from models import Article


# url routings

@app.route('/')
@app.route('/index')
def index():
    return render_template('index.html')


@app.route('/main')
def main():
    return render_template('main.html', warning=True)


@app.route('/members')
def members():
    return render_template('members.html', warning=True)


@app.route('/articles')
@app.route('/articles/<int:id>')
def articles(id=1):
    # Query data from data.sqlite
    article = Article().query_one(id)
    articles = Article().query_all()
    return render_template('articles.html', warning=True,
                           title=article["title"],
                           author=article["author"],
                           time=article["time"],
                           content=article["content"],
                           enumerate_items=enumerate(articles, start=1))


@app.route('/video')
def video():
    return render_template('video.html', warning=True)


@app.route('/upload')
def upload():
    form = UploadForm()
    return render_template('upload.html', warning=False, form=form)


@app.route('/upload-result', methods=['POST'])
def upload_result():
    # get vars from upload page
    a = Article()
    name = escape(request.form['name'])
    password = escape(request.form['password'])
    time = escape(request.form['time'])
    title = escape(request.form['title'])
    content = escape(request.form['content'])
    id = len(a.query_all()) + 1
    # password protection
    if password != app.config['PASSWORD']:
        flash("Wrong Password")
        return render_template('upload_fail.html')
    # commit data
    article = Article(title=title, author=name, content=content, time=time,
                      id=id)
    db.session.add(article)
    db.session.commit()
    flash("Upload Success")
    return render_template('upload_result.html')


@app.route('/share')
def share():
    return render_template("share.html", warning=False)


@app.route('/admin-login')
def admin_login():
    session['admin'] = False
    form = AdminForm()
    return render_template("admin_login.html", warning=False, form=form)


@app.route('/admin', methods=['POST'])
def admin():
    session['input_name'] = escape(request.form['admin_name'])
    session['input_password'] = escape(request.form['password'])
    if not session['admin']:
        if (session['input_name'] != 'rice'
            and session['input_name'] != 'andyzhou'):
            return redirect(url_for('admin_login'))
        if session['input_password'] != app.config['ADMIN_PASSWORD']:
            return redirect(url_for('admin_login'))
    session['admin'] = True
    session['admin_name'] = session['input_name']
    query_article = Article(title="test", author="test",
                            time="test", content="test")
    return render_template('admin.html', warning=False,
                           name=session['admin_name'].capitalize(),
                           articles=query_article.query_all())


@app.route('/kzkt')
def cloud_class():
    return render_template('kzkt.html', warning=True)


@app.route('/jkl')
def jkl():
    return render_template('jinkela.html', warning=False)


@app.route('/trump')
def trump():
    return render_template('trump.html', warning=False)


@app.errorhandler(404)
@app.route('/hrtg')
def page_not_found(e="hrtg"):
    return render_template('coffin_dance.html', warning=False), 404


@app.errorhandler(500)
@app.route('/aoligei')
def internal_server_error(e="aoligei"):
    return render_template('mickey_aoligei.html', warning=False, 
                           error_message="500 INTERNAL SERVER ERROR"), 500

@app.errorhandler(405)
def method_not_allowed(e):
    return render_template('xizhilang.html', warning=False,
                           error_message="405 METHOD NOT ALLOWED"), 405
