from application import app
from utils import render_template


@app.route('/')
def index():
    return render_template('base.html')


# Debug only.
if __name__ == '__main__':
    # Flask test server ignores HOST and port for security reason.
    host = app.config.get('HOST', '127.0.0.1')
    port = app.config.get('PORT', 5000)
    app.run(host=host, port=port, )
