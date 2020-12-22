import pynput.keyboard as Keyboard
import youtube_dl
from typing import Callable, Tuple, Optional
import subprocess
import os

mute_sh=r"""for card in $(amixer scontrols | sed "s/.* '\(.*\)',/\1/"); do amixer sset $card mute; done"""
unmute_sh=r"""for card in $(amixer scontrols | sed "s/.* '\(.*\)',/\1/"); do amixer sset $card unmute; done"""

class KeyLogger(object):
    """Log the past N key-presses"""

    def __init__(self, max_length: int = 100):
        self.max_length = max_length
        self.index = 0
        self.pressed = [" "] * max_length

    @property
    def pos(self) -> int:
        return self.index % self.max_length

    def append(self, char: str) -> None:
        self.pressed[self.pos] = char
        self.index += 1

    def get_last(self, n: int) -> str:
        pos = self.pos
        if pos < n:
            left = n + pos - 1
            right = pos
            return "".join(self.pressed[left:]) + "".join(self.pressed[:right])
        return "".join(self.pressed[:n])

    def call_backs(self) -> Tuple[Callable]:
        """Build callbacks for the key-logger."""

        def on_press(key):
            # Callback for  key-press
            try:
                char = key.char
                self.append(char)
            except AttributeError:
                # special key press
                pass

        def on_release(key):
            pass

        return on_press, on_release

    def start(self):
        """Start a keyboard listener"""
        on_press, on_release = self.call_backs()
        listener = Keyboard.Listener(on_press=on_press, on_release=on_release)
        listener.start()


def download_audio(youtube_url: str, local_path: str, progress_hook: Optional[Callable]=None) -> None:
    """Download a youtube link as an audio file and store it  locally"""
    _opts = {
    'outtmpl': local_path,
    'format': 'bestaudio/best',
    'postprocessors': [{
        'key': 'FFmpegExtractAudio',
        'preferredcodec': 'mp3',
        'preferredquality': '192',
        
    }],
    #'logger': MyLogger(),
    'progress_hooks': [progress_hook],
}
    
    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
        ydl.download([youtube_url])

def ensure_vlc():
    """Raise an error if VLC is not installed"""
    rc = os.system("which cvlc")
    assert rc == 0, 'VLC is not installed on the host'

def play_audio(local_path: str):
    """Play a local file with VLC"""
    subprocess.call(['cvlc', local_path])
    
def mute_all():
    subprocess.call(mute_sh, shell=True)

def unmute_all():
    subprocess.call(unmute_sh, shell=True)

def main():
    download_audio('https://www.youtube.com/watch?v=BaW_jenozKc', None)
    """
    on_press, on_release = KeyLogger(10).call_backs()
    with Keyboard.Listener(on_press=on_press, on_release=on_release) as listener:
        listener.join()
    """

if __name__ == "__main__":
    main()
