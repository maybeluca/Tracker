1) elementi da tracciare per sessione: data, durata, tipologia, (eventualmente presi da dati dell'orologio con zepp os)
2) elementi da tracciare per serie: nome, ripetizioni, peso //solo per work-out in palestra
3) database:
    sessions:   id, date, type, duration_min
    exercises:  id, name, 
    sets:       id, set_number session_id, exercise_id, reps, weight_kg //weight=NULL corpo libero