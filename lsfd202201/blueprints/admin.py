# -*- coding:utf-8 -*-
from flask import (render_template, request, flash,
                   redirect, url_for, session, Blueprint, current_app)
from werkzeug.security import check_password_hash
from lsfd202201.models import Article
from lsfd202201.forms import AdminLoginForm, EditForm
from lsfd202201.extensions import db
from lsfd202201.utils import admin_reqired

admin_bp = Blueprint('admin', __name__)


@admin_bp.route('/login/')
def login():
    if session['admin']:
        return redirect(url_for('admin.admin'))

    session['admin'] = False
    form = AdminLoginForm()
    return render_template("admin_login.html", form=form)


@admin_bp.route('/logout/')
@admin_reqired
def logout():
    session['admin'] = False
    current_app.logger.info(f"Admin {session} logged out")
    return redirect(url_for('main.main'))


@admin_bp.route('/', methods=['GET', 'POST'])
def admin():
    session.setdefault('admin', False)
    if not session['admin']:
        if 'admin_name' in request.form:
            session['input_name'] = request.form['admin_name']
            session['input_password'] = request.form['password']
            session['admin_name'] = session['input_name']

            if (session['input_name'] != 'rice' and
                    session['input_name'] != 'andyzhou'):
                # check admin name
                return redirect(url_for('admin.login'))

            if not check_password_hash(current_app.config['ADMIN_PASSWORD'],
                                       session['input_password']):
                # check admin password
                print("Password Incorrect.")
                return redirect(url_for('admin.login'))
            current_app.logger.info(f"Admin {session['admin_name']} logged in")

        elif 'admin_name' not in request.form:
            return redirect(url_for('admin.login'))

    session['admin'] = True
    return render_template(
        'admin.html',
        name=session['admin_name'].capitalize(),
        articles=Article().query_all()
    )


@admin_bp.route('/delete/<int:id>/', methods=['POST'])
@admin_reqired
def delete(id):
    """
    A view function for administrators to delete an articles.
    """
    Article().delete_by_id(id)
    flash(f"Article id {id} deleted", "success")
    current_app.logger.info(f"Article id {id} deleted.")
    return render_template("result.html", url=url_for("admin.admin"))


@admin_bp.route('/edit/<int:id>')
@admin_reqired
def edit(id):
    form = EditForm()
    content = Article().query_by_id(id).content
    return render_template("edit.html", id=id, form=form,
                           old_content=content)


@admin_bp.route('/edit_result/<int:id>', methods=['POST'])
@admin_reqired
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
    else:
        flash("Edit Succeeded", "success")
    return render_template("result.html", url=url_for("admin.admin"))
