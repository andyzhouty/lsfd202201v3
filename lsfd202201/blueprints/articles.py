# -*- coding:utf-8 -*-
from flask import (render_template, request, flash,
                   url_for, Blueprint, current_app)
from werkzeug.security import check_password_hash
from lsfd202201.models import Article
from lsfd202201.forms import UploadForm
from lsfd202201.extensions import db
from lsfd202201.emails import send_email

articles_bp = Blueprint("articles", __name__)


@articles_bp.route('/')
def articles():
    page = request.args.get('page', 1, int)
    all_articles = Article().query_all()
    if all_articles:
        article = Article().query_by_id(page)
        pagination = Article.query.order_by(
            Article.timestamp.desc()).paginate(page, 1)
        return render_template('articles.html',
                               this_article=article,
                               content=article.content,
                               pagination=pagination)
    flash("No Articles! Please Upload one first!", "warning")
    return render_template("result.html", url=url_for("articles.upload"))


@articles_bp.route('/upload/')
def upload():
    form = UploadForm()
    return render_template('upload.html', form=form)


@articles_bp.route('/upload-result/', methods=['POST'])
def upload_result():
    # get vars from upload page
    name = request.form['name']
    password = request.form['password']
    date = request.form['date']
    title = request.form['title']
    content = request.form['content']
    id = len(Article.query.all()) + 1
    uploader_password = current_app.config['PASSWORD']
    admin_password = current_app.config['ADMIN_PASSWORD']
    # password protection
    if not (check_password_hash(admin_password, password)
            or check_password_hash(uploader_password, password)):
        flash("Wrong Password", "warning")
        return render_template('result.html', url=url_for("articles.upload"))
    # commit data
    article = Article(
        title=title, author=name, content=content, date=date, id=id
    )
    db.session.add(article)
    db.session.commit()
    # send email to 2 admins
    email_data = {
        'title': title,
        'author': name,
        'content': content
    }
    recipents = [
        current_app.config['ADMIN_ONE_EMAIL'],
        current_app.config['ADMIN_TWO_EMAIL'],
    ]
    send_email(
        recipents=recipents,
        **email_data
    )
    flash("Upload Success", "success")
    return render_template('result.html', url=url_for("articles.articles"))
