# -*- coding:utf-8 -*-
from flask import (render_template, request, flash,
                   redirect, url_for, session, Blueprint, current_app)
from ..models import db, Article, Comment
from ..forms import AdminLoginForm, EditForm
from ..utils import admin_required, check_admin_login

admin_bp = Blueprint('admin', __name__)


@admin_bp.before_app_first_request
def before_app_first_request():
    session.setdefault('admin', False)


@admin_bp.before_request
def before_request():
    if ('Mozilla' not in request.user_agent.string and
            not current_app.config['TESTING']):
        print(request.user_agent.string)
        return redirect(url_for('main.main'))


@admin_bp.route('/login/')
def login():
    if session['admin']:
        return redirect(url_for('admin.admin'))

    session['admin'] = False
    form = AdminLoginForm()
    return render_template("admin/admin_login.html", form=form)


@admin_bp.route('/logout/')
@admin_required
def logout():
    current_app.logger.info(f"Admin {session['admin_name']} logged out")
    return redirect(url_for('main.main'))


@admin_bp.route('/', methods=['GET', 'POST'])
@admin_bp.route('/articles/', methods=['GET', 'POST'])
def admin():
    if not session['admin']:
        if request.method.lower() != 'post':
            return redirect(url_for('admin.login'))
        input_name = request.form['name']
        input_password = request.form['password']

        if not check_admin_login(input_password, input_name):
            return redirect(url_for('admin.login'))
        session['admin_name'] = input_name
        current_app.logger.info(f"Admin {session['admin_name']} logged in")

    session['admin'] = True
    return render_template(
        'admin/admin.html',
        name=session['admin_name'].capitalize(),
        articles=Article.query.all()
    )


@admin_bp.route('/articles/delete/<int:id>/', methods=['POST'])
@admin_required
def delete_article(id):
    """
    A view function for administrators to delete an articles.
    """
    article = Article().query_by_id(id)
    article.delete()
    flash(f"Article id {id} deleted", "success")
    current_app.logger.info(f"{str(article)} deleted.")
    return render_template("result.html", url=url_for("admin.admin"))


@admin_bp.route('/articles/edit/<int:id>')
@admin_required
def edit_article(id):
    form = EditForm()
    content = Article().query_by_id(id).content
    return render_template("admin/edit.html", id=id, form=form, old_content=content)


@admin_bp.route('/articles/edit_result/<int:id>', methods=['POST'])
@admin_required
def article_edit_result(id):
    try:
        article_content = request.form['ckeditor']
        id = id
        article = Article().query_by_id(id)
        article.content = article_content
        db.session.add(article)
        db.session.commit()
    except Exception as e:
        flash("Edit Failed!", "warning")
        print(e)
    else:
        flash("Edit Succeeded!", "success")
    return render_template("result.html", url=url_for("admin.admin"))


@admin_bp.route('/comments/')
@admin_required
def manage_comments():
    return render_template("admin/comments.html", comments=Comment().query.all())


@admin_bp.route('/comments/delete/<int:id>', methods=['POST'])
@admin_required
def delete_comment(id):
    comment = Comment().query_by_id(id)
    comment.delete()
    flash(f"{str(comment)} deleted.", "success")
    current_app.logger.info(f"Comment id {id} deleted.")
    return render_template("result.html", url=url_for("admin.manage_comments"))
