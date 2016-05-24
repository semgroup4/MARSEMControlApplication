# MARSEMControlApplication
Python app to control MARSEM

## Deploy/Release an executeable
This project uses the pyinstaller project to create a main executeable file.
```
pip install pyinstaller
```

In order to do this, run the following commands:

```
pyi-makespec main
```
This will create a main.spec file in the current directory. In order to get our .kv files bundled into the executeable, go ahead and edit the main.spec file and add the a.datas for the .kv files needed.
```
a = Analysis(['marsem/gui/main.py'],
             pathex=['/your/genereated/path/from/makespec/MARSEMControlApplication'],
             binaries=None,
             datas=None,
             hiddenimports=[],
             hookspath=[],
             runtime_hooks=[],
             excludes=[],
             win_no_prefer_redirects=False,
             win_private_assemblies=False,
             cipher=block_cipher)
a.datas += [('homeScreen.kv', 'marsem/gui/homeScreen.kv', 'DATA')]
a.datas += [('marsem.kv', 'marsem/gui/marsem.kv', 'DATA')]
a.datas += [('photoScreen.kv', 'marsem/gui/photoScreen.kv', 'DATA')]
```
After you have edited the main.spec file to look like this. Go ahead and run the build command.
```
pyinstaller main.spec -p .
```
This will create a folder called "main" in your dist folder. This will also create a executeable main file inside it.
Go ahead and run our application doing:
```
./dist/main/main &
```
You should now see the M.A.R.S.E.M GUI controller on your scren. If you have any errors, fix them.

## Setup OpenCV3.1 For the project
### Prequisites
- python3.4
- ffmpeg
- [compiler] sudo apt-get install build-essential
- [required] sudo apt-get install cmake git libgtk2.0-dev pkg-config libavcodec-dev libavformat-dev libswscale-dev
- [optional] sudo apt-get install python-dev python-numpy libtbb2 libtbb-dev libjpeg-dev libpng-dev libtiff-dev libjasper-dev libdc1394-22-dev


We use the latest version (3.1) as of this writing.
Documentation: [OpenCV Docs](http://docs.opencv.org/3.0-beta/doc/tutorials/introduction/linux_install/linux_install.html)



- PYTHON3_PACKAGES_PATH, where to put the opencv module
- PYTHON3_LIBRARY, the python dylib file to use
- PYTHON3_INCLUDE_DIR, the python pythonV.m file to use
- WITH_FFMPEG, raspberry camera sends an FFMPEG file, there fore we need this
- OPENCV_EXTRA_MODULES_PATH, where you put your opencv_contrib folder

```
cmake -D CMAKE_BUILD_TYPE=RELEASE \
	-D CMAKE_INSTALL_PREFIX=/usr/local \
	-D PYTHON3_PACKAGES_PATH= /YOUR/PATH/TO/PYHON/3.4/site-packages \
	-D PYTHON3_LIBRARY=/YOUR/PATH/TO/PYTHON/3.4/lib/libpython3.4m.dylib \
	-D PYTHON3_INCLUDE_DIR= /YOUR/PATH/TO/PYTHON/3.4/include/python3.4m \
	-D INSTALL_C_EXAMPLES=OFF \
	-D INSTALL_PYTHON_EXAMPLES=ON \
	-D BUILD_EXAMPLES=ON \
	-D BUILD_opencv_python3=ON \
        -D WITH_FFMPEG=ON \
	-D OPENCV_EXTRA_MODULES_PATH=~/opencv_contrib/modules ..
```

## How to run Kivy app
Stand in MARSEMControlApplication
PYTHONPATH=. python3 marsem/gui/main.py

## App images you need to get:
All images can be found here: https://drive.google.com/drive/folders/0B8ZOX8oToxRGYU9CZUVma3pHaXM
[stream_image.png]

Put them in /yourpersonalpath/MARSEMControlApplication

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






