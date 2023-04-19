from kivy.lang import Builder
from kivy.metrics import dp
from kivy.uix.screenmanager import Screen
from kivymd.uix.button import MDRaisedButton
import subway_info
from datetime import datetime
from line.modal_view import DirectionInformation


Builder.load_file("kv_files/line.kv")
class Line(Screen):

    def __init__(self, line: str, **kwargs):
        super().__init__(**kwargs)
        self.line = line

    def on_enter(self):
        directions = subway_info.get_directions(self.line)
        for d in directions:
            button = MDRaisedButton(text=d, font_style="Button", md_bg_color=[.8, .8, .8, 1],
                                    text_color=[.08, .07, .09, 1],
                                    padding=(dp(20), dp(20)),
                                    pos_hint={"center_x": 0.5},
                                    on_release=lambda x, direction=directions[d]: self.get_current_direction_modal_view(
                                        direction))
            self.ids.directions.add_widget(button)

    def reset(self):
        self.ids.directions.clear_widgets()

    def get_current_direction_modal_view(self, direction):
        view = DirectionInformation(self.line, direction, datetime.now().hour)
        view.open()
