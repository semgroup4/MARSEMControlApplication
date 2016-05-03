import os

from kivy.app import App

from kivy.factory import Factory
from kivy.properties import ObjectProperty
from kivy.uix import video
from kivy.uix.dropdown import DropDown
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.popup import Popup
from kivy.uix.video import Video
from kivy.uix.widget import Widget
from kivy.uix.button import Button
from kivy.uix.progressbar import ProgressBar
from kivy.uix.screenmanager import ScreenManager, Screen, FadeTransition



class HomeScreen(Screen):
    def dismiss_popup(self):
        self._popup.dismiss()

    # Shows open file
    def show_load(self):
        content = LoadDialog(load=self.load, cancel=self.dismiss_popup)
        self._popup = Popup(title="Load file", content=content,
                            size_hint=(0.9, 0.9))
        self._popup.open()

    # Shows save file
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


class VideoStream(Video):
    def show_stream(stream):
        self.video = Video(stream)
        self.video.bind(position=self.on_position_change,
                        duration=self.on_durattion_change)
        

    def on_position_change(instance, value):
        print('The position in the video is', value)

    def on_duration_change(instance, value):
        print('The duration of the video is', value)

class SettingsScreen(Screen):
    pass


class PhotoScreen(Screen):
    pass


class ScreenManagement(ScreenManager):
    pass


class CustomLayout(Widget):
    pass


class Decorations(Widget):
    pass


class Menu(FloatLayout):
    pass


class DropDown(Button):
    def __init__(self, **kw):
        super(DropDown, self).__init__(**kw)
        self.ddn = DropDown()
        self.ddn.bind(on_release=self.on_release)


class StartButton(Button):
    def start(self, *args):
        print('Start-the-car-code goes here')


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
        Factory.register('Root', cls=Root)
        Factory.register('LoadDialog', cls=LoadDialog)
        Factory.register('SaveDialog', cls=SaveDialog)

        screenManager = ScreenManagement()
        screenManager.add_widget(HomeScreen())
        screenManager.add_widget(SettingsScreen())
        screenManager.add_widget(PhotoScreen())

        return screenManager


if __name__ == "__main__":
    Marsem().run()
