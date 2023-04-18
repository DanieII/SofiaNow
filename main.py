from kivy.core.window import Window
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen
from kivymd.app import MDApp
from line_screen import Line


class Home(Screen):
    pass


class MyApp(MDApp):

    def build(self):
        self.title = "SofiaNow"
        Builder.load_file("my.kv")
        self.screens = [Home(name="home"), Line("M3", name="m3"), Line("M1-M2", name="m1-m2")]
        self.screen_manager = ScreenManager()
        [self.screen_manager.add_widget(s) for s in self.screens]
        return self.screen_manager

    def change_transition_direction(self, new):
        self.screen_manager.transition.direction = new


if __name__ == '__main__':
    MyApp().run()
