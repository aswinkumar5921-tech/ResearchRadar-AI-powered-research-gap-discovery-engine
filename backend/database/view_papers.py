import sqlite3

conn = sqlite3.connect("data/sqlite/research.db")
cursor = conn.cursor()

cursor.execute("SELECT * FROM papers")

rows = cursor.fetchall()

for row in rows:
    print(row)

conn.close()