from PIL import Image

import sys
sys.path.append("/Users/Frank/MARSEMControlApplication/marsem/protocol/") 
from kivy.app import App
from kivy.clock import Clock
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
from homeScreen import HomeScreen
from photoScreen import PhotoScreen
from settingsjson import settings_json


from config import *
import car
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
        setting = self.config.get('section_settings', 'save_path')

        return ScreenManagement(transition = FadeTransition())

    def build_config(self, config):
        config.setdefaults('section_settings', {
            'save_path': '/Users/Frank/Documents/kivy'})

    def build_settings(self, settings):
        settings.add_json_panel('Marsem Settings',
                                self.config,
                                data=settings_json)

    def on_config_change(self, config, section,
                         key, value):
        print(
        config, section, key, value)

    def on_startup(dt):
        print("starting")
        try:
            pass
            # car.stream(True)
        except NameError:
            print ("shits gone wrong")
    Clock.schedule_once(on_startup, 1)
    

if __name__ == "__main__":
    Marsem().run()


