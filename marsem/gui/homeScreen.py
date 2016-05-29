#!/usr/bin/python3.4 -tt
# -*- coding: utf-8 -*-


from kivy.clock import Clock
from kivy.graphics.texture import Texture
from kivy.lang import Builder
from kivy.uix.widget import Widget
from kivy.properties import BooleanProperty, NumericProperty
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
        car.start_server()

    def stop_server(self):
        car.stop_server()

    def stop_stream(self):
        car.stream(False)

    def connect(self):
        def _callback(t):
            if t and not opencv.is_connected():
                # Sleep ?
                time.sleep(1)
                opencv.connect()

        def _failure(t):
            if opencv.is_connected():
                opencv.stop()
        car.stream(True, success=_callback, failure=_failure)



class OpenCVStream(BoxLayout):
    error_count = 0                     # Counting number of times a frame from OpenCV could not be parsed into texture.

    loaded = False

    def load(self):
        if not self.loaded:
            self.loaded = True

            self.stream_image = Image(source='stream_image.png')
            self.stream_image.keep_ratio = False
            self.stream_image.allow_stretch = True

            self.add_widget(self.stream_image)

    def update(self, dt):
        try:
            frame = opencv.get_video() # Step 1, get the current frame from OpenCV.
    
            # Do some stuff to make it into a texture
            texture1 = Texture.create(size=(frame.shape[1], frame.shape[0]), colorfmt='bgr')
            texture1.blit_buffer(frame.tostring(), colorfmt='bgr', bufferfmt='ubyte') # Do some more stuff to make it into a texture
            texture1.flip_vertical()
            texture1.flip_horizontal()

            self.stream_image.texture = texture1 # Set the defined image's texture as the new texture
        except Exception as error:
            # Stop reading the opencv when there is no frame
            print(error)
            self.stream_image.texture = None
            return False

    def start(self):
        ocv = Thread(target=opencv.run,kwargs={"color": calibration.CURRENT_COLOR}, daemon=True)
        ocv.start()
        Clock.schedule_interval(self.update, 0.1)


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
        self.max = 600

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

        if self.value >= 600:
            return False
