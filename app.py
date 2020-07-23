# -*- coding:utf-8 -*-
import os
from flask import (render_template, request, flash,
                   escape, redirect, url_for, session)
from werkzeug.security import check_password_hash
from markdown import markdown
from . import app, db
from .functions import escape_quotes
from .models import Article
from .forms import UploadForm, AdminLoginForm, AdminDeleteForm, EditForm


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
def articles():
    # Query data from data.sqlite
    if "page" in request.args:
        page = int(request.args["page"])
    else:
        page = 1
    all_articles = Article().query_all()
    if all_articles:
        article = Article().query_one(page)
        pagination = Article.query.order_by(Article.timestamp.desc()).paginate(page, 1)
        return render_template('articles.html', warning=True,
                               this_article=article,
                               content=markdown(article["content"]),
                               pagination=pagination)
    flash("No Articles! Please Upload one first!", "warning")
    return render_template("result.html", url=url_for("upload"))


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
    date = escape(request.form['date'])
    title = escape(request.form['title'])
    content = request.form['pagedown']
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
    form = AdminDeleteForm()
    return render_template('admin.html', warning=False,
                           name=session['admin_name'].capitalize(),
                           articles=Article().query_all(),
                           form=form)


@app.route('/admin-delete', methods=['POST'])
def admin_delete():
    article_id_to_del = request.form['id']
    test_article = Article()
    exist = test_article.query_by_id(article_id_to_del)
    if exist:
        Article().delete_by_id(article_id_to_del)
        flash(f"Article id {article_id_to_del} deleted", "info")
    else:
        flash(f"Article id {article_id_to_del} not found.", "warning")
    return render_template("result.html", url=url_for("admin"))


@app.route('/edit/<int:id>')
def edit(id):
    session.setdefault("admin", False)
    if session['admin']:
        form = EditForm()
        return render_template("edit.html", id=id, form=form,
                               content=escape_quotes(
                                   Article().query_by_id(id).content
                               ))
    else:
        flash("Not Admin", "waring")
        return render_template('result.html', url=url_for("admin_login"))


@app.route('/edit-result/<int:id>', methods=['POST'])
def edit_result(id):
    try:
        article_content = request.form['pagedown']
        id = id
        article = Article().query_by_id(id)
        article.content = article_content
        cursor = db.session()
        cursor.add(article)
        cursor.commit()
    except:
        flash("Edit Failed!", "warning")
        return render_template('result.html', url=url_for('admin_login'))
    else:
        flash("Edit Succeeded", "success")
        return render_template("result.html", url=url_for("admin"))


@app.route('/about-zh')
def readme_zh():
    return render_template("readme_zh.html")


@app.route('/about')
@app.route('/about-en')
def readme_en():
    return render_template("readme_en.html")


@app.route('/kzkt')
def kzkt():
    return render_template('kzkt.html', warning=True)


@app.errorhandler(404)
@app.route('/hrtg')
def page_not_found(e="hrtg"):
    return render_template('coffin_dance.html', warning=False), 404


@app.errorhandler(500)
def internal_server_error(e):
    return render_template('error.html', warning=False,
                           error_message="500 INTERNAL SERVER ERROR"), 500


@app.errorhandler(405)
def method_not_allowed(e):
    return render_template('error.html', warning=False,
                           error_message="405 METHOD NOT ALLOWED"), 405
