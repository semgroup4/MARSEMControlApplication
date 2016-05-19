#!/usr/local/bin/python3

import numpy as np
import cv2
import time
import threading
import marsem.protocol.car as car
import test.config as config

min_color, max_color = ([86, 31, 4], [220, 88, 50]) # blue
#min_color, max_color = ([17, 15, 140], [50, 56, 200]) # red

min_color = np.array(min_color, dtype='uint8')
max_color = np.array(max_color, dtype='uint8')

kernel = np.ones((5,5), np.uint8)

#samples = []

f_frame = None


def main(samples=[]):
    global cap
    cap = cv2.VideoCapture(config.stream_file)
    print('>> OpenCV stream has started!')
    # The frame needs to be declared global to be able to be read from get_video
    global f_frame

    while cap.isOpened():
        ret, frame = cap.read()

        mask = cv2.inRange(frame, min_color, max_color)
        blue = cv2.bitwise_and(frame, frame, mask=mask)
        gray = cv2.cvtColor(blue, cv2.COLOR_BGR2GRAY)

        (thresh, im_bw) = cv2.threshold(gray, 128, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)
        im_bw = cv2.threshold(gray, thresh, 255, cv2.THRESH_BINARY)[1]

        dilation = cv2.dilate(im_bw, kernel, iterations=10)
        erosion = cv2.erode(dilation, kernel, iterations=14)

        (_, cnts, heir) = cv2.findContours(erosion.copy(), cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)
        if cnts:
            cnts = cnts[0]
            x, y, w, h = cv2.boundingRect(cnts)
            samples.append(x)
            center = x + int(w / 2)
            cv2.rectangle(frame, (center, 0), (center, 480), (0, 255, 0), 2)
        else:
            samples.append(0)

        f_frame = frame

        if len(samples) == 2:
            value = sum(samples) / len(samples)
            car.move_car(action="forward")
            print(threading.active_count())

            samples = []
        
        #cv2.imshow('Video', frame)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()


def get_video(callback=None):
    if cap.isOpened():
        return f_frame # retval, image
    else:
        if callback:
            callback() # If things are not connected
