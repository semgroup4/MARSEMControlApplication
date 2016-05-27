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

from threading import Thread

import time

import cv2

import marsem.opencv as opencv
import marsem.protocol.car as car
import marsem.gui.calibrationScreen as calibration


Builder.load_file("homeScreen.kv")


class HomeScreen(Screen):
    def start_server(self):
        car.start_server()

    def start(self):
        # TODO: check if this works.
        #ocv = Thread(target=opencv.run, args=(calibration.CURRENT_COLOR,), daemon=True)
        #ocv.start()
        opencv.run(calibration.CURRENT_COLOR)

    def connect(self):
        # Ask about tomorrow:
        def _callback(t):
            if t and not opencv.is_connected():
                # Sleep ?
                time.sleep(1)
                opencv.connect()

        def _failure(t):
            if opencv.is_connected():
                opencv.stop()

        # Activate the car stream (camera), upon returning True -> perform _callback | returning False ->
        # perform _failure.
        car.stream(True, success=_callback, failure=_failure)


class PhotoProgress(ProgressBar):
    def __init__(self, **kwargs):
        super(PhotoProgress, self).__init__(**kwargs)
        self.max = 600

    def start(self):
        self.schedule_update()

    def schedule_update(self):
        # Remove if already existing.
        Clock.unschedule(self.update)
        Clock.schedule_interval(self.update, 0.1)

    def update(self, dt):
        self.value += 1

        if self.value >= 600:
            self.value = 0
            return False
