
from kivy.app import App

from kivy.factory import Factory

from kivy.properties import ObjectProperty

from kivy.uix.widget import Widget
from kivy.uix.button import Button
from kivy.uix.dropdown import DropDown
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.popup import Popup
from kivy.uix.screenmanager import ScreenManager, FadeTransition

# Issue5 starts here!
from Marsem.gui.settings import SettingsScreen
from Marsem.gui.home import HomeScreen
from Marsem.gui.picture import PictureScreen

from Marsem.gui.config import *
# See config.py
# Use change_picture_path("new path to picture folder") to change path.


class ScreenManagement(ScreenManager):
    pass


class CustomLayout(Widget):
    pass


class Decorations(Widget):
    pass


class DropDown(Button):
    def __init__(self, **kw):
        super(DropDown, self).__init__(**kw)
        self.dropdown = DropDown()
        self.dropdown.bind(on_release=self.on_release)


class Menu(FloatLayout):
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

        screenManager = ScreenManagement(transition=FadeTransition())

        return screenManager
    

if __name__ == "__main__":
    Marsem().run()

