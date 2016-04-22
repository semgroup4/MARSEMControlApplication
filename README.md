# MARSEMControlApplication
Python app to control MARSEM

## WiPI
The name of the wifi is Raspberry42

## How to PI
* Connect to the Rasberry PI though ssh (ask for the password)
* Run the main.py on the Rasberry

## How to Remote
* Connect to the Rasberry server (when it's running)
* Run OpenCV stream
* ???
* Profit


## Notes

### Run the raspivid on the Raspberry PI
raspivid -t 0 -w 640 -h 480 -hf -fps 20 -o - | nc -k -l 2222

### Depricated
mplayer -fps 200 -demuxer h264es ffmpeg://tcp://192.168.2.1:2222






