# MARSEMControlApplication
Python app to control MARSEM

## Deploy
In order to deploy the application, run
```
python setup.py sdist
```
This will create a dist folder \(if there is none\). The resulting tar.gz is the application.

## Setup OpenCV (MAC OsX)
Make sure you have atleast python 3.4
* brew install opencv3 --with-ffmpeg
* pip3 install numpy




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


## Car
Runs on port 8000, takes a query parameter called 'action=action' where action can be:
* forward - move a step forward
* backward - move a step backward
* left - move a step left
* right - move a step right

## Notes

### Run the raspivid on the Raspberry PI
raspivid -t 0 -w 640 -h 480 -hf -fps 20 -o - | nc -k -l -p 2222
* -t time take before timeout and shutdown, 0 = no timeout
* -w width of the "frame"
* -h height of the "frame"
* -hf set horizontal flip
* -fps specifcy the framerate per second to record
* -o output to
* - send the image to stdoutput
* | pipe the output of the raspivid
* nc netcat network utility
* -k force nc to listen for another connection
* -l tell nc to listen for incomming connection
* 2222 the port to listen for connections on


### Testing
mplayer -fps 200 -demuxer h264es ffmpeg://tcp://192.168.2.1:2222






