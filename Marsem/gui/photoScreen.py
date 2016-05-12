import configparser
import os
from PIL import Image
from kivy.uix.screenmanager import Screen

from kivy.lang import Builder


Builder.load_file("photoScreen.kv")


class PhotoScreen(Screen):
    def getPath(self):
        config = configparser.ConfigParser()
        config.read('marsem.ini')
        settings_path = config.get('section_settings', 'save_path')
        return settings_path


    # provides filechooser path
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
                        if str.find('.png') > 0:  # Breakout PNG
                            img = Image.open(base + "/" + filename[i])
                            img.show()
                            files.append(base + "/" + filename[i])
                return print(files)

            listFiles(imagePath)
        except NameError:
            pass

