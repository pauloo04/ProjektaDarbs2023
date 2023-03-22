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
from kivy.uix.screenmanager import NoTransition

class Map(MapView):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        with db.connect("sakoplatviju.db") as con:
            notikumi = con.execute("""SELECT nosaukums, latitude, longitude FROM Notikumi""").fetchall()
            for notikums in notikumi:
                m = MapMarkerPopup(lat=float(notikums[1]), lon=float(notikums[2]))
                m.add_widget(Button(text=notikums[0]))
                self.add_marker(m)

class LOHome(GridLayout, Screen):
    pass

class LONotikumi(GridLayout, Screen):
    pass

class LOVeikals(GridLayout, Screen):
    pass

class LOFAQ(GridLayout, Screen):
    pass

class LOParMums(GridLayout, Screen):
    pass

class LIHome(GridLayout, Screen):
    pass

class LINotikumi(GridLayout, Screen):
    pass

class LIVeikals(GridLayout, Screen):
    pass

class LIFAQ(GridLayout, Screen):
    pass

class LIParMums(GridLayout, Screen):
    pass

class Pieslegties(GridLayout, Screen):
    email = ObjectProperty(None)
    pwd = ObjectProperty(None)

    def login(self):
        global user_logon_email
        global user_logon_id
        global user_logon_user
        if self.email.text and self.pwd.text:
            with db.connect("sakoplatviju.db") as con:
                iev_email = self.email.text
                iev_pwd = self.pwd.text
                atrasta = con.execute("""SELECT id, parole_hash FROM Lietotaji WHERE epasts=?""", (iev_email,)).fetchall()
                if atrasta:
                    print(atrasta)
                    if atrasta[0][1] == iev_pwd:
                        self.noti.text = "Veiksmīga pieslēgšanās!"
                        sm.current = "lihome"
                        user_logon_id = atrasta[0][0]
                        user_logon_user = atrasta[0][1]
                        user_logon_email = iev_email
                    else:
                        self.noti.text = "Nepareiza parole!"
                else:
                    self.noti.text = "Profils nepastāv!"
        else:
            self.noti.text = "Lūdzu aizpildiet visus laukus!"

class Registreties(GridLayout, Screen):
    user = ObjectProperty(None)
    email = ObjectProperty(None)
    pwd = ObjectProperty(None)
    pwdc = ObjectProperty(None)
    noti = ObjectProperty(None)

    def signup(self):
        if self.user.text and self.email.text and self.pwd.text and self.pwdc.text:
            with db.connect("sakoplatviju.db") as con:
                ievaditais = self.email.text
                registretie = con.execute("SELECT epasts FROM Lietotaji").fetchall()
                pastav = False
                for epasts in registretie:
                    if epasts[0].strip(",") == ievaditais:
                        pastav = True
                        break
                    if not pastav:
                        if self.pwd.text == self.pwdc.text:
                            con.execute("""INSERT INTO Lietotaji(vards, epasts, parole_hash) values (?, ?, ?)""", (self.email.text, self.email.text, self.pwd.text))
                            self.noti.text = f"Veiksmigi piereģistrēts ({self.email.text}, {self.pwd.text})!"
                        else:
                            self.noti.text = "Paroles nesakrīt!"
                    else:
                        self.noti.text = "E-pasts jau reģistrēts!"
        else:
            self.noti.text = "Lūdzu aizpildiet visus laukus!"

class Profils(GridLayout, Screen):
    user = ObjectProperty(None)
    cash = ObjectProperty(None)

    def update_label(self):
        try:
            self.user.text = user_logon_user
            print(user_logon_user)
        except:
            pass

class WindowManager(ScreenManager):
    pass

kivy.require('1.9.1')

kvfile = Builder.load_file("main.kv")
sm = WindowManager(transition=NoTransition())

sm.add_widget(LOHome(name="lohome"))
sm.add_widget(LONotikumi(name="lonotikumi"))
sm.add_widget(LOVeikals(name="loveikals"))
sm.add_widget(LOFAQ(name="lofaq"))
sm.add_widget(LOParMums(name="loparmums"))
sm.add_widget(Pieslegties(name="pieslegties"))
sm.add_widget(Registreties(name="registreties"))
sm.add_widget(LIHome(name="lihome"))
sm.add_widget(LINotikumi(name="linotikumi"))
sm.add_widget(LIVeikals(name="liveikals"))
sm.add_widget(LIFAQ(name="lifaq"))
sm.add_widget(LIParMums(name="liparmums"))
sm.add_widget(Profils(name="profils"))

user_logon_user = None
user_logon_email = None
user_logon_id = None

class main2(App):
    def build(self):
        return sm

if __name__ == "__main__":
    kv = main2()
    kv.run()