import sqlite3

DB_PATH = "data/sqlite/research.db"

conn = sqlite3.connect(DB_PATH)
cursor = conn.cursor()

cursor.execute("""
SELECT id, title, abstract
FROM papers
""")

papers = cursor.fetchall()

print(f"Loaded {len(papers)} papers")

for paper in papers[:5]:
    print("-" * 50)
    print("ID:", paper[0])
    print("Title:", paper[1])
    print("Abstract Preview:")

    if paper[2]:
        print(paper[2][:300])
    else:
        print("No abstract")

conn.close()