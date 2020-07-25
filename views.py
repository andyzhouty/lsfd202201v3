# -*- coding:utf-8 -*-
import os
from flask import (render_template, request, flash,
                   escape, redirect, url_for, session, current_app)
from werkzeug.security import check_password_hash
from . import create_app
from .functions import escape_quotes
from .models import Article
from .forms import UploadForm, AdminLoginForm, EditForm
from .extensions import db


app = create_app()


@app.route('/')
@app.route('/index')
def index():
    return render_template('index.html')


@app.route('/main')
def main():
    return render_template('main.html')


@app.route('/members')
def members():
    return render_template('members.html')


@app.route('/articles')
def articles():
    page = request.args.get('page', 1, int)  # get(key, default=None, type=None)
    all_articles = Article().query_all()
    if all_articles:
        article = Article().query_one(page)
        pagination = Article.query.order_by(
            Article.timestamp.desc()).paginate(page, 1)
        return render_template('articles.html',
                               this_article=article,
                               content=article["content"],
                               pagination=pagination)
    flash("No Articles! Please Upload one first!", "warning")
    return render_template("result.html", url=url_for("upload"))


@app.route('/video')
def video():
    return render_template('video.html')


@app.route('/upload')
def upload():
    form = UploadForm()
    return render_template('upload.html', form=form)


@app.route('/upload-result', methods=['POST'])
def upload_result():
    # get vars from upload page
    a = Article()
    name = escape(request.form['name'])
    password = request.form['password']
    date = escape(request.form['date'])
    title = escape(request.form['title'])
    content = request.form['content']
    id = len(a.query_all()) + 1
    config_password = app.config['PASSWORD']
    admin_password = app.config['ADMIN_PASSWORD']
    # password protection
    if not (check_password_hash(admin_password, password)
            or check_password_hash(config_password, password)):
        flash("Wrong Password", "warning")
        return render_template('result.html', url=url_for("upload"))
    # commit data
    article = Article(title=title, author=name, content=content, time=date,
                      id=id)
    db.session.add(article)
    db.session.commit()
    flash("Upload Success", "success")
    return render_template('result.html', url=url_for("articles"))


@app.route('/admin-login')
def admin_login():
    session['admin'] = False
    form = AdminLoginForm()
    return render_template("admin_login.html", form=form)


@app.route('/admin', methods=['GET', 'POST'])
def admin():
    session.setdefault('admin', False)
    if not session['admin'] and 'admin_name' in request.form:
        session['input_name'] = escape(request.form['admin_name'])
        session['input_password'] = escape(request.form['password'])
        session['admin_name'] = session['input_name']
        if (session['input_name'] != 'rice'
                and session['input_name'] != 'andyzhou'):
            return redirect(url_for('admin_login'))
        if not check_password_hash(app.config['ADMIN_PASSWORD'],
                                   session['input_password']):
            print("Password Incorrect.")
            return redirect(url_for('admin_login'))
    elif not session['admin'] and 'admin_name' not in request.form:
        return redirect(url_for('admin_login'))
    session['admin'] = True
    return render_template('admin.html',
                           name=session['admin_name'].capitalize(),
                           articles=Article().query_all(),
                           )


@app.route('/admin-delete/<id>', methods=['POST'])
def admin_delete(id):
    Article().delete_by_id(id)
    flash(f"Article id {id} deleted", "success")
    return render_template("result.html", url=url_for("admin"))


@app.route('/edit/<int:id>')
def edit(id):
    session.setdefault("admin", False)
    if session['admin']:
        form = EditForm()
        content = Article().query_by_id(id).content
        return render_template("edit.html", id=id, form=form,
                               old_content=content)
    else:
        flash("Not Admin", "waring")
        return render_template('result.html', url=url_for("admin_login"))


@app.route('/edit-result/<int:id>', methods=['POST'])
def edit_result(id):
    try:
        article_content = request.form['ckeditor']
        id = id
        article = Article().query_by_id(id)
        article.content = article_content
        cursor = db.session()
        cursor.add(article)
        cursor.commit()
    except Exception as e:
        flash("Edit Failed!", "warning")
        print(e)
        return render_template('result.html', url=url_for('admin_login'))
    else:
        flash("Edit Succeeded", "success")
        return render_template("result.html", url=url_for("admin"))


@app.route('/about-zh')
def about_zh():
    return render_template("about_zh.html")


@app.route('/about')
@app.route('/about-en')
def about_en():
    return render_template("about_en.html")


@app.route('/kzkt')
def kzkt():
    return render_template('kzkt.html')


@app.errorhandler(404)
@app.route('/hrtg')
def page_not_found(e="hrtg"):
    return render_template('coffin_dance.html'), 404


@app.errorhandler(500)
def internal_server_error(e):
    return render_template('error.html',
                           error_message="500 INTERNAL SERVER ERROR"), 500


@app.errorhandler(405)
def method_not_allowed(e):
    return render_template('error.html',
                           error_message="405 METHOD NOT ALLOWED"), 405
