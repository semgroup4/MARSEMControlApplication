#!/usr/bin/python3.4 -tt
# -*- coding: utf-8 -*-


import cv2
import sys
import numpy as np
from time import sleep

import requests

import marsem.protocol.car as car

MOVE = True


#cascPath = sys.argv[1]
#faceCascade = cv2.CascadeClassifier(cascPath)

faceCascade = cv2.CascadeClassifier('./haarcascade_frontalface_default.xml')
#faceCascade = cv2.CascadeClassifier('haarcascade_frontalface_alt.xml')
#eye_cascade = cv2.CascadeClassifier('haarcascade_eye.xml')

#video_capture = cv2.VideoCapture(0)
video_capture = cv2.VideoCapture() 
# Handle this better
#if not video_capture.open('tcp://192.168.2.1:2222'):
#    print("Failed to open remote file, make sure server is running & not busy")
#    exit(1)



min_color, max_color = ([86, 31, 4], [220, 88, 50]) # blue
#min_color, max_color = ([17, 15, 140], [50, 56, 200]) # red

min_color = np.array(min_color, dtype='uint8')
max_color = np.array(max_color, dtype='uint8')

kernel = np.ones((5,5),np.uint8)

def connect(callback=None):
    if video_capture.open("tcp://192.168.2.1:2222"):
        print("Success in connecting to remote file")
        return True
    else:
        if callback:
            callback()
        print("Failed to open remote file, make sure the server is running and not busy")
        return False


def run(burst=0, samples=[], callback=None):
    while video_capture.isOpened():
        # Capture frame-by-frame
        ret, frame = video_capture.read()
        
        burst += 1
        if burst < 200:
            continue
        
        mask = cv2.inRange(frame, min_color, max_color)
        blue = cv2.bitwise_and(frame, frame, mask=mask)
        
        gray = cv2.cvtColor(blue, cv2.COLOR_BGR2GRAY)
        (thresh, im_bw) = cv2.threshold(gray, 128, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)
        im_bw = cv2.threshold(gray, thresh, 255, cv2.THRESH_BINARY)[1]
        dilation = cv2.dilate(im_bw,kernel,iterations=10)
        erosion = cv2.erode(dilation,kernel,iterations=14)
        #opening = cv2.morphologyEx(erosion, cv2.MORPH_OPEN, kernel)

        (cnts, _, heir) = cv2.findContours(erosion.copy(), cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)
        if cnts.any():
            cnt = cnts[0]
            x,y,w,h = cv2.boundingRect(cnt)
            #print(x, y, w, h)

            samples.append(x)

            #cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2)
            center = x + int(w / 2)
            cv2.rectangle(frame, (center, 0), (center, 480), (0, 255, 0), 2)
        else:
            samples.append(0)

        if len(samples) == 2:
            value = sum(samples) / len(samples)

            if value > 30:
                if MOVE:
                    car.move_right()

            if value < 30:
                if MOVE:
                    car.move_forward()
            samples = []

        # Draw a rectangle around the faces
        #for (x, y, w, h) in faces:
        #    cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2)

        # Display the resulting frame
        cv2.imshow('Video', frame)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            if callback:
                stop(callback=callback)
            else:
                stop()
            break

def get_video(callback=None):
    if video_capture.isOpened():
        return video_capture.retrieve() # retval, image
    else:
        if callback:
            callback() # If things are not connected

def stop(callback=None):
    video_capture.release()
    cv2.destroyAllWindows()
    if callback:
        callback()

if __name__ == '__main__':
    connect()
    run()
