import sqlite3

conn = sqlite3.connect("data/sqlite/research.db")
cursor = conn.cursor()
cursor.execute("SELECT COUNT(*) FROM papers")

print("Total Papers:", cursor.fetchone()[0])
cursor.execute("""
SELECT COUNT(*)
FROM papers
WHERE abstract IS NOT NULL
AND abstract != ''
""")

print("Papers with Abstract:", cursor.fetchone()[0])
cursor.execute("""
SELECT AVG(cited_by_count)
FROM papers
""")

print("Average Citations:", round(cursor.fetchone()[0], 2))
cursor.execute("""
SELECT publication_year,
COUNT(*)

FROM papers

GROUP BY publication_year

ORDER BY publication_year DESC
""")

print("\nPapers by Year")

for row in cursor.fetchall():
    print(row)
cursor.execute("""
SELECT venue,
COUNT(*)

FROM papers

GROUP BY venue

ORDER BY COUNT(*) DESC

LIMIT 10
""")

print("\nTop Venues")

for row in cursor.fetchall():
    print(row)
    
cursor.execute("""
SELECT language,
COUNT(*)

FROM papers

GROUP BY language
""")

print("\nLanguages")

for row in cursor.fetchall():
    print(row)
    
conn.close()    