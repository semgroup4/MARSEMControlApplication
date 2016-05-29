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
        
            buf1 = cv2.flip(frame, 0) # Convert it into a string
            buf = buf1.tostring()
    
            # Do some stuff to make it into a texture
            texture1 = Texture.create(size=(frame.shape[1], frame.shape[0]), colorfmt='bgr')
            texture1.blit_buffer(buf, colorfmt='bgr', bufferfmt='ubyte') # Do some more stuff to make it into a texture

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



class PhotoProgress(ProgressBar):
    def __init__(self, **kwargs):
        super(PhotoProgress, self).__init__(**kwargs)
        self.max = 60 # 60 seconds

    def start(self):
        self.schedule_update()

    def schedule_update(self):
        # Remove if already existing.
        Clock.unschedule(self.update)
        Clock.schedule_interval(self.update, 1.0)

    def update(self, dt):
        self.value += 1

        if self.value >= 60:
            self.value = 0
            return False
