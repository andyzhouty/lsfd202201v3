# -*- coding:utf-8 -*-
import os
from flask import (Flask, render_template, request, flash,
                   escape, redirect, url_for, session)
from flask_bootstrap import Bootstrap
from flask_share import Share
from flask_sqlalchemy import SQLAlchemy
from flask_pagedown import PageDown
from werkzeug.security import check_password_hash
from markdown import markdown
from forms import UploadForm, AdminLoginForm, AdminDeleteForm

# basic configurations
app = Flask(__name__)
basedir = os.path.abspath(os.path.dirname(__file__))
app.config.from_object('app_config')
app.config['SQLALCHEMY_DATABASE_URI'] = \
    'sqlite:///' + os.path.join(basedir, 'data.sqlite')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
pagedown = PageDown(app)
db = SQLAlchemy(app)

# use bootstrap and flask-share
bootstrap = Bootstrap(app)
share = Share(app)

# import db
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
    all_articles = Article().query_all()
    return render_template('articles.html', warning=True,
                           title=article["title"],
                           author=article["author"],
                           time=article["time"],
                           content=markdown(article["content"]),
                           enumerate_items=enumerate(all_articles, start=1))


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
    password = request.form['password']
    time = escape(request.form['time'])
    title = escape(request.form['title'])
    content = request.form['pagedown']
    id = len(a.query_all()) + 1
    PASSWORD = app.config['PASSWORD']
    ADMIN_PASSWORD = app.config['ADMIN_PASSWORD']
    # password protection
    if not (check_password_hash(ADMIN_PASSWORD, password)
            or check_password_hash(PASSWORD, password)):
        flash("Wrong Password")
        return render_template('post_fail.html', url=url_for("upload"))
    # commit data
    article = Article(title=title, author=name, content=content, time=time,
                      id=id)
    db.session.add(article)
    db.session.commit()
    flash("Upload Success")
    return render_template('post_result.html', url=url_for("articles"))


@app.route('/share')
def share():
    return render_template("share.html", warning=False)


@app.route('/markdown-help')
def markdown_help():
    return render_template("markdown_help.html", warning=False)


@app.route('/admin-login')
def admin_login():
    session['admin'] = False
    form = AdminLoginForm()
    return render_template("admin_login.html", warning=False, form=form)


@app.route('/admin', methods=['GET', 'POST'])
def admin():
    if not session['admin']:
        session['input_name'] = escape(request.form['admin_name'])
        session['input_password'] = escape(request.form['password'])
        if (session['input_name'] != 'rice'
                and session['input_name'] != 'andyzhou'):
            return redirect(url_for('admin_login'))
        if not check_password_hash(app.config['ADMIN_PASSWORD'],
                                   session['input_password']):
            print("Password Incorrect.")
            return redirect(url_for('admin_login'))
    session['admin'] = True
    session['admin_name'] = session['input_name']
    query_article = Article(title="test", author="test",
                            time="test", content="test")
    form = AdminDeleteForm()
    return render_template('admin.html', warning=False,
                           name=session['admin_name'].capitalize(),
                           articles=query_article.query_all(),
                           form=form)


@app.route('/admin-delete', methods=['POST'])
def admin_delete():
    article_id_to_del = request.form['id']
    test_article = Article()
    exist = test_article.query_by_id(article_id_to_del)
    if exist:
        Article().delete_by_id(article_id_to_del)
        flash(f"Article id {article_id_to_del} deleted")
    else:
        flash(f"Article id {article_id_to_del} not found.")
    return render_template("post_result.html", url=url_for("admin"))


@app.route('/about')
def about():
    return render_template("about.html")


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
