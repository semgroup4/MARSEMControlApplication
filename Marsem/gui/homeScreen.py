#!/usr/bin/python3.4 -tt
# -*- coding: utf-8 -*-


from kivy.clock import Clock
from kivy.graphics.texture import Texture
from kivy.lang import Builder
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.image import Image
from kivy.uix.screenmanager import Screen
from kivy.uix.button import Button
from kivy.uix.progressbar import ProgressBar

import cv2

import time

import test.opencvtest as opencv

from threading import Thread


Builder.load_file("homeScreen.kv")


class HomeScreen(Screen):
    pass


class OpenCVStream(BoxLayout):
    def update(self, dt):
        try:
            frame = opencv.get_video()

            buf1 = cv2.flip(frame, 0)
            buf = buf1.tostring()

            texture1 = Texture.create(size=(frame.shape[1], frame.shape[0]), colorfmt='bgr')
            texture1.blit_buffer(buf, colorfmt='bgr', bufferfmt='ubyte')

            self.img1.texture = texture1
        except Exception:
            print('>> Could not retrieve frame, OpenCV may just be starting up')

    def start(self):
        self.img1 = Image(source='i44gsTM.jpg')
        self.add_widget(self.img1)

        opencv_stream = Thread(target=opencv.main, args=(), daemon=True, name='OpenCV')
        opencv_stream.start()

        Clock.schedule_interval(self.update, 1.0 / 33.0)


class StartButton(Button):
    def start(self, *args):
        print('Start-the-car-code goes here')


class PhotoProgress(ProgressBar):
    pass
