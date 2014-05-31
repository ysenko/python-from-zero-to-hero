from application import app


@app.route('/')
def index():
    return 'Hello World!'


# Debug only.
if __name__ == '__main__':
    app.run()
