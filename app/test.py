import sqlite3
from datetime import date

from main import find_exercise, conn, cur
conn = sqlite3.connect("tracker.db")
cur = conn.cursor()
print(find_exercise())
conn.commit()
conn.close()