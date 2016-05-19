#!/usr/bin/python3.4 -tt
# -*- coding: utf-8 -*-


import configparser

import os

from PIL import Image

from kivy.uix.screenmanager import Screen
from kivy.lang import Builder


Builder.load_file("photoScreen.kv")


class PhotoScreen(Screen):
    def getPath(self):
        config = configparser.ConfigParser()
        config.read("marsem/gui/marsem.ini")
        settings_path = config.get('section_settings', 'save_path')
        return settings_path


    # Provides filechooser path
    def loadImage(self, fileChooser):
        global imagePath
        imagePath = fileChooser.path

        return print(fileChooser.path)

    def showImages(self):
        try:
            def listFiles(path):
                files = []
                for base, directory, filename in os.walk(path):
                    for i in range(len(filename)):
                        str = filename[i]
                        # Change what pictures can be loaded by changing .jpg to something else.
                        if str.find('.jpg') > 0:  # Breakout jpg
                            img = Image.open(base + "/" + filename[i])
                            img.show()
                            files.append(base + "/" + filename[i])
                return print(files)

            listFiles(imagePath)
        except NameError:
            pass

