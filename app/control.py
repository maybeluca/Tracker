import sqlite3

conn = sqlite3.connect("tracker.db")
print(conn.execute("SELECT * FROM exercises").fetchall())
print(conn.execute("SELECT * FROM sessions").fetchall())
conn.close()