#!/usr/bin/python3.4 -tt
# -*- coding: utf-8 -*-


import cv2
import numpy as np
import time
from threading import Thread

import marsem.protocol.car as car
import marsem.protocol.config as cfg

blue_min = [255, 204, 204]
blue_max = [255, 0, 0]
red_min = [17, 15, 140]
red_max = [50, 56, 200]
green_min = [25, 94, 10]
green_max = [55, 144, 45]

video_capture = cv2.VideoCapture()
video_capture.set(cv2.CAP_PROP_FPS, 200)
kernel = np.ones((5,5), np.uint8)

current_frame = None
DEFAULT_TIMEOUT = 20

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
    if video_capture.open(cfg.stream_file):
        print("Success in connecting to remote file")
        return True
    else:
        if callback:
            callback()
        print("Failed to open remote file, make sure the server is running and not busy")
        return False


def run(color=Color() ,samples=[], callback=None, timeout=DEFAULT_TIMEOUT, burst=0):
    t_end = time.time() + timeout

    while video_capture.isOpened() and t_end > time.time():
        ret, frame = video_capture.read()

        burst += 1
        if burst < 50:
            update_current_frame(frame)
            continue
        
        mask = cv2.inRange(frame, color.min, color.max)
        blue = cv2.bitwise_and(frame, frame, mask=mask)
        gray = cv2.cvtColor(blue, cv2.COLOR_BGR2GRAY)

        (thresh, im_bw) = cv2.threshold(gray, 128, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)
        im_bw = cv2.threshold(gray, thresh, 255, cv2.THRESH_BINARY)[1]

        dilation = cv2.dilate(im_bw, kernel, iterations=10)
        erosion = cv2.erode(dilation, kernel, iterations=14)

        (_, contours, heir) = cv2.findContours(erosion.copy(), cv2.RETR_LIST, cv2.CHAIN_APPROX_NONE)
        if contours:
            contour = contours[0]
            x, y, w, h = cv2.boundingRect(contour)

            samples.append(x)

            center = x + int(w / 2)
            cv2.rectangle(frame, (center, 0), (center, 480), (0, 255, 0), 2)
        else:
            samples.append(0)

        # At this point, the green line has been added to the frame and the frame can be made available.
        update_current_frame(frame)
        if len(samples) == 2:
            value = sum(samples) / len(samples)
            print(value)
            if value > 45:
                car.move_right()
            if value < 45:
                car.move_forward()
            samples = []
        elif len(samples) > 2:
            samples = []

    if callback:
        callback()
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



