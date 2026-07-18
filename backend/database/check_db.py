import sqlite3

conn = sqlite3.connect("data/sqlite/research.db")
cursor = conn.cursor()

cursor.execute("SELECT COUNT(*) FROM papers")
print("Total papers:", cursor.fetchone()[0])

cursor.execute("""
SELECT title, publication_year, cited_by_count
FROM papers
LIMIT 10
""")

for row in cursor.fetchall():
    print(row)

conn.close()