#!/usr/bin/python3.4 -tt
# -*- coding: utf-8 -*-


from kivy.uix.screenmanager import Screen
from kivy.uix.button import Button
from kivy.uix.progressbar import ProgressBar
from kivy.lang import Builder


Builder.load_file("homeScreen.kv")


class HomeScreen(Screen):
    pass


class StartButton(Button):
    def start(self, *args):
        print('Start-the-car-code goes here')


class PhotoProgress(ProgressBar):
    pass
