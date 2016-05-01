from kivy import app
from kivy.app import App
from kivy.base import runTouchApp
from kivy.config import ConfigParser
from kivy.lang import Builder
from kivy.uix import button
from kivy.uix.anchorlayout import AnchorLayout

from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.dropdown import DropDown
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.settings import SettingsWithSidebar

from settingsjson import settings_json


class Menu(DropDown):
    def open_dropdown_menu(self,*vargs):
        dropdown = Menu()
        dropdown.open
        mainbutton = self.ids['mainbutton']
    pass


class Interface(BoxLayout):
    pass


class Root(App):
    def build(self):
        main_box = FloatLayout()
        menu_box = AnchorLayout(anchor_x='left', anchor_y='top')
        settings_box = BoxLayout(orientation='vertical')

        settings = Interface()

        menu_box.add_widget(runTouchApp(Menu))
        settings_box.add_widget(settings)
        main_box.add_widget(settings_box)
        main_box.add_widget(menu_box)

        return main_box
    


if __name__ == '__main__':
    Root().run()
