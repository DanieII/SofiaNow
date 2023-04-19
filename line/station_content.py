from kivy.lang import Builder
from kivy.uix.gridlayout import GridLayout
from kivymd.uix.label import MDLabel
from kivymd.uix.list import OneLineListItem


class OneLineListItemAligned(OneLineListItem):
    def __init__(self, halign, **kwargs):
        super(OneLineListItemAligned, self).__init__(**kwargs)
        self.ids._lbl_primary.halign = halign


Builder.load_file("kv_files/direction_information.kv")
class Content(GridLayout):

    def __init__(self, *args, **kwargs):
        super().__init__(**kwargs)
        self.station, self.arrivals = args
        for i, v in enumerate(self.arrivals.items(), 1):
            hour, arrivals = v
            current_list = self.ids.list1 if i == 1 else self.ids.list2
            current_list.add_widget(MDLabel(text=f"{hour}\n", halign='center'))

            for arrival in arrivals:
                item = OneLineListItemAligned(halign="center", text=f"{' ' * (len(arrival) // 2)}{arrival}")
                current_list.add_widget(item)
