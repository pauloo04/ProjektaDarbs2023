import sqlite3 as db
with db.connect("sakoplatviju.db") as con:
    cur = con.execute
    cur = con.execute("""CREATE TABLE IF NOT EXISTS Lietotaji(
        id INTEGER PRIMARY KEY,
        vards TEXT,
        epasts TEXT,
        parole_hash TEXT
        )""")
    cur = con.execute("""CREATE TABLE IF NOT EXISTS Notikumi(
        id INTEGER PRIMARY KEY,
        nosaukums TEXT,
        latitude FLOAT,
        longitude FLOAT,
        vietas INTEGER
    )""")
    cur = con.execute("""INSERT OR IGNORE INTO Notikumi(nosaukums, latitude, longitude, vietas) VALUES
        ('Sakopsana1', 26.55, 74, 15),
        ('Testa Sakopsana', 26.7, 73.6, 10)
        """)