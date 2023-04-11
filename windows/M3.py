from kivy.properties import NumericProperty
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.screenmanager import Screen
from kivymd.uix.expansionpanel import MDExpansionPanel, MDExpansionPanelOneLine


class Content(BoxLayout):
    pass


class M3(Screen):

    def on_enter(self):
        # Test panels
        self.ids.directions.add_widget(MDExpansionPanel(panel_cls=MDExpansionPanelOneLine(text="Text"), icon="apple", content=Content()))
        self.ids.directions.add_widget(MDExpansionPanel(panel_cls=MDExpansionPanelOneLine(text="another"), icon="apple", content=Content()))

    def reset(self):
        self.ids.directions.clear_widgets()