#!/usr/bin/python3.4 -tt
# -*- coding: utf-8 -*-


import cv2
import numpy as np

import marsem.protocol.car as car

class Color():
    def __init__(self):
        """ Defaults to red color """
        self.min = create_color_range([17, 15, 140])
        self.max = create_color_range([50, 56, 200])

    def set_min_max(xa, xb):
        self.set_min(xa)
        self.set_max(xb)
        
    def set_min(xs):
        self.min = create_color_range(xs)

    def set_max(xs):
        self.max = create_color_range(xs)


video_capture = cv2.VideoCapture()
kernel = np.ones((5,5), np.uint8)
current_frame = None


def create_color_range(lst):
    return np.array(lst, dtype='uint8')

def connect(callback=None):
    """ Connects to the videostream on the raspberry pi """
    if video_capture.open("tcp://192.168.2.1:2222"):
    #if video_capture.open(0):
        print("Success in connecting to remote file")
        return True
    else:
        if callback:
            callback()
        print("Failed to open remote file, make sure the server is running and not busy")
        return False


# This needs to be threaded, to prevent main thread block
def run(color=Color() ,samples=[], callback=None):
    global current_frame

    while video_capture.isOpened():
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
                if MOVE:
                    car.move_right()

            if value < 45:
                if MOVE:
                    car.move_forward()
            samples = []

        if cv2.waitKey(1) & 0xFF == ord('q'):
            if callback:
                stop(callback=callback)
            else:
                stop()
            break


def get_video(callback=None):
    if video_capture.isOpened():
        return current_frame
    else:
        if callback:
            callback() # If things are not connected


def stop(callback=None):
    video_capture.release()
    if callback:
        callback()

if __name__ == '__main__':
    connect()
    run()
