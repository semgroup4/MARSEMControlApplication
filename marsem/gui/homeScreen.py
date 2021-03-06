#!/usr/bin/python3.4 -tt
# -*- coding: utf-8 -*-


from kivy.clock import Clock
from kivy.graphics.texture import Texture
from kivy.lang import Builder
from kivy.uix.widget import Widget
from kivy.properties import BooleanProperty, NumericProperty, ObjectProperty
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.image import Image
from kivy.uix.screenmanager import Screen
from kivy.uix.button import Button
from kivy.uix.progressbar import ProgressBar

from timeit import default_timer as timer

from threading import Thread, current_thread

import time

import cv2

import marsem.opencv as opencv
import marsem.protocol.car as car
import marsem.gui.calibrationScreen as calibration


Builder.load_file("homeScreen.kv")


class HomeScreen(Screen):
    def start_server(self):
        if car.start_server():
            return True
        else:
            return False

    def stop_server(self):
        if car.stop_server():
            return False
        else:
            return True

    def stop_stream(self):
        opencv.stop()
        return car.stream(False)

    def connect(self):
        def _callback(t):
            if t and not opencv.is_connected():
                # Sleep ?
                time.sleep(1)
                return opencv.connect()

        def _failure(t):
            if opencv.is_connected():
                opencv.stop()
                return False
        return car.stream(True, success=_callback, failure=_failure)


class OpenCVStream(BoxLayout):
    error_count = 0                     # Counting number of times a frame from OpenCV could not be parsed into texture.

    loaded = False

    frame = ObjectProperty(None,allownone=True, force_dispatch=True)

    def on_frame(self, instance, pos):
        if self.frame != None:
            texture = Texture.create(size=(self.frame.shape[1],
                                           self.frame.shape[0]),
                                     colorfmt='bgr')
            texture.blit_buffer(self.frame.tostring(),
                                colorfmt='bgr',
                                bufferfmt='ubyte')
            texture.flip_horizontal()
            self.stream_image.texture = texture
        else:
            self.stream_image.texture = None


    def load(self):
        if not self.loaded:
            self.loaded = True

            self.stream_image = Image(source='stream_image.png')
            self.stream_image.keep_ratio = False
            self.stream_image.allow_stretch = True

            self.add_widget(self.stream_image)

    def update(self, dt):
        self.frame = opencv.get_video()

    def start(self):
        def _callback():
            Clock.unschedule(self.update)
            self.stream_image.texture = None
        c = calibration.CURRENT_COLOR
        #c.set_min_max(opencv.green_min, opencv.green_max)
        ocv = Thread(target=opencv.run,kwargs={"color": c, 
                                               "callback": _callback}, daemon=True)
        ocv.start()
        Clock.schedule_interval(self.update, 0.01)


class Status(Widget):
    # Assume that nothing is enabled and assign r, g, b and o to values you want as default
    # color for the widget "thing", whatever it might be (does not necessarily have to
    # inherit from 'Widget'.
    enabled = BooleanProperty(False)
    r = NumericProperty(0.988)
    g = NumericProperty(0.043)
    b = NumericProperty(0)
    o = NumericProperty(0.5)

    # 'value' is the 'enabled' BooleanProperty. Since we named the property 'enabled', the
    # function that will listen to a changed value HAS TO BE NAMED 'on_enabled'!
    def on_enabled(self, instance, value):
        if value:
            self.r = 0.227
            self.g = 1
            self.b = 0.082
            self.o = 1
        else:
            self.r = 0.988
            self.g = 0.043
            self.b = 0
            self.o = 0.5


class PhotoProgress(ProgressBar):
    def __init__(self, **kwargs):
        super(PhotoProgress, self).__init__(**kwargs)
        self.value = 0
        self.max = opencv.DEFAULT_TIMEOUT * 10 # Milliseconds

    def start(self):
        self.value = 0
        self.schedule_update()

    def schedule_update(self):
        Clock.unschedule(self.update) # Remove if already existing.
        Clock.schedule_interval(self.update, 0.1)

    def stop(self):
        Clock.unschedule(self.update)

    def update(self, dt):
        self.value += 1

        if self.value >= self.max:
            return False
