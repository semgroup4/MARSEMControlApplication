#!/usr/bin/python3.4 -tt
# -*- coding: utf-8 -*-


from kivy.clock import Clock
from kivy.graphics.texture import Texture
from kivy.lang import Builder
from kivy.properties import BooleanProperty
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.image import Image
from kivy.uix.screenmanager import Screen
from kivy.uix.button import Button
from kivy.uix.progressbar import ProgressBar

from timeit import default_timer as timer

import time

import cv2

import marsem.opencv as opencv
import marsem.protocol.car as car


Builder.load_file("homeScreen.kv")


class HomeScreen(Screen):
    pass


class OpenCVStream(BoxLayout):
    error_count = 0                     # Counting number of times a frame from OpenCV could not be parsed into texture.

    loaded = False

    def start_server(self):
        car.start_server()

    def stop_server(self):
        car.stop_server()

    def load(self):
        if not self.loaded:
            self.loaded = True

            self.stream_image = Image(source='stream_image.png')
            self.stream_image.keep_ratio = False
            self.stream_image.allow_stretch = True

            self.add_widget(self.stream_image)

    def update(self, dt):
        try:
            frame = opencv.get_video()

            buf1 = cv2.flip(frame, 0)
            buf = buf1.tostring()

            texture1 = Texture.create(size=(frame.shape[1], frame.shape[0]), colorfmt='bgr')
            texture1.blit_buffer(buf, colorfmt='bgr', bufferfmt='ubyte')

            self.stream_image.texture = texture1

            self.error_count = 0        # Reset error count if all went well.
        except Exception:
            self.error_count += 1       # Add 1 to error count since exception was raised.

            print('>> Could not retrieve frame, OpenCV may just be starting up')

            if self.error_count >= 10:  # 10 or more errors were encountered, abort stream.
                self.error_count = 0    # Reset error count to 0 in order to be able to start the stream again.
                Clock.unschedule(self.update)

                print('>> Stream unavailable')

    def start(self):
        # NEW, added car.stream here instead for automation purposes.
        # TODO: check if this works.
        opencv.run()
        Clock.schedule_interval(self.update, 0.1)

    def connect(self):
        if car.stream(True):
            time.sleep(2)
            opencv.connect()

    def stop(self):
        opencv.stop()
        Clock.unschedule(self.update)


class StartButton(Button):
    def start(self, *args):
        print('Start-the-car-code goes here')


class PhotoProgress(ProgressBar):
    def start(self):
        self.max = 600

        Clock.schedule_interval(self.update, 0.1)

    def update(self, dt):
        self.value += 1

        if self.value is 60:
            Clock.unschedule(self.update())
