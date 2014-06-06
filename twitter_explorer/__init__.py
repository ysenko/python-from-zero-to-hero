from application import app, db, bcrypt, login_manager
from utils import render_template, user_loader

from twitter_explorer.handlers import login, index


login_manager.login_view = 'login'
login_manager.user_loader(user_loader)


# Routes.
app.add_url_rule('/login', 'login', login.login, methods=['GET', 'POST'])
app.add_url_rule('/signup', 'signup', login.register, methods=['GET', 'POST'])
app.add_url_rule('/logout', 'logout', login.logout, methods=['GET'])
app.add_url_rule('/', 'index', index.index, methods=['GET'])


# Debug only.
if __name__ == '__main__':
    host = app.config.get('HOST', '127.0.0.1')
    port = app.config.get('PORT', 5000)
    app.run(host=host, port=port, debug=True)
