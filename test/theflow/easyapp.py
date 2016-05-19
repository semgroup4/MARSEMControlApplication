from kivy.app import App

from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.widget import Widget


class FirstScreen(Screen):
    pass


class SecondScreen(Screen):
    pass


class ThirdScreen(Screen):
    pass


class FourthScreen(Screen):
    pass


class CustomLayout(Widget):
    pass


class EasyApp(App):
    def build(self):
        screenmanager = ScreenManager()

        screenmanager.add_widget(FirstScreen(name='First'))
        screenmanager.add_widget(SecondScreen(name='Second'))
        screenmanager.add_widget(ThirdScreen(name='Third'))
        screenmanager.add_widget(FourthScreen(name='Fourth'))

        return screenmanager


if __name__ == "__main__":
    EasyApp().run()
