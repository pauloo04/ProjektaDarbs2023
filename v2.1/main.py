import kivy
import sqlite3 as db

from kivy.app import App
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.gridlayout import GridLayout
from kivy.uix.button import Button
from kivy.properties import ObjectProperty
from kivy.graphics import Rectangle, RoundedRectangle
from kivy.uix.widget import Widget
from kivy_garden.mapview import MapMarkerPopup, MapView

class Map(MapView):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        with db.connect("sakoplatviju.db") as con:
            notikumi = con.execute("""SELECT nosaukums, latitude, longitude FROM Notikumi""").fetchall()
            for notikums in notikumi:
                m = MapMarkerPopup(lat=float(notikums[1]), lon=float(notikums[2]))
                m.add_widget(Button(text=notikums[0]))
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
    email = ObjectProperty(None)
    pwd = ObjectProperty(None)

    def signup(self):
        with db.connect("sakoplatviju.db") as con:
            ievaditais = self.email.text
            registretie = con.execute("SELECT epasts FROM Lietotaji").fetchall()
            pastav = False
            for epasts in registretie:
                if epasts[0].strip(",") == ievaditais:
                    pastav = True
                    break
            if not pastav:
                con.execute("""INSERT INTO Lietotaji(vards, epasts, parole_hash) values (?, ?, ?)""", ("Pagaidam nav", self.email.text, self.pwd.text))
                print(f"Veiksmigi piereģistrēts ({self.email.text}, {self.pwd.text})!")
            else:
                print("E-pasts jau reģistrēts!")


class WindowManager(ScreenManager):
    pass

kivy.require('1.9.1')

kvfile = Builder.load_file("main.kv")

class main2(App):

    def build(self):
        return kvfile

if __name__ == "__main__":
    kv = main2()
    kv.run()