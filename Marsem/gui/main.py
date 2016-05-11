from PIL import Image
from kivy.app import App
from kivy.uix.widget import Widget
from kivy.uix.button import Button
from kivy.uix.progressbar import ProgressBar
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.stacklayout import StackLayout
from kivy.uix.screenmanager import ScreenManager, Screen, FadeTransition
# Use change_picture_path("new path to picture folder") to change path.


# Issue5 starts here!
from Marsem.gui.settings import SettingsScreen
from Marsem.gui.home import HomeScreen
from Marsem.gui.photo import PhotoScreen

from Marsem.gui.config import *
# See config.py
# See config.py
# Use change_picture_path("new path to picture folder") to change path.





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

        return ScreenManagement(transition=FadeTransition())


if __name__ == "__main__":
    Marsem().run()


