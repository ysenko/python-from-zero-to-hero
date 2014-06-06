from application import app, db, bcrypt, login_manager
from utils import render_template, user_loader
from flask.ext.login import login_required

from twitter_explorer.handlers import login


login_manager.login_view = 'login'
login_manager.user_loader(user_loader)


# Routes.
app.add_url_rule('/login', 'login', login.login, methods=['GET', 'POST'])
app.add_url_rule('/signup', 'signup', login.register, methods=['GET', 'POST'])

@login_required
def index():
    return 'Hello World'

app.add_url_rule('/', 'index', index, methods=['GET', 'POST'])

# Debug only.
if __name__ == '__main__':
    host = app.config.get('HOST', '127.0.0.1')
    port = app.config.get('PORT', 5000)
    app.run(host=host, port=port, debug=True)
