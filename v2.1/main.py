import kivy

from kivy.app import App
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.gridlayout import GridLayout
from kivy.uix.button import Button
from kivy.graphics import Rectangle, RoundedRectangle
from kivy.uix.widget import Widget
from kivy_garden.mapview import MapMarkerPopup, MapView

class Map(MapView):
    def __init__(self, **kwargs):
        coords = [(57, 24.5), (56.9, 24.4)]
        super().__init__(**kwargs)
        for coord in coords:
            m = MapMarkerPopup(lat=coord[0], lon=coord[1])
            m.add_widget(Button(text="Yo!"))
            self.add_marker(m)

class Home(GridLayout, Screen):
    pass

class Notikumi(GridLayout, Screen):
    pass

class Veikals(GridLayout, Screen):
    pass

class FAQ(GridLayout, Screen):
    pass

class ParMums(GridLayout, Screen):
    pass

class Pieslegties(GridLayout, Screen):
    pass

class Registreties(GridLayout, Screen):
    pass

class WindowManager(ScreenManager):
    pass

kivy.require('1.9.1')

kvfile = Builder.load_file("main.kv")

class main2(App):

    def login(self):
        print("login")

    def register(self):
        print("register")

    def build(self):
        return kvfile

if __name__ == "__main__":
    kv = main2()
    kv.run()