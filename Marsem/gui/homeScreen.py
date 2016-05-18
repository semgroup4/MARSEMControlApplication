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

import cv2

import marsem.opencv as opencv

from threading import Thread


Builder.load_file("homeScreen.kv")


loaded = False


class HomeScreen(Screen):
    pass


class OpenCVStream(BoxLayout):
    def load(self):
        global loaded

        if not loaded:
            self.stream_image = Image(source='stop_icon.png')
            self.add_widget(self.stream_image)
            loaded = True

    def update(self, dt):
        try:
            frame = opencv.get_video()

            buf1 = cv2.flip(frame, 0)
            buf = buf1.tostring()

            texture1 = Texture.create(size=(frame.shape[1], frame.shape[0]), colorfmt='bgr')
            texture1.blit_buffer(buf, colorfmt='bgr', bufferfmt='ubyte')

            self.stream_image.texture = texture1
        except Exception:
            print('>> Could not retrieve frame, OpenCV may just be starting up')

    def start(self):
        opencv_stream = Thread(target=opencv.run, args=(), daemon=True, name='OpenCV')
        opencv_stream.start()

        Clock.schedule_interval(self.update, 1.0 / 33.0)

    def connect(self):
        opencv.connect()

    def stop(self):
        opencv.stop()
        Clock.unschedule(self.update)


class CustomButton(Button):
    enabled = BooleanProperty(True)

    def on_enabled(self, instance, value):
        if value:
            self.background_color = [1,1,1,1]
            self.color = [1,1,1,1]
        else:
            self.background_color = [1,1,1,.3]
            self.color = [1,1,1,.5]

    def on_touch_down(self, touch):
        if self.enabled:
            return super(self.__class__, self).on_touch_down(touch)


class StartButton(Button):
    def start(self, *args):
        print('Start-the-car-code goes here')


class PhotoProgress(ProgressBar):
    pass
