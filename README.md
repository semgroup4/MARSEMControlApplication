# MARSEMControlApplication
Python app to control MARSEM

## Deploy
In order to deploy the application, run
```
python setup.py sdist
```
This will create a dist folder \(if there is none\). The resulting tar.gz is the application.

## Setup OpenCV (MAC OsX)
Make sure you're using pip for python 2.7
* brew install opencv
* cd /Library/Python/2.7/site-packages/
* ln -s /usr/local/Cellar/opencv/2.4.8/lib/python2.7/site-packages/cv.py cv.py
* ln -s /usr/local/Cellar/opencv/2.4.8/lib/python2.7/site-packages/cv2.so cv2.so
* pip install numpy




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
raspivid -t 0 -w 640 -h 480 -hf -fps 20 -o - | nc -k -l 2222

### Depricated
mplayer -fps 200 -demuxer h264es ffmpeg://tcp://192.168.2.1:2222






