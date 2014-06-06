import flask

from flask.ext.login import login_required

from twitter_explorer.utils import render_template


@login_required
def index():
    if flask.request.method == 'GET':
        return render_template('index.html', current_page='Main')
