import sqlite3
from datetime import date

TIPI_SESSIONE = ["palestra", "corsa", "camminata", "altro"]

conn = sqlite3.connect("tracker.db")
cur = conn.cursor()

print("Tipo di sessione:")
for i, tipo in enumerate(TIPI_SESSIONE, start=1):
    print(f"{i}) {tipo}")

scelta = int(input("Scegli un numero: "))
tipo = TIPI_SESSIONE[scelta - 1]

durata = int(input("Durata in minuti: "))
oggi = date.today().isoformat()

cur.execute(
    "INSERT INTO sessions (date, type, duration_min) VALUES (?, ?, ?)",
    (oggi, tipo, durata),
)

conn.commit()
cur.execute("SELECT * FROM sessions")
rows = cur.fetchall()
for row in rows:
    print(f"{row[0]}, {row[1]}, {row[2]}, {row[3]}\n")

conn.close()
print("Sessione salvata!")