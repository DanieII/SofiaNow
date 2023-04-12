from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.modalview import ModalView
from kivy.uix.screenmanager import Screen
from kivy.uix.scrollview import ScrollView
from kivymd.uix.button import MDRaisedButton
from kivymd.uix.expansionpanel import MDExpansionPanel, MDExpansionPanelOneLine
import subway_info


class Content(BoxLayout):
    pass


class DirectionInformation(ModalView):

    def __init__(self, line, direction):
        super().__init__()
        self.size_hint = (.85, .85)
        self.line = line
        self.direction = direction
        # self.stations: dict = subway_info.get_stations(line)
        self.stations = {'МЕТРОСТАНЦИЯ ГОРНА БАНЯ': '3336', 'МЕТРОСТАНЦИЯ ОВЧА КУПЕЛ II': '3334',
                         'МЕТРОСТАНЦИЯ МИЗИЯ/НБУ': '3332', 'МЕТРОСТАНЦИЯ ОВЧА КУПЕЛ': '3330',
                         'МЕТРОСТАНЦИЯ ЦАР БОРИС III / КРАСНО СЕЛО': '3328', 'МЕТРОСТАНЦИЯ БУЛ. БЪЛГАРИЯ': '3324',
                         'МЕТРОСТАНЦИЯ МЕДИЦИНСКИ УНИВЕРСИТЕТ': '3322', 'МЕТРОСТАНЦИЯ НДК 2': '3320',
                         'МЕТРОСТАНЦИЯ СВ. ПАТРИАРХ ЕВТИМИЙ': '3318', 'МЕТРОСТАНЦИЯ ОРЛОВ МОСТ': '3316',
                         'МЕТРОСТАНЦИЯ ТЕАТРАЛНА': '3312', 'МЕТРОСТАНЦИЯ ХАДЖИ ДИМИТЪР': '3310'}
        self.create_expansion_panels_for_each_station()

    def create_expansion_panels_for_each_station(self):
        stations_grid = GridLayout(cols=1, spacing=(0, 10), size_hint_y=None, size_hint_x=None, width=1000)

        for station in self.stations:
            panel = MDExpansionPanel(panel_cls=MDExpansionPanelOneLine(text=station), icon="subway", content=Content())
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
        # directions = subway_info.get_directions(self.line)
        directions = {'м.Витоша-м.Обеля-м.Летище София': '2666', 'м.Летище София-м.Обеля-м.Витоша': '2667',
                      'м.Витоша-м.Обеля-м.Бизнес Парк': '2668', 'м.Бизнес Парк-м.Обеля-м.Витоша': '2669'}
        for d in directions:
            button = MDRaisedButton(text=d, font_style="Button", md_bg_color=[.8, .8, .8, 1], text_color=[.08, .07, .09, 1],
                                    on_release=lambda x, direction=d: self.get_current_direction_modal_view(direction))
            self.ids.directions.add_widget(button)

    def reset(self):
        self.ids.directions.clear_widgets()

    def get_departing_times(self):
        pass

    def get_current_direction_modal_view(self, direction):
        view = DirectionInformation(self.line, direction)
        view.open()
