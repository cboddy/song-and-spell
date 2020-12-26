# song-and-spell

### tl;dr

A key-logger that triggers playing an audio track when a sequence of keys are pressed and  a web-app to configure the words and songs.

Requires VLC to be installed on the host and an X server to be running.

![](https://github.com/cboddy/song-and-spell/blob/master/images/song_and_spell_webui.png)

### install on raspberry-pi 400

##### With a screen attached
We need to force the  X-server to start when the HDMI cable is not plugged in (for the pynput key-logger). The easiest way I found is to run `sudo raspi-config`, then select Advanced, Screen and pick any screen resolution except for the default one.

Pair, trust and connect your bluetooth speaker. There are many guides for this,  [here is one](https://raspberrydiy.com/connect-raspberry-pi-bluetooth-speaker/).

To install the app, add a systemd-service so that it starts on start-up  and make some other changes so that it can headlessly connect to a bluetooth speaker, download and install the [install script](/scripts/install_rpi.sh) on your raspberry-pi 400. In a terminal:

*Note: this script will only work on a raspberry-pi (or any debian-derived OS with a bluetooth transciever and a normal user `pi` that is in the audio and bluetooth groups).*

```
curl -L https://github.com/cboddy/song-and-spell/blob/master/scripts/install_rpi.sh | sudo bash 
```

Note: this will restart your raspberry-pi. Turn on your speaker and it should automatically connect and go to the web-ui running on port 5000.


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
* ~~file-upload~~
* ~~new systemd-service~~
* ~~install script~~
* volume-normalisation?

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

### development
```
python3 -m venv
. bin/venv/activate
python3 setup.py develop
```
