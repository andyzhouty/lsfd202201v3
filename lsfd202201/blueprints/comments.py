from ..emails import send_email
from ..models import Comment, db
from ..forms import CommentForm
from flask import (Blueprint, flash, redirect, render_template,
                   url_for, current_app)

comment_bp = Blueprint('comments', __name__)


@comment_bp.route('/', methods=['GET', 'POST'])
def comment():
    form = CommentForm()
    if form.validate_on_submit():
        author = form.name.data
        body = form.body.data
        message = Comment(body=body, author=author)
        db.session.add(message)
        db.session.commit()
        recipients = current_app.config['ADMIN_EMAIL_LIST']
        send_email(
            recipients=recipients,
            subject="A new comment was added!",
            template="comments/comment_notification",
            **dict(author=author, content=body)
        )
        flash('Your idea has been sent to the admins!')
    comments = Comment.query.order_by(Comment.timestamp.desc()).all()
    return render_template('comments/comments.html', form=form, comments=comments)  # noqa
