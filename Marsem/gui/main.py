from PIL import Image
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.widget import Widget
from kivy.uix.button import Button
from kivy.config import ConfigParser
from kivy.uix.progressbar import ProgressBar
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.stacklayout import StackLayout
from kivy.uix.screenmanager import ScreenManager, Screen, FadeTransition
# Use change_picture_path("new path to picture folder") to change path.


# Issue5 starts here!
from marsem.gui.homeScreen import HomeScreen
from marsem.gui.photoScreen import PhotoScreen
from marsem.gui.settingsjson import settings_json


from marsem.gui.config import *
# See config.py
# See config.py
# Use change_picture_path("new path to picture folder") to change path.


class pathSettings(BoxLayout):
    config = ConfigParser()
    config.read('myconfig.ini')





class PhotoViewer(Screen):
    pass


class PhotoController(StackLayout):
    pass


class ScreenManagement(ScreenManager):
    pass


class CustomLayout(Widget):
    pass


class Decorations(Widget):
    pass


class Menu(FloatLayout):
    pass


class StartButton(Button):
    def start(self, *args):
        print('Start-the-car-code goes here')


class PhotoProgress(ProgressBar):
    pass


class Marsem(App):
    def build(self):

        self.use_kivy_settings = False
        setting = self.config.get('Marsem Config', 'Save Path')

        return ScreenManagement(transition = FadeTransition())

    def build_config(self, config):
        config.setdefaults('Marsem Config', {
            'Save Path': '/Users/Frank/Documents/kivy'})

    def build_settings(self, settings):
        settings.add_json_panel('Marsem Settings',
                                self.config,
                                data=settings_json)

    def on_config_change(self, config, section,
                         key, value):
        print(
        config, section, key, value)

if __name__ == "__main__":
    Marsem().run()


