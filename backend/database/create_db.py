import sqlite3

conn = sqlite3.connect("data/sqlite/research.db")
cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS papers (

    id INTEGER PRIMARY KEY AUTOINCREMENT,

    openalex_id TEXT UNIQUE,

    title TEXT,

    abstract TEXT,

    publication_year INTEGER,

    doi TEXT,

    cited_by_count INTEGER,

    language TEXT,

    paper_type TEXT,

    created_date TEXT
)
""")

conn.commit()
conn.close()

print("Database created successfully!")