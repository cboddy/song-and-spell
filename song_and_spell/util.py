import pynput.keyboard as Keyboard
import youtube_dl
from typing import Callable, Tuple, Optional, List
import subprocess
import os

mute_sh=r"""for card in $(amixer scontrols | sed "s/.* '\(.*\)',/\1/"); do amixer sset $card mute; done"""
unmute_sh=r"""for card in $(amixer scontrols | sed "s/.* '\(.*\)',/\1/"); do amixer sset $card unmute; done"""

class KeyLogger(object):
    """Log the past N key-presses"""

    def __init__(self, max_length: int, on_press: Callable[[str], None]):
        """on_press should take a string of the last max_length keys that have been pressed"""
        self.max_length = max_length
        self.index = 0
        self.pressed = [" "] * max_length
        self.on_press= on_press

    @property
    def pos(self) -> int:
        return self.index % self.max_length

    def append(self, char: str) -> None:
        self.pressed[self.pos] = char
        self.index += 1
    
    def get_last(self) -> str:
        pos = self.pos
        return "".join(self.pressed[pos:]) + "".join(self.pressed[:pos])

    def call_backs(self) -> Tuple[Callable]:
        """Build callbacks for the key-logger."""
        def on_press(key):
            # Callback for key-press
            try:
                #print(f'Appending {key.char}')
                self.append(key.char)
                self.on_press(self.get_last())
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
    'keepvideo': True
    #'logger': MyLogger(),
    #'progress_hooks': [progress_hook],
}
    
    with youtube_dl.YoutubeDL(_opts) as ydl:
        ydl.download([youtube_url])

def ensure_vlc():
    """Raise an error if VLC is not installed"""
    rc = os.system("which cvlc")
    assert rc == 0, 'VLC is not installed on the host'

def play_audio(local_path: str):
    """Play a local file with VLC"""
    subprocess.call(['cvlc', local_path])
    
def mute_amixer():
    """Mute  master speaker via alsa-mixer"""
    subprocess.call("amixer sset Master,0 mute".split())

def set_volume_amixer(volume_percentage: int) -> None:
    """Set master speaker volume via alsa-mixer"""
    assert 0 <= int(volume_percentage) <= 100, f"Volume {volume_percentage} outside the range [0,100]"
    subprocess.call("amixer sset Master,0 {volume_percentage}% unmute".split())

def main():
    download_audio('https://www.youtube.com/watch?v=BaW_jenozKc', None)
    """
    on_press, on_release = KeyLogger(10).call_backs()
    with Keyboard.Listener(on_press=on_press, on_release=on_release) as listener:
        listener.join()
    """

if __name__ == "__main__":
    main()
