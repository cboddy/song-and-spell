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
* ~~delete bug~~
* ~~vlc not terminating when song finishes~~
* ~~space to stop~~
* volume-normalisation?
* ~~file-upload~~
* new systemd-service
* install script

### notes
* the pynput library requires an X server to be running. Set default resolution in `raspi-config` (anything other than default) to force the X server to start. 

### setup  bluetooth
```
# install required packages
sudo apt install bluealsa pulseaudio* bluez-tools vlc

# set display to force X-server to start
TODO
raspi-config nonint ???

# pair bluetooth
TODO

# update bluetoothd service to start  with a2dp plugin
sudo sed -i 's#ExecStart=/usr/lib/bluetooth/bluetoothd#& --plugin=a2dp#' /lib/systemd/system/bluetooth.service
# reload/restart bluetooth service
systemctl daemon-reload
systemctl restart bluetooth

# switch to the bluetooth speaker as the default speaker when it connects
echo "load-module module-switch-on-connect" >> /etc/pulse/default.pa

```
### setup
```
python3 -m venv
. bin/venv/activate
pip3 install -r requirements.txt
```
