# -*- coding:utf-8 -*-
from flask import (render_template, request, flash,
                   redirect, url_for, session, Blueprint, current_app)
from werkzeug.security import check_password_hash
from ..models import db, Article, Comment
from ..forms import AdminLoginForm, EditForm
from ..utils import admin_reqired

admin_bp = Blueprint('admin', __name__)


@admin_bp.route('/login/')
def login():
    session.setdefault('admin', False)
    if session['admin']:
        return redirect(url_for('admin.admin'))

    session['admin'] = False
    form = AdminLoginForm()
    return render_template("admin/admin_login.html", form=form)


@admin_bp.route('/logout/')
@admin_reqired
def logout():
    session['admin'] = False
    current_app.logger.info(f"Admin {session['admin_name']} logged out")
    return redirect(url_for('main.main'))


@admin_bp.route('/', methods=['GET', 'POST'])
@admin_bp.route('/articles/', methods=['GET', 'POST'])
def admin():
    session.setdefault('admin', False)
    if not session['admin']:
        if 'admin_name' in request.form:
            session['input_name'] = request.form['admin_name']
            input_password = request.form['password']
            session['admin_name'] = session['input_name']

            if (session['input_name'] != 'rice' and
                    session['input_name'] != 'andyzhou'):
                # check admin name
                return redirect(url_for('admin.login'))

            if not check_password_hash(current_app.config['ADMIN_PASSWORD'],
                                       input_password):
                # check admin password
                print("Password Incorrect.")
                return redirect(url_for('admin.login'))
            current_app.logger.info(f"Admin {session['admin_name']} logged in")

        elif 'admin_name' not in request.form:
            return redirect(url_for('admin.login'))

    session['admin'] = True
    return render_template(
        'admin/admin.html',
        name=session['admin_name'].capitalize(),
        articles=Article().query_all()
    )


@admin_bp.route('/articles/delete/<int:id>/', methods=['POST'])
@admin_reqired
def delete_article(id):
    """
    A view function for administrators to delete an articles.
    """
    article = Article().query_by_id(id)
    Article().delete_by_id(id)
    flash(f"Article id {id} deleted", "success")
    current_app.logger.info(f"{str(article)} deleted.")
    return render_template("result.html", url=url_for("admin.admin"))


@admin_bp.route('/articles/edit/<int:id>')
@admin_reqired
def edit_article(id):
    form = EditForm()
    content = Article().query_by_id(id).content
    return render_template("admin/edit.html", id=id, form=form,
                           old_content=content)


@admin_bp.route('/articles/edit_result/<int:id>', methods=['POST'])
@admin_reqired
def article_edit_result(id):
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
    else:
        flash("Edit Succeeded!", "success")
    return render_template("result.html", url=url_for("admin.admin"))


@admin_bp.route('/comments/')
@admin_reqired
def manage_comments():
    comments = Comment().query_all()
    return render_template("admin/comments.html", comments=comments)


@admin_bp.route('/comments/delete/<int:id>', methods=['POST'])
@admin_reqired
def delete_comment(id):
    comment = Comment().query_by_id(id)
    Comment().delete_by_id(id)
    flash(f"{str(comment)} deleted.", "success")
    current_app.logger.info(f"Comment id {id} deleted.")
    return render_template("result.html", url=url_for("admin.manage_comments"))
