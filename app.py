import flask
import xdg
import json
import util
from typing import Optional, Dict
import os.path
import re


def build_app():
    """Build the flask app"""
    app = flask.Flask(__name__, template_folder='static/templates')
    app.data_path = os.path.join(xdg.xdg_data_home(), 'song_and_spell')

    @app.route("/")
    def index():
        words = app.list_words()
        return flask.render_template('index.html', words=words)

    @app.route("/upsert/<word>/<url>")
    def add_word(word: str, url: str):
        """Create or update a word -> song mapping"""
        local_path = app.get_path(word)
        util.download_audio(url, local_path)

    @app.route("/delete/<word>")
    def delete_word(word: str):
        """Delete a word"""
        local_path = app.get_path(word)
        os.remove(local_path)


    @app.route("/mute/")
    def mute():
        """Mute all sound devices"""
        util.mute_all()

    @app.route("/unmute/")
    def unmute():
        """Unmute all sound devices"""
        util.unmute_all()

    @app.route("/play/<word>")
    def play_song(word: str):
        """Play the song for a word"""
        local_path = app.get_path(word)
        util.play_audio(local_path)


    def init():
        os.makedirs(app.data_path, exist_ok=True)
        util.ensure_vlc()
        def get_path(word: str) -> str:
            assert  re.match('^\w+$', word), f'Word {word} is not valid'
            return os.path.join(app.data_path, word)

        app.get_path = get_path
        app.list_words = lambda :[os.path.basename(f)
                                  for f in os.listdir(app.data_path)]
        def on_press(last_n: str) -> None:
            words = app.list_words()
            try:
                longest_match = next(word 
                                for word in sorted(words, key=lambda w: len(w), reverse=True)
                                if word == last_n[- len(word):])
            except StopIteration:
                return
            local_path = app.get_path(longest_match)
            util.play_audio(local_path)

        app.key_logger = util.KeyLogger(100, on_press)
        app.key_logger.start()
    app.init = init
    return app
            
    
if __name__ == "__main__":
    app = build_app()
    app.init()
    app.run()
