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
        while True:
            exercise_id = find_exercise(session_id)
            if exercise_id is False:
                break
            reps, weight = input("Inserisci ripetizioni e peso separati da uno spazio: ").split()
            record_set(session_id, exercise_id, int(reps), float(weight))
    print("Sessione salvata!")

def find_exercise(session_id):
    print("0) Prosegui\n1) Ripeti esercizio\n2) Termina allenamento\n")
    c=int(input("Scelta: "))
    if c==0:
        es=input("Esercizio: ").strip().lower()
        cur.execute("SELECT id, name FROM exercises WHERE name LIKE ?", (f"%{es}%",))
        results = cur.fetchall()
        print("0) Crea Esercizio")
        if results:
            print("Esercizi trovati:")
            for i, (ex_id, name) in enumerate(results, start=1):
                print(f"{i}) {name} (ID: {ex_id})")
            scelta = int(input("Scegli un numero: "))
            if scelta==0:
                print(f"Creare l'esercizio {es} ? s/n ")
                if input().strip().lower() == "s":
                    cur.execute("INSERT INTO exercises (name) VALUES (?)", (es,))
                    exercise_id = cur.lastrowid
                else:
                    return find_exercise(session_id)
            elif (scelta < 0 or scelta > len(results)):
                print("Scelta non valida.\n")
                return find_exercise(session_id)
            else:
                exercise_id = results[scelta - 1][0]
        else:
            print(f"Nessun esercizio trovato. Creare l'esercizio {es} ? s/n ")
            if input().strip().lower() == "s":
                cur.execute("INSERT INTO exercises (name) VALUES (?)", (es,))
                exercise_id = cur.lastrowid
            else:
                return find_exercise(session_id)
    elif c==1:
        cur.execute("SELECT exercise_id FROM sets WHERE session_id = ? ORDER BY id DESC LIMIT 1", (session_id,))
        last_exercise = cur.fetchone()
        if last_exercise:
            exercise_id = last_exercise[0]
        else:
            print("Nessun esercizio precedente trovato.\n")
            return find_exercise(session_id)
    elif c==2:
        print("Allenamento terminato.")
        return False
    else:
        print("Scelta non valida.\n")
        return find_exercise(session_id)

    conn.commit()
    return exercise_id

def record_set(session_id, exercise_id, reps, weight):
    cur.execute(
        "SELECT COUNT(*) from sets where session_id = ? AND exercise_id = ?"
        ,
        (session_id, exercise_id)
    )
    conteggio=cur.fetchone()[0]
    cur.execute(
        "INSERT INTO sets (session_id, exercise_id, set_number, reps, weight_kg ) VALUES (?, ?, ?, ?, ?)",
        (session_id, exercise_id, conteggio + 1, reps, weight )
    )
    conn.commit()


if __name__ == "__main__":
    record_session()
    conn.commit()
    conn.close()
