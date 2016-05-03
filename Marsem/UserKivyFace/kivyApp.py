from kivy.app import App

from kivy.uix.scrollview import ScrollView
from kivy.uix.widget import Widget
from kivy.uix.button import Button
from kivy.uix.progressbar import ProgressBar
from kivy.uix.screenmanager import ScreenManager, Screen, FadeTransition


class HomeScreen(Screen):
    pass


class SettingsScreen(Screen):
    pass


class PictureScreen(Screen):
    pass


class PictureView(ScrollView):
    pass


class CustomLayout(Widget):
    pass


class Decorations(Widget):
    pass


class StartButton(Button):

    def start(self, *args):
        print('Start-the-car-code goes here')


class BackButton(Button):
    pass


class PhotoProgress(ProgressBar):
    pass


class Marsem(App):

    def build(self):
        screenmanager = ScreenManager(transition=FadeTransition())
        screenmanager.add_widget(HomeScreen(name='home'))
        screenmanager.add_widget(PictureScreen(name='pictures'))
        screenmanager.add_widget(SettingsScreen(name='settings'))

        return screenmanager


if __name__ == "__main__":
    Marsem().run()
