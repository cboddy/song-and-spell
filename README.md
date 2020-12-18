# song-and-spell

### tl;dr

A key-logger that triggers playing an audio track when a sequence of keys are pressed and  a web-app to configure the words and songs.


### todo 

* key-logger
* flask-web-app
    * list of words and files/links
      * remove word/file
    * form add word/link 
      * youtube-dl the link and store as mp3 locally.
    * sqlite or folder/json file for storage
* systemd service to:
    * run on start-up
    * restart on error
* bash script to deploy (ideally to an [rpi-400]https://www.raspberrypi.org/products/raspberry-pi-400/)

### setup
```
python3 -m venv
. bin/venv/activate
pip3 install -r requirements.txt
```
