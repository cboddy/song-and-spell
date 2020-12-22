import flask
import xdg
import os
import json
import util
from typing import Optional, Dict
import os.path


def build_app():
    """Build the flask app"""
    app = flask.Flask(__name__, template_folder='static/templates')
    app.data_path = os.path.join(xdg.xdg_data_home(), 'song_and_spell')
    app.config_path = os.path.join(xdg.xdg_config_home(), 'song_and_spell', "config.json")

    @app.route("/")
    def index():
        return flask.render_template('index.html', word_to_path=app.word_to_path)

    @app.route("/upsert/<word>/<url>")
    def add_word(word: str, url: str):
        """Create or update a word -> song mapping"""
        util.download_audio(url,

    @app.route("/delete/<word>")
    def delete_word(word: str):
        """Delete a word"""
        app.word_to_path.delete(word)

    @app.route("/mute/")
    def mute():
        """Mute all sound devices"""
        util.mute_all()

    @app.route("/unmute/")
    def mute():
        """Unmute all sound devices"""
        util.unmute_all()

    @app.route("/play/<word>")
    def play_song(word: str):
        """Play the song for a word"""
        util.play_audio(app.word_to_path.get_path(word))


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

    def ensure_vlc():
        """Raise an error if VLC is not installed"""
        rc = os.system("which cvlc")
        if rc != 0:
            raise ValueError('VLC is not installed on the host')

    def init():
        os.makedirs(os.path.dirname(app.config_path), exist_ok=True)
        os.makedirs(app.data_path, exist_ok=True)
        app.key_logger = util.KeyLogger(100)
        try:
            word_to_path = load_config()
        except FileNotFoundError:
            app.word_to_path = {}
        validate_config(word_to_path)
        app.word_to_path = Words(word_to_path) 
        app.key_logger.start()
    ensure_vlc()
    app.init = init
    app.save_config = save_config

    return app
            
    
if __name__ == "__main__":
    app = build_app()
    app.init()
    app.run()
