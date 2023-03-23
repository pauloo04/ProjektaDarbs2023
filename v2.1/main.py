import kivy
import sqlite3 as db

from kivy.app import App
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.gridlayout import GridLayout
from kivy.uix.button import Button
from kivy.properties import ObjectProperty, StringProperty, BooleanProperty
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

    cash = StringProperty(" ")
    noti = ObjectProperty(None)

    def on_pre_enter(self, *args):
        self.update_labels()

    def update_labels(self):
        self.cash = str(user_logon_cash) + "C"
    
    def pirkt(self, prece_id):
        global user_logon_cash
        with db.connect("sakoplatviju.db") as con:
            prece = con.execute("Select nosaukums, cena from Preces where id=?", (prece_id,)).fetchall()
            if user_logon_cash >= prece[0][1]:
                self.noti.text = f"Veiksmīgi nopirkts {prece[0][0]} par {prece[0][1]}C!"
                user_logon_cash -= prece[0][1]
                con.execute("""Update Lietotaji set cash = ? where id = ?""", (user_logon_cash, user_logon_id))
                self.update_labels()
            else:
                self.noti.text = "Nepietiek līdzekļu!"

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
        global user_logon_cash
        if self.email.text and self.pwd.text:
            with db.connect("sakoplatviju.db") as con:
                iev_email = self.email.text
                iev_pwd = self.pwd.text
                atrasta = con.execute("""SELECT id, lietotajvards, parole_hash, cash FROM Lietotaji WHERE epasts=?""", (iev_email,)).fetchall()
                if atrasta:
                    if atrasta[0][2] == iev_pwd:
                        self.noti.text = "Veiksmīga pieslēgšanās!"
                        sm.current = "lihome"
                        user_logon_id = atrasta[0][0]
                        user_logon_user = atrasta[0][1]
                        user_logon_email = iev_email
                        user_logon_cash = atrasta[0][3]
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
                ievaditais_user = self.user.text
                ievaditais_email = self.email.text
                registretie = con.execute("SELECT lietotajvards, epasts FROM Lietotaji").fetchall()
                pastav_email = False
                for lietotajvards, epasts in registretie:
                    if epasts == ievaditais_email:
                        pastav_email = True
                        break
                if not pastav_email:
                    pastav_user = False
                    for lietotajvards, epasts in registretie:
                        if lietotajvards == ievaditais_user:
                            pastav_user = True
                            break
                    if not pastav_user:
                        if self.pwd.text == self.pwdc.text:
                            con.execute("""INSERT INTO Lietotaji(lietotajvards, epasts, parole_hash, cash) values (?, ?, ?, ?)""", (self.user.text, self.email.text, self.pwd.text, 0))
                            self.noti.text = f"Veiksmigi piereģistrēts {self.user.text}!"
                        else:
                            self.noti.text = "Paroles nesakrīt!"
                    else:
                        self.noti.text = "Lietotājvārds aizņemts!"
                else:
                    self.noti.text = "E-pasts jau reģistrēts!"
        else:
            self.noti.text = "Lūdzu aizpildiet visus laukus!"

class Profils(GridLayout, Screen):
    cash = StringProperty(" ")
    changeuser = BooleanProperty(False)
    changeemail = BooleanProperty(False)
    changeusertext = StringProperty("Mainīt")
    changeemailtext = StringProperty("Mainīt")
    userfield = ObjectProperty(None)
    emailfield = ObjectProperty(None)

    def on_pre_enter(self, *args):
        self.update_labels()

    def update_labels(self):
        self.userfield.text = user_logon_user
        self.cash = str(user_logon_cash) + "C"
        self.emailfield.text = user_logon_email
    
    def change_user(self):
        global user_logon_user
        if self.changeusertext == "Saglabāt":
            with db.connect("sakoplatviju.db") as con:
                con.execute("""Update Lietotaji set lietotajvards = ? where id = ?""", (self.userfield.text, user_logon_id))
                user_logon_user = self.userfield.text
                con.commit()
        self.changeuser = not self.changeuser
        self.changeusertext = "Mainīt" if self.changeusertext == "Saglabāt" else "Saglabāt"
    
    def change_email(self):
        global user_logon_email
        if self.changeemailtext == "Saglabāt":
            with db.connect("sakoplatviju.db") as con:
                con.execute("""Update Lietotaji set epasts = ? where id = ?""", (self.emailfield.text, user_logon_id))
                user_logon_email = self.emailfield.text
                con.commit()
        self.changeemail = not self.changeemail
        self.changeemailtext = "Mainīt" if self.changeemailtext == "Saglabāt" else "Saglabāt"

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