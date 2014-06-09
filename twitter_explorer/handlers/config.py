"""Handlers responsible for Twitter backend configuration."""

from flask import request
from flask.ext import login
from flask_wtf import Form
from wtforms import TextField
from wtforms.validators import DataRequired

from twitter_explorer.models import TwitterConfig
from twitter_explorer.utils import render_template


class ConfigForm(Form):
    token_key = TextField(validators=[DataRequired()])
    token_secret = TextField(validators=[DataRequired()])


@login.login_required
def config():
    config = None

    if request.method == 'POST':
        form = ConfigForm()
        if form.validate_on_submit():
            config = TwitterConfig.update(login.current_user,
                                          form.token_key.data,
                                          form.token_secret.data)

    if config is None:
        config = TwitterConfig.get_by_user(login.current_user)

    return render_template('config.html',
                           current_page='Twitter Configuration',
                           twitter_config=config)
