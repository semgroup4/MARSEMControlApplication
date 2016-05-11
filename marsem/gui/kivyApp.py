import os
from PIL import Image
from kivy.app import App
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.stacklayout import StackLayout
from kivy.uix.widget import Widget
from kivy.uix.button import Button
from kivy.uix.progressbar import ProgressBar
from kivy.uix.screenmanager import ScreenManager, Screen


class HomeScreen(Screen):
    pass


class SettingsScreen(Screen):
    pass


class PhotoScreen(Screen):
    # provides filechooser path
    def loadImage(self, fileChooser):
        global imagePath
        imagePath = fileChooser.path

        return print(fileChooser.path)


class PhotoViewer(Screen):
    #Load images from filechooser path
    def showImages(self):
        try:
            def listFiles(path):
                files = []
                for base, directory, filename in os.walk(path):
                    for i in range(len(filename)):
                        str = filename[i]
                        if str.find('.png') > 0:                            #Breakout PNG
                            img = Image.open(base + "/" + filename[i])
                            img.show()
                            files.append(base + "/" + filename[i])
                return print(files)

            listFiles(imagePath)
        except NameError:
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
        return ScreenManagement()


if __name__ == "__main__":
    Marsem().run()
