#!/usr/bin/python3.4 -tt
# -*- coding: utf-8 -*-


from kivy.app import App
from kivy.clock import Clock
from kivy.uix.widget import Widget
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.screenmanager import ScreenManager, Screen, FadeTransition

from marsem.gui.homeScreen import HomeScreen
from marsem.gui.photoScreen import PhotoScreen
from marsem.gui.settingsjson import settings_json
from marsem.protocol import car

import marsem.protocol.config as cfg
import io
#import requests
#from io import BytesIO




class ScreenManagement(ScreenManager):
    pass


class CustomLayout(Widget):
    pass


class Decorations(Widget):
    pass


class Menu(FloatLayout):
    #The picture function is currently bound to the "Settings Button"
    def car_picture(self):
        byte_stream = io.BytesIO(car.picture())
        img = Image.open(byte_stream)
        

class Marsem(App):
    def build(self):

        self.use_kivy_settings = False
        setting = self.config.get('section_settings', 'save_path')

        return ScreenManagement(transition = FadeTransition())

    def build_config(self, config):
        config.setdefaults('section_settings', {
        'save_path': '~/'})

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
        
        except NameError:
            print ("shits gone wrong")
        Clock.schedule_once(on_startup, 1)
    

if __name__ == "__main__":
    Marsem().run()


