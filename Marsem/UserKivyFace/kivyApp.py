import os
import io
import urllib
import threading
from kivy.app import App
from kivy.atlas import CoreImage
from kivy.factory import Factory
from kivy.properties import ObjectProperty
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.popup import Popup
from kivy.uix.widget import Widget
from kivy.uix.button import Button
from kivy.uix.progressbar import ProgressBar
from kivy.uix.screenmanager import ScreenManager, Screen, FadeTransition
from kivy.uix.image import Image
from kivy.properties import StringProperty
from kivy.core.image import Image as CoreImage
from kivy.clock import Clock
from collections import deque


class MjpegViewer(Image):

    url = StringProperty()


    def start(self):
        self.quit = False
        self._queue = deque()
        self._thread = threading.Thread(target=self.read_stream)
        self._thread.daemon = True
        self._thread.start()
        self._image_lock = threading.Lock()
        self._image_buffer = None
        Clock.schedule_interval(self.update_image, 1 / 30.)

    def stop(self):
        self.quit = True
        self._thread.join()
        Clock.unschedule(self.read_queue)

    def read_stream(self):
        stream = urllib.urlopen(self.url)
        bytes = ''
        while not self.quit:
            bytes += stream.read(1024)
            a = bytes.find('\xff\xd8')
            b = bytes.find('\xff\xd9')
            if a != -1 and b != -1:
                jpg = bytes[a:b + 2]
                bytes = bytes[b + 2:]

                data = io.BytesIO(jpg)
                im = CoreImage(data,
                               ext="jpeg",
                               nocache=True)
                with self._image_lock:
                    self._image_buffer = im

    def update_image(self, *args):
        im = None
        with self._image_lock:
            im = self._image_buffer
            self._image_buffer = None
        if im is not None:
            self.texture = im.texture
            self.texture_size = im.texture.size

class HomeScreen(Screen):


    def dismiss_popup(self):
        self._popup.dismiss()

    # Shows open file
    def show_load(self):
        content = LoadDialog(load=self.load, cancel=self.dismiss_popup)
        self._popup = Popup(title="Load file", content=content,
                            size_hint=(0.9, 0.9))
        self._popup.open()

    #Shows save file
    def show_save(self):
        content = SaveDialog(save=self.save, cancel=self.dismiss_popup)
        self._popup = Popup(title="Save file", content=content,
                            size_hint=(0.9, 0.9))
        self._popup.open()

    def load(self, path, filename):
        with open(os.path.join(path, filename[0])) as stream:
            self.text_input.text = stream.read()

        self.dismiss_popup()

    def save(self, path, filename):
        with open(os.path.join(path, filename), 'w') as stream:
            stream.write(self.text_input.text)

        self.dismiss_popup()

class CustomLayout(Widget):
    pass


class Decorations(Widget):
    pass


class Menu(FloatLayout):
    pass


class StartButton(Button):
    def start(self, *args):
        print 'Start-the-car-code goes here'


class PhotoProgress(ProgressBar):
    pass


class LoadDialog(FloatLayout):
    load = ObjectProperty(None)
    cancel = ObjectProperty(None)


class SaveDialog(FloatLayout):
    save = ObjectProperty(None)
    text_input = ObjectProperty(None)
    cancel = ObjectProperty(None)


class Root(FloatLayout):
    loadfile = ObjectProperty(None)
    savefile = ObjectProperty(None)
    text_input = ObjectProperty(None)


class Marsem(App):
    def build(self):
        main = FloatLayout()
        screenmanager = ScreenManager(transition=FadeTransition())
        screenmanager.add_widget(HomeScreen(name='home'))
        Factory.register('Root', cls=Root)
        Factory.register('LoadDialog', cls=LoadDialog)
        Factory.register('SaveDialog', cls=SaveDialog)
        home = HomeScreen()

        viewer = MjpegViewer(
            url=
            "http://195.235.198.107:3344/axis-cgi/mjpg/video.cgi?resolution=320x240")
        viewer.start()

        main.add_widget(home)
        main.add_widget(viewer)


        return main


if __name__ == "__main__":

    Marsem().run()
