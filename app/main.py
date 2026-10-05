import sqlite3
from datetime import date

TIPI_SESSIONE = ["palestra", "corsa", "camminata", "altro"]

conn = sqlite3.connect("tracker.db")
cur = conn.cursor()

def record_session():
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
    session_id = cur.lastrowid
    if tipo=="palestra":
            record_exercises(session_id)
    print("Sessione salvata!")

def record_exercises(session_id):
    exercise_id = find_exercise()
    

def find_exercise():
    es=input("Esercizio: ").strip().lower()
    cur.execute("SELECT id, name FROM exercises WHERE name LIKE ?", (f"%{es}%",))
    results = cur.fetchall()
    if results:
        print("Esercizi trovati:")
        for i, (ex_id, name) in enumerate(results, start=1):
            print(f"{i}) {name} (ID: {ex_id})")
        scelta = int(input("Scegli un numero: "))
        exercise_id = results[scelta - 1][0]
    else:
        cur.execute("INSERT INTO exercises (name) VALUES (?)", (es,))
        exercise_id = cur.lastrowid
    conn.commit()
    return exercise_id

if __name__ == "__main__":
    record_session()
    conn.commit()
    conn.close()
