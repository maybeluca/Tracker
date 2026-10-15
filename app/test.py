import sqlite3
from datetime import date

from main import find_exercise, conn, cur, record_session
conn = sqlite3.connect("tracker.db")
cur = conn.cursor()
record_session()
conn.commit()
conn.close()