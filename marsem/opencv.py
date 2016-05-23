#!/usr/bin/python3.4 -tt
# -*- coding: utf-8 -*-


from kivy.clock import Clock

import cv2

import numpy as np

from timeit import default_timer as timer

# Necessary to call schedule_interval with common def args.
from functools import partial

import marsem.protocol.car as car

import marsem.protocol.config as cfg


class Color():
    def __init__(self):
        """ Defaults to red color """
        self.min = create_color_range([17, 15, 140])
        self.max = create_color_range([50, 56, 200])

    def set_min_max(self, xa, xb):
        self.set_min(xa)
        self.set_max(xb)
        
    def set_min(self, xs):
        self.min = create_color_range(xs)

    def set_max(self, xs):
        self.max = create_color_range(xs)


video_capture = cv2.VideoCapture()
kernel = np.ones((5,5), np.uint8)

current_frame = None
partial_def = None


def create_color_range(lst):
    return np.array(lst, dtype='uint8')


# Connects the video capture to its video source.
def connect(callback=None):
    """ Connects to the videostream on the raspberry pi """
    # TODO: This may well need to be changed, is the port correct?
    if video_capture.open(cfg.stream_file):
        print("Success in connecting to remote file")
        return True
    else:
        if callback:
            callback()
        print("Failed to open remote file, make sure the server is running and not busy")
        return False


# Called to start OpenCV stream, this def. prepares some necessary args.
def run(color=Color(), samples=[], callback=None):
    start_time = timer()    # Get the point in time where this def. was called to count from this point.

    # You have to use a 'partial' def. in order to schedule an event *with* arguments.
    global partial_def
    # partial(def, arg, arg, arg, arg)
    partial_def = partial(update, start_time, color, samples, callback)

    # partial def., Clock time interval
    Clock.schedule_interval(partial_def, 0.1)


# Updating OpenCV stream frame 'current_frame'
def update(start_time, color, samples, callback, dt):
    global current_frame  # The current video frame captured by OpenCV

    if video_capture.isOpened():
        # Capture frame-by-frame
        ret, frame = video_capture.read()
        
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
        current_frame = frame

        if len(samples) == 2:
            value = sum(samples) / len(samples)

            if value > 45:
                car.move_right()

            if value < 45:
                car.move_forward()
            samples = []

        if cv2.waitKey(1) & 0xFF == ord('q'):
            if callback:
                stop(callback=callback)
                Clock.unschedule(partial_def)
                car.stream(False)
            else:
                stop()
                Clock.unschedule(partial_def)
                car.stream(False)

        # Checking running time of OpenCV:
        current_time = timer()              # Current execution time to be compared with start_time.
        diff = current_time - start_time    # Calculate the difference.

        if diff > 10.0:                     # If the difference is more than the set threshold, abort.
            stop()
            Clock.unschedule(partial_def)
            car.stream(False)


# Returns a 'single' prepared frame from OpenCV
def get_video(callback=None):
    if video_capture.isOpened():
        return current_frame
    else:
        if callback:
            callback() # If things are not connected


# Stops video capturing with OpenCV and stops the car stream (closes the camera).
def stop(callback=None):
    video_capture.release()
    # NEW, can we keep this?
    car.stream(False)
    if callback:
        callback()

if __name__ == '__main__':
    connect()
    run()
