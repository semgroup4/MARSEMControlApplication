#!/usr/bin/python3.4 -tt
# -*- coding: utf-8 -*-

import marsem.opencv as opencv

import cv2

from kivy.graphics.texture import Texture

from kivy.uix.screenmanager import Screen
from kivy.lang import Builder


Builder.load_file("calibrationScreen.kv")


class CalibrationScreen(Screen):
    def takeSnapshot(self):
        try:
            frame = opencv.get_video()

            buf1 = cv2.flip(frame, 0)
            buf = buf1.tostring()

            texture1 = Texture.create(size=(frame.shape[1], frame.shape[0]), colorfmt='bgr')
            texture1.blit_buffer(buf, colorfmt='bgr', bufferfmt='ubyte')

            self.stream_image.texture = texture1
        except Exception:
            print('>> Could not retrieve frame, OpenCV may just be starting up')