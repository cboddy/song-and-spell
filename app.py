import flask
from keylogger import KeyLogger


def build_app():
    """Build the flask app"""
    app = flask.Flask(__name__, template_folder='static/templates')
    app.key_logger = KeyLogger(100)

    @app.route("/")
    def index():
        return flask.render_template('index.html')

    return app


if __name__ == "__main__":
    app = build_app()
    app.key_logger.start()
    app.run()
