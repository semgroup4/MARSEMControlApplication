#!/usr/bin/python2 -tt
# -*- coding: utf-8 -*-

"""

import numpy as np
import cv2

cap = cv2.VideoCapture(0)


#img = cv2.imread('sachin.jpg')

while True:
    # Capture frame-by-frame
    ret, frame = cap.read()

    # Our operations on the frame come here
    #frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # Display the resulting frame
    cv2.imshow('frame',frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

    faces = face_cascade.detectMultiScale(frame, 1.3, 5)
    print(faces)
    #print(faces)
    for (x,y,w,h) in faces:
        img = cv2.rectangle(img,(x,y),(x+w,y+h),(255,0,0),2)
        roi_gray = gray[y:y+h, x:x+w]
        roi_color = img[y:y+h, x:x+w]
        eyes = eye_cascade.detectMultiScale(roi_gray)
        for (ex,ey,ew,eh) in eyes:
            cv2.rectangle(roi_color,(ex,ey),(ex+ew,ey+eh),(0,255,0),2)

cv2.imshow('img',img)
cv2.waitKey(0)
cv2.destroyAllWindows()

# When everything done, release the capture
cap.release()
cv2.destroyAllWindows()

"""






import cv2
import sys
import numpy as np
from time import sleep
import requests

MOVE = True


#cascPath = sys.argv[1]
#faceCascade = cv2.CascadeClassifier(cascPath)

faceCascade = cv2.CascadeClassifier('./haarcascade_frontalface_default.xml')
#faceCascade = cv2.CascadeClassifier('haarcascade_frontalface_alt.xml')
#eye_cascade = cv2.CascadeClassifier('haarcascade_eye.xml')

#video_capture = cv2.VideoCapture(0)
video_capture = cv2.VideoCapture()
video_capture.open('tcp://192.168.2.1:2222')

min_color, max_color = ([86, 31, 4], [220, 88, 50]) # blue
#min_color, max_color = ([17, 15, 140], [50, 56, 200]) # red

min_color = np.array(min_color, dtype='uint8')
max_color = np.array(max_color, dtype='uint8')

kernel = np.ones((5,5),np.uint8)

samples = []

burst = 0

while True:
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

    (cnts, _, asdf) = cv2.findContours(erosion.copy(), cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)
    if cnts.any():
        cnt = cnts[0]
        x,y,w,h = cv2.boundingRect(cnt)
        #print(x, y, w, h)

        samples.append(x)

        #cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2)
        center = int(x + (w / 2))
        cv2.rectangle(frame, (center, 0), (center, 480), (0, 255, 0), 2)
    else:
        samples.append(0)

    if len(samples) == 2:
        value = sum(samples) / len(samples)
        print(value)

        if value > 30:
            print('right')
            if MOVE:
                requests.get('http://192.168.2.1:8000/?action=right')

        if value < 30:
            print('forward')
            if MOVE:
                requests.get('http://192.168.2.1:8000/?action=forward')

        samples = []

    """
    faces = faceCascade.detectMultiScale(
        frame,
        scaleFactor=1.1,
        minNeighbors=5,
        minSize=(30, 30),
        flags=cv2.cv.CV_HAAR_SCALE_IMAGE
    )
    """

    # Draw a rectangle around the faces
    #for (x, y, w, h) in faces:
    #    cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2)

    # Display the resulting frame
    cv2.imshow('Video', frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# When everything is done, release the capture
video_capture.release()
cv2.destroyAllWindows()
