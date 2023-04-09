from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager
from kivymd.app import MDApp
from windows.main_window import Main
import subway_info


class MyApp(MDApp):

    def build(self):
        self.theme_cls.theme_style = "Dark"
        Builder.load_file("my.kv")
        self.screens = [Main(name="Main")]
        self.screen_manager = ScreenManager()
        [self.screen_manager.add_widget(x) for x in self.screens]
        return self.screen_manager


if __name__ == '__main__':
    MyApp().run()
