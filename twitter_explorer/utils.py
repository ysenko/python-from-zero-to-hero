"""Set of utilities."""

from flask import render_template as flask_render_template, url_for
from flask.ext import login

from twitter_explorer import models


def render_template(template, *args, **kwargs):
    kwargs.setdefault('page_title', 'TwitterExplorer v0.1')
    kwargs.setdefault('bootstrap_path',
                      url_for('static', filename='bootstrap-3.1.1-dist'))
    kwargs.setdefault('logout_page', url_for('logout'))
    kwargs.setdefault('current_user', login.current_user)

    return flask_render_template(template, *args, **kwargs)


def user_loader(email_addr):
    return models.User.get_by_email(email_addr)
