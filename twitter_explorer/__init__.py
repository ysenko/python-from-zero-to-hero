import functools

from flask import render_template as flask_render_template, url_for

from application import app


def render_template(template, *args, **kwargs):
    kwargs.setdefault('title', 'Twitterxplorer v0.1')
    kwargs.setdefault('bootstrap_path', url_for('static',
                                                filename='bootstrap-3.1.1-dist'))

    print 'PATH', kwargs['bootstrap_path']
    return flask_render_template(template, *args, **kwargs)


@app.route('/')
def index():
    return render_template('base.html')


# Debug only.
if __name__ == '__main__':
    # Flask test server ignores HOST and port for security reason.
    host = app.config.get('HOST', '127.0.0.1')
    port = app.config.get('PORT', 5000)
    app.run(host=host, port=port, )
