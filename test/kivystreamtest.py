from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.image import Image
from kivy.clock import Clock
from kivy.graphics.texture import Texture

import cv2
import opencvtest as opencv


class CamApp(App):
    def build(self):
        self.img1 = Image(source='images/1.jpg')
        layout = BoxLayout()
        layout.add_widget(self.img1)
        #opencv2 stuffs

        opencv.main()
        Clock.schedule_interval(self.update, 1.0/33.0)
        return layout

    def update(self, dt):
        print("Update")
        # display image from cam in opencv window
        ret, frame = opencv.get_video()
        # convert it to texture
        buf1 = cv2.flip(frame, 0)
        buf = buf1.tostring()
        texture1 = Texture.create(size=(frame.shape[1], frame.shape[0]), colorfmt='bgr')
        texture1.blit_buffer(buf, colorfmt='bgr', bufferfmt='ubyte')
        # display image from the texture
        self.img1.texture = texture1

if __name__ == '__main__':
    CamApp().run()
