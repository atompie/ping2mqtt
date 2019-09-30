# ping2mqtt
Online presence to mqtt

# Installation

    sudo pip3 install multiping
    sudo pip3 install paho-mqtt
    
    cd /opt
    sudo git clone https://github.com/atompie/ping2mqtt.git
    sudo cp /opt/ping2mqtt/ping2mqtt.conf /etc/ping2mqtt.conf
    sudo cp /opt/ping2mqtt/systemd/ping2mqtt.service /etc/systemd/system/ping2mqtt.service
    sudo chown root:root /etc/systemd/system/ping2mqtt.service
    sudo chmod 664 /etc/systemd/system/ping2mqtt.service

    sudo systemctl daemon-reload
    
# Running

Service runs only as root.

    sudo service ping2mqtt start 
    
Start at server stat-up

    sudo systemctl enable ping2mqtt
