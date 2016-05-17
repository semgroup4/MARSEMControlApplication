from kivy.uix.boxlayout import BoxLayout
from kivy.uix.image import Image
from kivy.clock import Clock
from kivy.graphics.texture import Texture

from threading import Thread

import time

import cv2
import test.opencvtest as opencv


class OpenCVStream(BoxLayout):
    def update(self, dt):
        # TESTING SHIT
        #ret, frame = self.capture.read()

        # OUR SHIT
        frame = opencv.get_video()

        # convert it (whatever "it" is) to a texture
        try:
            buf1 = cv2.flip(frame, 0)
            buf = buf1.tostring()
            texture1 = Texture.create(size=(frame.shape[1], frame.shape[0]), colorfmt='bgr')
            texture1.blit_buffer(buf, colorfmt='bgr', bufferfmt='ubyte')
            # display image from the texture
            self.img1.texture = texture1
        except:
            print('>> Could not retrieve frame, OpenCV may just be starting up')

    def start(self):
        self.img1 = Image(source='i44gsTM.jpg')
        self.add_widget(self.img1)

        # TESTING SHIT
        #self.capture = cv2.VideoCapture(0)

        # OUR SHIT
        opencv_thread = Thread(target=opencv.main, args=(), daemon=True, name='OpenCV')
        opencv_thread.start()

        Clock.schedule_interval(self.update, 1.0 / 33.0)
