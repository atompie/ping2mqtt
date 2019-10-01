# ping2mqtt
Online presence to mqtt

# Installation

    sudo -H pip3 install multiping
    sudo -H pip3 install paho-mqtt
    
    cd /opt
    sudo git clone https://github.com/atompie/ping2mqtt.git
    sudo cp /opt/ping2mqtt/ping2mqtt.conf /etc/ping2mqtt.conf
    sudo cp /opt/ping2mqtt/systemd/ping2mqtt.service /etc/systemd/system/ping2mqtt.service
    sudo chown root:root /etc/systemd/system/ping2mqtt.service
    sudo chmod 664 /etc/systemd/system/ping2mqtt.service

    sudo systemctl daemon-reload

# Configuration

Configuration file is in /etc folder. Edit file ping2mqtt.conf to connect 
to mosquitto and add ip addresses to ping. Config file is quite self explanatory.
Edit host, port, user, and password in section \[mqtt\] to connect to mqtt server.
No TSL authentication is available at this moment, only basic authentication. 

To ping define ip and topic to send to information if the device is online or offile.

    [192.168.1.1]
    ; Send status of the device to the following topic.
    ; $prefix is replaced by prefix defined in [defaults] section. 
    
    topic = $prefix/router

    ; Payload is defined in [defaults] and can be overridden here.
    online_label = ON
    offline_label = OFF
    
Full config example:

```
[mqtt]
; MQTT authentication section. Set host, port, user, and password.
; No TSL authentication is available at this moment

; Default host is 127.0.0.1
; host = 127.0.0.1

; Default port id 1883
; port = 1883

; Default user is empty undefined user
; user =

; Default password is empty undefined password
; password =

[defaults]
; Defaults define global values for all moitored devices. It can be overridden in
; configuration of any device.

; Default prefix for mqtt topic. Default value is ping.
; prefix = ping

; Default quality of service is 0
; qos = 1

; What to send in payload when device is online or offline.
; If online_payload or offline_payload is not defined then the average response time is returned.
; Further more update_time is discarded. Average response time is reported to MQTT server all the time.
online_payload = ONLINE
offline_payload = OFFLINE


[ping]
; Wait X sec after multi ping is preformed. This lets you decrease the number of pings
; that are executed by te ping2mqtt service.
interval = 5

; Ping timeout in seconds. If there is not response for PING in 2 seconds set the device as OFFLINE.
timeout = 2

; Number of retries when there is no PONG for your PING. There is a initial ping and 3 retries.
; All together 4 tries. After 4 tries with no response device is set as OFFLINE.
retries = 3

; Send update of address statue every 10 min unless state changes.
; Then update immediately, but not quicker then set interval
update_time = 600


; Devices to ping section

[192.168.1.1]
; Send status of the device to the following topic. Payload is defined in [defaults] and can be
; overridden here

topic = $prefix/router
```
# Running

Service runs only as root.

    sudo service ping2mqtt start 
    
Start at server stat-up

    sudo systemctl enable ping2mqtt
