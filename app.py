import flask
import xdg
import os
import json
from keylogger import KeyLogger
from typing import Optional, Dict
import os.path


def build_app():
    """Build the flask app"""
    app = flask.Flask(__name__, template_folder='static/templates')
    app.data_path = os.path.join(xdg.xdg_data_home(), 'song_and_spell')
    app.config_path = os.path.join(xdg.xdg_config_home(), 'song_and_spell', "config.json")

    @app.route("/")
    def index():
        return flask.render_template('index.html')

    def load_config() -> Dict[str,str]:
        """Loads the config file"""
        with open(app.config_path) as f:
            return json.load(f)

    def validate_config(word_to_path: Dict[str,str]):
        """Raise an error if any of the files do not exist"""
        assert isinstance(word_to_path, dict), 'Expected key-value dict, found {word_to_path}'
        for word, path in word_to_path.items():
            assert isinstance(word, str), f"{word} is not a string"
            assert os.path.exists(path), f"{path} does not exist - expected local file-path" 

    def save_config():
        with open(self.config_path, "w") as f:
            json.dump(self.word_to_path, f)

    def init():
        os.makedirs(os.path.dirname(app.config_path), exist_ok=True)
        os.makedirs(app.data_path, exist_ok=True)
        app.key_logger = KeyLogger(100)
        try:
            app.word_to_path = load_config()
        except FileNotFoundError:
            app.word_to_path = {}
        validate_config(app.word_to_path)
        app.key_logger.start()
    app.init = init
    app.save_config = save_config

    return app
            
    
if __name__ == "__main__":
    app = build_app()
    app.init()
    app.run()
