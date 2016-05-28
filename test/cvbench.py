import cv2
import numpy as np
from random import randrange
img = np.zeros((1920, 1080), dtype = np.uint8)
counter = 0
while counter < 1000:
    cv2.line(img, (randrange(0, 1920), randrange(0, 1080)), (randrange(0, 1920), randrange(0, 1080)), (randrange(0, 255)))
    cv2.imshow('test', img)
    temp = cv2.waitKey(1)
    counter += 1
    print(counter)

"""
cmake -D CMAKE_BUILD_TYPE=RELEASE \
    -D CMAKE_INSTALL_PREFIX=/usr/local \
    -D PYTHON3_PACKAGES_PATH= /Library/Frameworks/Python.framework/Versions/3.4/lib/python3.4/site-packages/ \
    -D PYTHON3_LIBRARY=/YOUR/PATH \
    -D PYTHON3_INCLUDE_DIR= /YOUR/PATH/TO/PYTHON/3.4/include/python3.4m \
    -D INSTALL_C_EXAMPLES=OFF \
    -D INSTALL_PYTHON_EXAMPLES=ON \
    -D BUILD_EXAMPLES=ON \
    -D BUILD_opencv_python3=ON \
    -D WITH_FFMPEG=ON \
    -D WITH_TBB=ON \
    -D OPENCV_EXTRA_MODULES_PATH=~/opencv_contrib/modules ..
"""
