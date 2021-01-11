import flask
import xdg
import json
import song_and_spell.util as util
from typing import Optional, Dict
import os.path
import re
import sys
import logging


def build_app():
    """Build the flask app"""
    app = flask.Flask(__name__, template_folder='static/templates')

    @app.route("/")
    def index():
        words = app.list_words()
        volume_perc = util.get_volume_percent_amixer()
        return flask.render_template('index.html', words=words, volume_perc=volume_perc)

    @app.route("/add_word", methods=['POST', 'GET'])
    def add_word():
        """Create or update a word -> song mapping"""
        if flask.request.method == 'POST':
            word = flask.request.form['word'].lower().strip()
            local_path = app.get_path(word)
            def upload_file():
                try:
                    flask.request.files['uploadFile'].save(local_path)
                    flask.flash(f'Successfully uploaded song for {word}.')
                except:
                    flask.flash(f'Failed to upload song for {word}.')
                    raise
            def get_from_youtube():
                url = flask.request.form['ytLink']
                try:
                    util.download_audio(url, local_path)
                    flask.flash(f'Successfully downloaded song for {word}.')
                    app.logger.info(f"Successfully added word {word} to local path {local_path} from link {url}")
                except: 
                    flask.flash(f'Failed to download song for {word}.')
                    app.logger.exception(f"Failed to add word {word} to local path {local_path} from link {url}")
                    raise
            uploadFile = flask.request.files.get('uploadFile')
            if uploadFile and uploadFile.content_length > 0:
                upload_file()
            else:
                get_from_youtube()
            return flask.redirect(flask.url_for('index'))
        else:
            volume_perc = util.get_volume_percent_amixer()
            return flask.render_template('add_word.html', volume_perc=volume_perc)

    @app.route("/delete/<word>")
    def delete_word(word: str):
        """Delete a word"""
        local_path = app.get_path(word)
        os.remove(local_path)
        flask.flash(f'Deleted the song for word {word}.')
        return flask.redirect(flask.url_for('index'))


    @app.route("/mute/")
    def mute():
        util.mute_amixer()
        flask.flash(f'Speaker muted - use slider to un-mute.')
        return flask.redirect(flask.url_for('index'))
        

    @app.route("/set_volume", methods=['POST'])
    def set_volume():
        volume_perc = int(flask.request.form['volume_perc'])
        util.set_volume_amixer(volume_perc)
        flask.flash(f'Volume set to {volume_perc}%')
        return flask.redirect(flask.url_for('index'))

    @app.route("/play/<word>")
    def play_song(word: str):
        """Play the song for a word"""
        local_path = app.get_path(word)
        app.logger.info(f"Playing word from web-ui {word}")
        util.play_audio(local_path)
        return flask.redirect(flask.url_for('index'))

    def init():
        app.data_path = os.path.join(xdg.xdg_data_home(), 'song_and_spell')
        os.makedirs(app.data_path, exist_ok=True)
        util.ensure_vlc()
        valid_word = "^\w+$"
        def get_path(word: str) -> str:
            assert  re.match(valid_word, word), f'Word {word} is not valid'
            return os.path.join(app.data_path, word)

        def on_press(last_n: str) -> None:
            last_n = last_n.lower()
            words = app.list_words()
            try:
                longest_match = next(word 
                                for word in sorted(words, key=lambda w: len(w), reverse=True)
                                if word == last_n[- len(word):])
            except StopIteration:
                return
            local_path = app.get_path(longest_match)
            app.logger.info(f"Playing word {longest_match}")
            util.play_audio(local_path)
        app.get_path = get_path
        app.list_words = lambda: [os.path.basename(f)
                                  for f in os.listdir(app.data_path)
                                  if re.match(valid_word, f)]
        app.logger.info("starting keylogger")
        util.KeyLogger(100, on_press, on_space=lambda: util.stop_all_vlc()).start()
        app.secret_key= os.urandom(24) # for flask.flash
    app.init = init
    return app
            
def main(): 
    logging.basicConfig(stream=sys.stdout, level=logging.INFO)
    app = build_app()
    app.init()
    app.run(host="0.0.0.0")

if __name__ == "__main__":
    main()
