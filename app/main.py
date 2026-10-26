import sqlite3
from datetime import date, datetime

TIPI_SESSIONE = ["palestra", "corsa", "camminata", "altro"]

conn = sqlite3.connect("tracker.db")
cur = conn.cursor()

def ask_int_float(prompt, min1, min2, max1=None, max2=None):
    while True:
        try:
            intVar, floatVar = input(prompt).split()
            intVar=int(intVar)
            floatVar=floatVar.replace(",", ".")
            floatVar=float(floatVar)
        except ValueError:
            print("Inserisci due valori separati da uno spazio.")
            continue
        if intVar < min1 or floatVar < min2 or (max1 is not None and intVar>max1 or max2 is not None and floatVar>max2):
            if max1 is not None or max2 is not None:
                print(f"inserire un intero compreso tra {min1} e {max1} e un decimale compreso tra {min2} e {max2}.")
            else:    
                print(f"inserire un intero maggiore o uguale a {min1} e un decimale maggiore di {min2}.")
            continue
        return intVar, floatVar
    
def ask_int(prompt, minimo, massimo=None):
    while True:
        try:
            scelta = int(input(prompt))
        except ValueError:
            print("Inserisci un numero valido.")
            continue
        if scelta < minimo or (massimo is not None and scelta > massimo):
            if massimo is not None:
                print(f"Scegli un numero da {minimo} a {massimo}")
            else:
                print(f"Scegli un numero maggiore o uguale a {minimo}")
            continue
        return scelta

"""def record_session():
    print("Tipo di sessione:")
    for i, tipo in enumerate(TIPI_SESSIONE, start=1):
        print(f"{i}) {tipo}")
    scelta = ask_int("Scegli un numero: ", 1, len(TIPI_SESSIONE))
    tipo = TIPI_SESSIONE[scelta - 1]
    oggi = date.today().isoformat()

    cur.execute(
        "INSERT INTO sessions (date, type, duration_min) VALUES (?, ?, ?)",
        (oggi, tipo, None),
    )
    session_id = cur.lastrowid
    if tipo=="palestra":
        inizio = datetime.now()
        try:
            while True:
                exercise_id = find_exercise(session_id)
                if exercise_id is False:
                    break
                reps, weight=ask_int_float("Inserisci il numero di ripetizioni e il peso (r p): ", 1, 0)
                record_set(session_id, exercise_id, reps, weight)
        finally:
            minuti=round((datetime.now()-inizio).total_seconds()/60)
            save_duration(session_id, minuti)
    else:
        minuti=ask_int("Inserisci la durata in minuti: ", 1)
        save_duration(session_id, minuti)
    print("Sessione salvata!")"""

def save_duration(session_id, minuti):
    cur.execute("UPDATE sessions SET duration_min = ? WHERE id = ?", (minuti, session_id))
    conn.commit()

def search_exercises(query):
    cur.execute("SELECT id, name FROM exercises WHERE name LIKE ?", (f"%{query}%",))
    results = cur.fetchall()
    return results;

def create_exercise(query):
    cur.execute("INSERT INTO exercises (name) VALUES (?)", (f"%{query}%",))
    return True

def last_exercise_id():
    return cur.lastrowid

# -----TEST------
print(f"esercizi trovati:\n{search_exercises("panca")}")
create_exercise("esercizio prova")
print(f"Id ultimo esercizio: {last_exercise_id}")

def find_exercise(session_id):
    print("0) Prosegui\n1) Ripeti esercizio\n2)Ripeti esercizio con dati diversi\n3) Termina allenamento\n")
    c=ask_int("Scelta: ", 0, 3,)
    if c==0:
        es=input("Esercizio: ").strip().lower()
        cur.execute("SELECT id, name FROM exercises WHERE name LIKE ?", (f"%{es}%",))
        results = cur.fetchall()
        if results:
            print("Esercizi trovati:")
            for i, (ex_id, name) in enumerate(results, start=1):
                print(f"{i}) {name} (ID: {ex_id})")
            print("0) Crea Esercizio")
            scelta = ask_int("Scegli l'esercizio: ", 0, len(results))
            if scelta==0:
                print(f"Creare l'esercizio {es} ? s/n ")
                if input().strip().lower() == "s":
                    cur.execute("INSERT INTO exercises (name) VALUES (?)", (es,))
                    exercise_id = cur.lastrowid
                else:
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
    else: 
        print("Allenamento terminato.")
        return False
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
