from kivy.uix.boxlayout import BoxLayout
from kivy.uix.image import Image
from kivy.clock import Clock
from kivy.graphics.texture import Texture

from threading import Thread


import cv2
import test.opencvtest as opencv


class OpenCVStream(BoxLayout):
    def update(self, dt):
        frame = opencv.get_video()

        try:
            buf1 = cv2.flip(frame, 0)
            buf = buf1.tostring()

            texture1 = Texture.create(size=(frame.shape[1], frame.shape[0]), colorfmt='bgr')
            texture1.blit_buffer(buf, colorfmt='bgr', bufferfmt='ubyte')

            self.img1.texture = texture1
        except Exception:
            print('>> Could not retrieve frame, OpenCV may just be starting up')

    def start(self):
        self.img1 = Image(source='stop_icon.png')
        self.add_widget(self.img1)

        opencv_stream = Thread(target=opencv.main, args=(), daemon=True, name='OpenCV')
        opencv_stream.start()

        Clock.schedule_interval(self.update, 1.0 / 33.0)
