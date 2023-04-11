from kivy.core.window import Window
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen
from kivymd.app import MDApp
import subway_info
from windows.M3 import M3


class Directions(Screen):
    pass


class MyApp(MDApp):

    def build(self):
        Window.size = (540, 800)
        Builder.load_file("my.kv")
        self.screens = [Directions(name="main"), M3(name="m3")]
        self.screen_manager = ScreenManager()
        [self.screen_manager.add_widget(s) for s in self.screens]
        return self.screen_manager

    def direction_to(self, new):
        self.screen_manager.transition.direction = new


if __name__ == '__main__':
    MyApp().run()
