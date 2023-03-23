import sqlite3 as db
with db.connect("sakoplatviju.db") as con:
    cur = con.execute
    cur = con.execute("""CREATE TABLE IF NOT EXISTS Lietotaji(
        id INTEGER PRIMARY KEY,
        lietotajvards TEXT,
        epasts TEXT,
        parole_hash TEXT,
        cash INTEGER
        )""")
    cur = con.execute("""CREATE TABLE IF NOT EXISTS Notikumi(
        id INTEGER PRIMARY KEY,
        nosaukums TEXT,
        latitude FLOAT,
        longitude FLOAT,
        vietas INTEGER
    )""")
    
    cur = con.execute("""CREATE TABLE IF NOT EXISTS Preces(
        id INTEGER PRIMARY KEY,
        nosaukums TEXT,
        cena INTEGER
    )""")
    cur = con.execute("""INSERT OR IGNORE INTO Notikumi(nosaukums, latitude, longitude, vietas) VALUES
        ('Sakopsana1', 26.55, 74, 15),
        ('Testa Sakopsana', 26.7, 73.6, 10)
        """)
    
    cur = con.execute("""INSERT OR IGNORE INTO Preces(nosaukums, cena) VALUES
        ('Prece1', 100),
        ('Prece2', 400),
        ('Prece3', 60),
        ('Prece4', 120),
        ('Prece5', 310),
        ('Prece6', 150)
        """)