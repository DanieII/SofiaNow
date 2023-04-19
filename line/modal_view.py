import threading
from kivy.clock import Clock
from kivy.lang import Builder
from kivy.metrics import dp
from kivy.uix.gridlayout import GridLayout
from kivy.uix.modalview import ModalView
from kivy.uix.scrollview import ScrollView
from kivymd.uix.expansionpanel import MDExpansionPanel, MDExpansionPanelOneLine
import subway_info
from line.station_content import Content


Builder.load_file("kv_files/direction_information.kv")
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
        stations_grid = GridLayout(cols=1, spacing=(0, dp(15)), size_hint=(None, None), width=self.width)

        for station, arrivals in self.stations_with_times.items():
            station, *station_name = station.split()
            panel = MDExpansionPanel(panel_cls=MDExpansionPanelOneLine(text=" ".join(station_name)), icon="subway",
                                     content=Content(station, arrivals))
            stations_grid.add_widget(panel)

        stations_grid.bind(minimum_height=stations_grid.setter('height'))

        scroll_view = ScrollView(do_scroll_x=False)
        scroll_view.add_widget(stations_grid)

        self.add_widget(scroll_view)
