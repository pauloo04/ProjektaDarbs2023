import sqlite3 as db

user_user = input("Ievadiet lietotāja lietotājvārdu, kuram vēlaties piešķirt kredītus: ")
with db.connect("sakoplatviju.db") as con:
    lietotajs = con.execute("Select * from Lietotaji where lietotajvards = ?", (user_user,))
    if lietotajs:
        try:
            summa = int(input("Ievadiet cik kredītus vēlaties piešķirt šim lietotājam: "))
            current = con.execute("Select cash from Lietotaji where lietotajvards = ?", (user_user,)).fetchall()
            con.execute("Update Lietotaji set cash = ? where lietotajvards = ?", (current[0][0] + summa, user_user))
            con.commit()
        except ValueError:
            print("Nepareizi ievaddati!")
    else:
        print("Lietotājs nepastāv!")