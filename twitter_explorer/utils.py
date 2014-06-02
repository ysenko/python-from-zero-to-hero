"""Set of utilities."""

from flask import render_template as flask_render_template, url_for


def render_template(template, *args, **kwargs):
    kwargs.setdefault('page_title', 'TwitterExplorer v0.1')
    kwargs.setdefault('bootstrap_path',
                      url_for('static', filename='bootstrap-3.1.1-dist'))

    return flask_render_template(template, *args, **kwargs)
