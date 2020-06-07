import flask

app = flask.Flask(__name__)

# Methods
@app.route('/')
def home():

    return 'Time sent!'


@app.route('/time')
def time():
    return 'Yo!'


if __name__ == '__main__':
    app.run()
