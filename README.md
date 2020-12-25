# song-and-spell

### tl;dr

A key-logger that triggers playing an audio track when a sequence of keys are pressed and  a web-app to configure the words and songs.

Requires VLC to be installed on the host and an X server to be running.

### todo 

* ~~key-logger~~
* ~~youtube-dl the link and store as mp3 locally.~~
* ~~flask-web-app~~
    * ~~list of words and files/links~~
    * ~~mute~~
    * ~~upload file~~
      * ~~remove word/file~~
    * ~~form add word/link ~~
* ~~systemd service to:~~
    * ~~run on start-up~~
    * ~~restart on error~~
* bash script to deploy (ideally to an [rpi-400]https://www.raspberrypi.org/products/raspberry-pi-400/)

### notes
* the pynput library requires an X server to be running. Set default resolution in `raspi-config` (anything other than default) to force the X server to start. 
### setup
```
python3 -m venv
. bin/venv/activate
pip3 install -r requirements.txt
```
