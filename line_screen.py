import threading
import kivy._clock
from kivy.clock import Clock
from kivy.uix.gridlayout import GridLayout
from kivy.uix.modalview import ModalView
from kivy.uix.screenmanager import Screen
from kivy.uix.scrollview import ScrollView
from kivymd.uix.button import MDRaisedButton
from kivymd.uix.expansionpanel import MDExpansionPanel, MDExpansionPanelOneLine
from kivymd.uix.label import MDLabel
from kivymd.uix.list import OneLineListItem
import subway_info
from datetime import datetime


class Content(GridLayout):

    def __init__(self, *args, **kwargs):
        super().__init__(**kwargs)
        self.station, self.arrivals = args
        for i, v in enumerate(self.arrivals.items(), 1):
            hour, arrivals = v
            current_list = self.ids.list1 if i == 1 else self.ids.list2
            current_list.add_widget(MDLabel(text=f"{hour}\n", halign='center'))
            for arrival in arrivals:
                current_list.add_widget(
                    OneLineListItem(text=f"{' ' * (self.width // 2 - (len(arrival) * 3))}{arrival}"))


class DirectionInformation(ModalView):

    def __init__(self, line, direction, current_hour):
        super().__init__()
        self.size_hint = (.85, .85)
        self.current_hour = current_hour
        self.loading = True
        self.line = line
        self.direction = direction

    def on_open(self):
        self.start()
        Clock.schedule_interval(self.check_loading, 0.1)

    def start(self):
        self.thread = threading.Thread(target=self.load)
        self.thread.start()

    def load(self):
        result = subway_info.get_stations_with_arrivals(self.line, self.direction)
        self.stations_with_times = result
        self.loading = False

    def check_loading(self, *args):
        if not self.loading:
            self.create_expansion_panels_for_each_station()
            self.ids.spinner.active = False
            return False

    def create_expansion_panels_for_each_station(self):
        stations_grid = GridLayout(cols=1, spacing=(0, 15), size_hint_y=None, size_hint_x=None, width=1000)

        for station, arrivals in self.stations_with_times.items():
            panel = MDExpansionPanel(panel_cls=MDExpansionPanelOneLine(text=station), icon="subway",
                                     content=Content(station, arrivals))
            stations_grid.add_widget(panel)

        stations_grid.bind(minimum_height=stations_grid.setter('height'))

        scroll_view = ScrollView(do_scroll_x=False)
        scroll_view.add_widget(stations_grid)

        self.add_widget(scroll_view)


class Line(Screen):

    def __init__(self, line: str, **kwargs):
        super().__init__(**kwargs)
        self.line = line

    def on_enter(self):
        directions = subway_info.get_directions(self.line)
        for d in directions:
            button = MDRaisedButton(text=d, font_style="Button", md_bg_color=[.8, .8, .8, 1],
                                    text_color=[.08, .07, .09, 1],
                                    padding=(20, 20),
                                    on_release=lambda x, direction=directions[d]: self.get_current_direction_modal_view(
                                        direction))
            self.ids.directions.add_widget(button)

    def reset(self):
        self.ids.directions.clear_widgets()

    def get_current_direction_modal_view(self, direction):
        view = DirectionInformation(self.line, direction, datetime.now().hour)
        view.open()
