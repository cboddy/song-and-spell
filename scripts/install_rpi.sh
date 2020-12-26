#!/bin/bash
# install required packages
sudo apt install -y bluealsa pulseaudio* bluez-tools vlc pip3

# update bluetoothd service to start  with a2dp plugin
sudo sed -i 's#ExecStart=/usr/lib/bluetooth/bluetoothd#& --plugin=a2dp#' /lib/systemd/system/bluetooth.service
# reload/restart bluetooth service
systemctl daemon-reload
systemctl restart bluetooth

# switch to the bluetooth speaker as the default speaker when it connects
echo "load-module module-switch-on-connect" >> /etc/pulse/default.pa

#  install the python song-and-spell app
sudo pip3 install song_and_spell

# add song-and-spell systemd-service
sudo bash -c 'cat << EOF > /etc/systemd/system/sands.service
[Unit]
Description=Song.And.Spell
After=syslog.target
After=network.target

[Service]
Type=simple
User=pi
Group=pi
WorkingDirectory=/home/pi/
ExecStart=/usr/local/bin/song_and_spell
Restart=always
Environment=USER=pi HOME=/home/pi

[Install]
WantedBy=multi-user.target
EOF
'
sudo systemctl enable sands.service
systemctl daemon-reload
# reboot
sudo reboot
