import flask
import logging

from flask.ext import login
from flask_wtf import Form
from wtforms import TextField
from wtforms.validators import DataRequired

from twitter_explorer.models import TwitterConfig
from twitter_explorer.twitter_backend import auth, search
from twitter_explorer.utils import render_template


class SearchForm(Form):
    search_query = TextField('search_query', validators=[DataRequired()])


@login.login_required
def index():
    search_results = []
    search_query = None

    if flask.request.method == 'POST':
        form = SearchForm()
        if not form.validate_on_submit():
            # Form is not valid, just return to edit page.
            return render_template('index.html', current_page='Main',
                                   search_results=search_results,
                                   search_query=search_query)

        search_query = form.search_query.data

        app_key = flask.current_app.config.get('TWITTER_TOKEN_KEY', '')
        app_secret = flask.current_app.config.get('TWITTER_TOKEN_SECRET', '')
        twitter_conf = TwitterConfig.get_by_user(login.current_user)

        if twitter_conf is None:
            logging.warn('Cannot get twitter config for %s' %
                         login.current_user)
            return flask.redirect(flask.url_for('config'))

        twitter_api = auth.get_authorized_api(twitter_conf.token_key,
                                              twitter_conf.token_secret,
                                              app_key,
                                              app_secret)
        if twitter_api is None:
            logging.warn('Cannot get authorized twitter API for %s' %
                         login.current_user)
            return flask.redirect(flask.url_for('config'))

        search_results = search.search(
            twitter_api,
            search_query,
            count=flask.current_app.config.get('TWEETS_IN_RESULT', 50))

    return render_template('index.html', current_page='Main',
                           search_results=search_results,
                           search_query=search_query)
