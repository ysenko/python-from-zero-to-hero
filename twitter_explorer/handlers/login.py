"""Handlers responsible for login and authentication."""

from flask import request, url_for, redirect
from flask.ext.login import login_user, login_required, logout_user
from flask_wtf import Form
from wtforms import TextField, PasswordField
from wtforms.validators import DataRequired, Email

from twitter_explorer.models import User
from twitter_explorer.utils import render_template


class LoginForm(Form):
    email = TextField('email', validators=[Email()])
    password = PasswordField('password', validators=[DataRequired()])


class SignUpForm(Form):
    email = TextField('email', validators=[Email()])
    password = PasswordField('password', validators=[DataRequired()])
    fullname = TextField('fullname', validators=[DataRequired()])


def login():
    """Show login page or login user into the system."""
    form = LoginForm()
    if request.method == 'GET' or not form.validate_on_submit():
        return render_template(
            'login.html',
            registration_page=url_for('signup')
        )

    user = User.get_by_email(form.email.data)
    if user is not None and user.check_password(form.password.data):
        login_user(user)
        return redirect('/')
    else:
        return render_template(
            'login.html',
            registration_page=url_for('signup')
        )


@login_required
def logout():
    logout_user()
    return redirect('login')


def register():
    """Registration page."""
    form = SignUpForm()

    if request.method == 'GET' or not form.validate_on_submit():
        return render_template('register.html')

    User.register(
        form.fullname.data,
        form.email.data,
        form.password.data
    )
    return redirect(url_for('login'))
