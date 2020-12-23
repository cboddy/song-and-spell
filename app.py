import flask
import xdg
import json
import util
from typing import Optional, Dict
import os.path
import re

VALID_WORD = "^\w+$"

def build_app():
    """Build the flask app"""
    app = flask.Flask(__name__, template_folder='static/templates')
    app.data_path = os.path.join(xdg.xdg_data_home(), 'song_and_spell')

    @app.route("/")
    def index():
        words = app.list_words()
        return flask.render_template('index.html', words=words)

    @app.route("/add_word", methods=['POST', 'GET'])
    def add_word():
        """Create or update a word -> song mapping"""
        if flask.request.method == 'POST':
            word = flask.request.form['word']
            url = flask.request.form['ytLink']
            local_path = app.get_path(word)
            app.logger.info(f'Adding word {word} with url {url}')
            try:
                util.download_audio(url, local_path)
                flask.flash(f'Successfully downloaded song for {word}.')
            except: 
                flask.flash(f'Failed to download song for {word}.')
            return flask.redirect(flask.url_for('index'))
        else:
            return flask.render_template('add_word.html')

    @app.route("/delete/<word>")
    def delete_word(word: str):
        """Delete a word"""
        local_path = app.get_path(word)
        os.remove(local_path)
        flask.flash(f'Deleted the song for word {word}.')


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
            assert  re.match(VALID_WORD, word), f'Word {word} is not valid'
            return os.path.join(app.data_path, word)

        app.get_path = get_path
        app.list_words = lambda :[os.path.basename(f)
                                  for f in os.listdir(app.data_path)
                                  if re.match(VALID_WORD, f)]
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
        #app.debug = True
        app.secret_key= os.urandom(24) # for flask.flash
    app.init = init
    return app
            
def main(): 
    app = build_app()
    app.init()
    app.run(host="0.0.0.0")

if __name__ == "__main__":
    main()
