#!/usr/bin/python3.4 -tt
# -*- coding: utf-8 -*-


import cv2
import numpy as np
import time
from threading import Thread
import functools

import marsem.protocol.car as car
import marsem.protocol.config as cfg

blue_min = [255, 204, 204]
blue_max = [255, 0, 0]
red_min = [17, 15, 140]
red_max = [50, 56, 200]
green_min = [25, 94, 10]
green_max = [55, 144, 45]

#cv2.VideoCapture.set(cv2.CV_CAP_PROP_FPS, 200)
video_capture = cv2.VideoCapture()
video_capture.set(cv2.CAP_PROP_FPS, 200)

current_frame = None
DEFAULT_TIMEOUT = 60

# **************************************
# OpenCV Color class
# Sets the colors for opencv
# **************************************
class Color():
    def __init__(self):
        """ Defaults to red color """
        self.min = create_color_range(red_min)
        self.max = create_color_range(red_max)

    def set_min_max(self, xa, xb):
        self.set_min(xa)
        self.set_max(xb)
        
    def set_min(self, xs):
        self.min = create_color_range(xs)

    def set_max(self, xs):
        self.max = create_color_range(xs)

    def get_color(self):
        return 'Min: ' + str(self.min) + '\nMax: ' + str(self.max)



def create_color_range(lst):
    return np.array(lst, dtype='uint8')


# **************************************
# OpenCV
# OpenCV module
# **************************************

def update_current_frame(f):
    global current_frame
    current_frame = f

def is_connected():
    return video_capture.isOpened()


# Connects the video capture to its video source.
def connect(callback=None):
    """ Connects to the videostream on the raspberry pi """
    if video_capture.isOpened():
        print("Already connected")
        return True
    #if video_capture.open(0):
    if video_capture.open(cfg.stream_file):
        print("Success in connecting to remote file")
        return True
    else:
        if callback:
            callback()
        print("Failed to open remote file, make sure the server is running and not busy")
        return False


def run(color=Color() ,samples=[], callback=None, timeout=DEFAULT_TIMEOUT):
    t_end = time.time() + timeout
    time_t = time.time
    burst = 0
    kernel = np.ones((5,5), np.uint8)

    # Avoid re-evauluating the module calls inside the loop
    # Code optimization, do not remove!
    append = samples.append
    capt_read = video_capture.read
    inRange = cv2.inRange
    bitwise_and = cv2.bitwise_and
    cvtColor = cv2.cvtColor
    color_min = color.min
    color_max = color.max
    BGR2GRAY = cv2.COLOR_BGR2GRAY
    treshold = cv2.threshold
    THRESH_BINARY = cv2.THRESH_BINARY
    THRESH_OTSU = cv2.THRESH_OTSU
    morphologyEx = cv2.morphologyEx
    MORPH_CLOSE = cv2.MORPH_CLOSE
    findContours = cv2.findContours
    RETR_LIST = cv2.RETR_LIST
    CHAIN_APPROX_SIMPLE = cv2.CHAIN_APPROX_SIMPLE
    boundingRect = cv2.boundingRect
    rectangle = cv2.rectangle
    car_move_forward = car.move_forward
    car_move_right = car.move_right

    while (1):
        ret, frame = capt_read()
        
        if burst < 200:
            # Read 200 frames or so before starting
            burst += 1
            update_current_frame(frame)
            continue

        if time_t() > t_end:
            break
        
        mask = inRange(frame, color_min, color_max)
        mask_color = bitwise_and(frame, frame, mask=mask)
        gray = cvtColor(mask_color, BGR2GRAY)

        (thresh, im_bw) = treshold(gray, 128, 255, THRESH_BINARY + THRESH_OTSU)
        im_bw = treshold(gray, thresh, 255, THRESH_BINARY)[1]

        # Erode and dilate using MORPH_CLOSE in morphologyEx
        erosion = morphologyEx(im_bw, MORPH_CLOSE, kernel)
        (_, contours, heirarchy) = findContours(erosion.copy(), RETR_LIST, CHAIN_APPROX_SIMPLE)
        if contours:
            contour = contours[0]
            x, y, w, h = boundingRect(contour)
            append(x)

            center = x + int(w / 2)
            rectangle(frame, (center, 0), (center, 480), (0, 255, 0), 2)
        else:
            append(0)
        update_current_frame(frame)

        length = len(samples)
        if length >= 2:
            value = sum(samples) / length
            if value > 45:
                # Move a "lot" to the right
                car_move_right()
#                car_move_right()
#                car_move_right()
            else:
                car_move_forward()
#                car_move_forward()
#                car_move_forward()
            del samples[:]
            
    if callback:
        callback()
        
    time.sleep(2)
    stop()
    # Turn the stream OFF after OpenCV has run to completion.
    car.stream(False)


# Returns a 'single' prepared frame from OpenCV
def get_video(callback=None):
    if video_capture.isOpened():
        return current_frame
    else:
        if callback:
            callback() # If things are not connected


# Stops video capturing with OpenCV and stops the car stream (closes the camera).
def stop():
    video_capture.release()
