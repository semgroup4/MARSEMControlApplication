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
    def start_server(self):
        car.start_server()

    def reset(self):
        def _callback(t):
            if t and not opencv.is_connected():
                time.sleep(2)
                opencv.connect()
            else:
                if opencv.is_connected():
                    # Close the opencv
                    opencv.stop()

        def _failure(t):
            if opencv.is_connected():
                opencv.stop()

        car.stream(False, success=_callback, failure=_failure)

    def connect(self):
        def _callback(t):
            if t and not opencv.is_connected():
                print('good boooooy')
                # Sleep ?
                time.sleep(2)
                opencv.connect()
            else:
                if opencv.is_connected():
                    # Close the opencv
                    opencv.stop()

        def _failure(t):
            if opencv.is_connected():
                opencv.stop()

        car.stream(True, success=_callback, failure=_failure)

    def start_sequence(self):
        opencv.run()

    # TODO! Why is this here?
    def car_picture(self):
        picture = car.picture()
        byte_stream = io.BytesIO(picture)
        print(byte_stream)
        img = Image.open(byte_stream)
        print("img", img)


class PhotoProgress(ProgressBar):
    def start(self):
        self.max = 600

        Clock.schedule_interval(self.update, 0.1)

    def update(self, dt):
        self.value += 1

        if self.value is 60:
            Clock.unschedule(self.update())
