# -*- coding:utf-8 -*-
from flask import (render_template, request, flash,
                   url_for, Blueprint, current_app)
from werkzeug.security import check_password_hash
from ..models import Article
from ..forms import UploadForm
from ..extensions import db
from ..emails import send_email

articles_bp = Blueprint("articles", __name__)


@articles_bp.route('/')
def articles():
    page = request.args.get('page', 1, int)
    all_articles = Article().query_all()
    if all_articles:
        article = Article().query_by_id(page)
        pagination = Article.query.order_by(
            Article.timestamp.desc()).paginate(page, 1)
        return render_template('articles/articles.html',
                               this_article=article,
                               content=article.content,
                               pagination=pagination)
    flash("No Articles! Please Upload one first!", "warning")
    return render_template("result.html", url=url_for("articles.upload"))


@articles_bp.route('/upload/')
def upload():
    form = UploadForm()
    return render_template('articles/upload.html', form=form)


@articles_bp.route('/upload-result/', methods=['POST'])
def upload_result():
    # get values from upload page
    name = request.form['name']
    password = request.form['password']
    date = request.form['date']
    title = request.form['title']
    content = request.form['content']
    uploader_password = current_app.config['PASSWORD']
    admin_password = current_app.config['ADMIN_PASSWORD']
    # password protection
    if not (check_password_hash(admin_password, password)
            or check_password_hash(uploader_password, password)):
        flash("Wrong Password", "warning")
        return render_template('result.html', url=url_for("articles.upload"))
    # commit data
    current_app.logger.info("The article was ready to commit.")
    article = Article(
        title=title, author=name, content=content, date=date
    )
    db.session.add(article)
    db.session.commit()
    # send email to 2 admins
    if current_app.config['EMAIL_ADMIN']:
        email_data = {
            'title': title,
            'author': name,
            'content': content
        }
        recipents = current_app.config['ADMIN_EMAIL_LIST']
        send_email(
            recipents=recipents,
            subject="A new article was added just now!",
            template="articles/article_notifaction",
            **email_data
        )
    flash("Upload Success", "success")
    return render_template('result.html', url=url_for("articles.articles"))
