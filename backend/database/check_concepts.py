import sqlite3

conn = sqlite3.connect("data/sqlite/research.db")
cursor = conn.cursor()

cursor.execute("SELECT COUNT(*) FROM concepts")
print("Concepts:", cursor.fetchone()[0])

cursor.execute("SELECT COUNT(*) FROM paper_concepts")
print("Relationships:", cursor.fetchone()[0])

conn.close()