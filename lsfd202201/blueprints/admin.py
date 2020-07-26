# -*- coding:utf-8 -*-
from flask import (render_template, request, flash,
                   escape, redirect, url_for, session, Blueprint, current_app)
from werkzeug.security import check_password_hash
from lsfd202201.models import Article
from lsfd202201.forms import AdminLoginForm, EditForm
from lsfd202201.extensions import db

admin_bp = Blueprint('admin', __name__)


@admin_bp.route('/login')
def admin_login():
    session['admin'] = False
    form = AdminLoginForm()
    return render_template("admin_login.html", form=form)


@admin_bp.route('', methods=['GET', 'POST'])
def admin():
    session.setdefault('admin', False)
    if not session['admin'] and 'admin_name' in request.form:
        session['input_name'] = escape(request.form['admin_name'])
        session['input_password'] = escape(request.form['password'])
        session['admin_name'] = session['input_name']
        if (session['input_name'] != 'rice'
                and session['input_name'] != 'andyzhou'):
            return redirect(url_for('admin_login'))
        if not check_password_hash(current_app.config['ADMIN_PASSWORD'],
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


@admin_bp.route('/delete/<id>', methods=['POST'])
def admin_delete(id):
    Article().delete_by_id(id)
    flash(f"Article id {id} deleted", "success")
    return render_template("result.html", url=url_for("admin"))


@admin_bp.route('/edit/<int:id>')
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


@admin_bp.route('/edit_result')
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
