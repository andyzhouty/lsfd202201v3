from flask import (
    session,
    request,
    current_app,
    render_template,
    flash,
    redirect,
    url_for,
    Blueprint,
)
from flask_login import current_user, login_required
from flask_login.utils import login_user, logout_user
from ..models import db, Article, Feedback, User
from ..forms import AdminLoginForm, EditForm
from ..utils import redirect_back

admin_bp = Blueprint("admin", __name__)


@admin_bp.before_request
def before_request():
    if "Mozilla" not in request.user_agent.string and not current_app.config["TESTING"]:
        return redirect(url_for("main.main"))


@admin_bp.route("/login", methods=["GET", "POST"])
def login():
    if current_user.is_authenticated:
        return redirect_back(".admin")
    form = AdminLoginForm()
    if form.validate_on_submit():
        name = form.name.data
        password = form.password.data

        user = User.query.filter_by(name=name).first()
        if user is None or not user.validate_password(password):
            flash("Invalid username or email!")
            return redirect_back(".login")
        login_user(user)
        current_app.logger.info(f"User {name} logged in")
        return redirect_back(".admin")
    return render_template("admin/admin_login.html", form=form)


@admin_bp.route("/logout")
@login_required
def logout():
    current_app.logger.info(f"User {current_user.name} logged out")
    logout_user()
    return redirect(url_for("main.main"))


@admin_bp.route("")
@login_required
def admin():
    return render_template("admin/admin.html", name=current_user.name.capitalize())


@admin_bp.route("/articles/delete/<int:id>", methods=["POST"])
@login_required
def delete_article(id):
    """
    A view function for administrators to delete an articles.
    """
    article = Article.query_by_id(id)
    article.delete()
    flash(f"Article id {id} deleted", "success")
    current_app.logger.info(f"{str(article)} deleted.")
    return render_template("result.html", url=url_for("admin.admin"))


@admin_bp.route("/articles/edit/<int:id>", methods=["GET", "POST"])
@login_required
def edit_article(id):
    form = EditForm()
    content = Article.query_by_id(id).content
    if form.validate_on_submit():
        article_content = form.content.data
        article = Article.query_by_id(id)
        article.content = article_content
        db.session.add(article)
        db.session.commit()
        flash("Edit Succeeded!")
        return redirect(url_for("admin.admin"))
    form.content.data = content
    return render_template("admin/edit.html", id=id, form=form)


@admin_bp.route("/feedbacks")
@login_required
def manage_feedback():
    return render_template("admin/feedbacks.html")


@admin_bp.route("/feedback/delete/<int:id>", methods=["POST"])
@login_required
def delete_feedback(id):
    feedback = Feedback.query_by_id(id)
    feedback.delete()
    flash(f"{str(feedback)} deleted.", "success")
    current_app.logger.info(f"Feedback id {id} deleted.")
    return render_template("result.html", url=url_for("admin.manage_feedback"))
