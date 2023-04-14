from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.modalview import ModalView
from kivy.uix.screenmanager import Screen
from kivy.uix.scrollview import ScrollView
from kivymd.uix.button import MDRaisedButton
from kivymd.uix.expansionpanel import MDExpansionPanel, MDExpansionPanelOneLine
import subway_info
from datetime import datetime


class Content(BoxLayout):

    def __init__(self, line, direction, station, current_hour, **kwargs):
        super().__init__(**kwargs)
        self.line = line
        self.direction = direction
        self.station = station
        self.current_hour = current_hour
        self.get_closest_arrivals()

    def get_closest_arrivals(self):
        pass
        # schedule = subway_info.get_station_schedule(self.direction, self.station, self.line)


class DirectionInformation(ModalView):

    def __init__(self, line, direction, current_hour):
        super().__init__()
        self.size_hint = (.85, .85)
        self.current_hour = current_hour
        self.stations: dict = subway_info.get_stations(line)
        # self.stations = {'МЕТРОСТАНЦИЯ ГОРНА БАНЯ': '3336', 'МЕТРОСТАНЦИЯ ОВЧА КУПЕЛ II': '3334',
        #                  'МЕТРОСТАНЦИЯ МИЗИЯ/НБУ': '3332', 'МЕТРОСТАНЦИЯ ОВЧА КУПЕЛ': '3330',
        #                  'МЕТРОСТАНЦИЯ ЦАР БОРИС III / КРАСНО СЕЛО': '3328', 'МЕТРОСТАНЦИЯ БУЛ. БЪЛГАРИЯ': '3324',
        #                  'МЕТРОСТАНЦИЯ МЕДИЦИНСКИ УНИВЕРСИТЕТ': '3322', 'МЕТРОСТАНЦИЯ НДК 2': '3320',
        #                  'МЕТРОСТАНЦИЯ СВ. ПАТРИАРХ ЕВТИМИЙ': '3318', 'МЕТРОСТАНЦИЯ ОРЛОВ МОСТ': '3316',
        #                  'МЕТРОСТАНЦИЯ ТЕАТРАЛНА': '3312', 'МЕТРОСТАНЦИЯ ХАДЖИ ДИМИТЪР': '3310'}
        self.line = line
        self.direction = direction
        self.create_expansion_panels_for_each_station()

    def create_expansion_panels_for_each_station(self):
        stations_grid = GridLayout(cols=1, spacing=(0, 10), size_hint_y=None, size_hint_x=None, width=1000)

        for station in self.stations:
            station_id = self.stations[station]
            panel = MDExpansionPanel(panel_cls=MDExpansionPanelOneLine(text=station), icon="subway",
                                     content=Content(self.line, self.direction, station_id, self.current_hour))
            stations_grid.add_widget(panel)
        subway_info.close_driver()
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
        # directions = {'м.Витоша-м.Обеля-м.Летище София': '2666', 'м.Летище София-м.Обеля-м.Витоша': '2667',
        #               'м.Витоша-м.Обеля-м.Бизнес Парк': '2668', 'м.Бизнес Парк-м.Обеля-м.Витоша': '2669'}
        for d in directions:
            button = MDRaisedButton(text=d, font_style="Button", md_bg_color=[.8, .8, .8, 1],
                                    text_color=[.08, .07, .09, 1],
                                    padding=(20, 20),
                                    on_release=lambda x, direction=directions[d]: self.get_current_direction_modal_view(direction)
            self.ids.directions.add_widget(button)

    def reset(self):
        self.ids.directions.clear_widgets()

    def get_departing_times(self):
        pass

    def get_current_direction_modal_view(self, direction):
        view = DirectionInformation(self.line, direction, datetime.now().hour)
        view.open()
