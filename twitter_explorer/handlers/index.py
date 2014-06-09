import flask

from flask.ext.login import login_required
from flask_wtf import Form
from wtforms import TextField
from wtforms.validators import DataRequired

from twitter_explorer.twitter_backend import auth
from twitter_explorer.utils import render_template


class SearchForm(Form):
    search_query = TextField('search_query', validators=[DataRequired()])

@login_required
def index():
    search_results = []
    search_query = None

    if flask.request.method == 'POST':
        pass

    return render_template('index.html', current_page='Main',
                            search_results=search_results,
                            search_query=search_query)
