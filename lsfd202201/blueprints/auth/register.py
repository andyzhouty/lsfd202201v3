from flask import render_template
from lsfd202201.models import Creator, User
from . import auth_bp


@auth_bp.route('/register-index/')
def register_index():
    return render_template('auth/register_index.html')


@auth_bp.route('/register-creator', methods=['GET', 'POST'])
def register_creator():
    new_creator = Creator(
        name=form.name.data
    )