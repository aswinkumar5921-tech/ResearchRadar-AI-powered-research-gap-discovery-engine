import sqlite3
import os

# Create folder if it doesn't exist
os.makedirs("data/sqlite", exist_ok=True)

conn = sqlite3.connect("data/sqlite/research.db")
cursor = conn.cursor()

# -------------------- Papers --------------------
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
    venue TEXT
)
""")

# -------------------- Authors --------------------
cursor.execute("""
CREATE TABLE IF NOT EXISTS authors (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT UNIQUE
)
""")

# -------------------- Concepts --------------------
cursor.execute("""
CREATE TABLE IF NOT EXISTS concepts (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT UNIQUE,
    score REAL
)
""")

# -------------------- Paper ↔ Author --------------------
cursor.execute("""
CREATE TABLE IF NOT EXISTS paper_authors (
    paper_id INTEGER,
    author_id INTEGER,
    PRIMARY KEY (paper_id, author_id)
)
""")

# -------------------- Paper ↔ Concept --------------------
cursor.execute("""
CREATE TABLE IF NOT EXISTS paper_concepts (
    paper_id INTEGER,
    concept_id INTEGER,
    PRIMARY KEY (paper_id, concept_id)
)
""")

conn.commit()
conn.close()

print("Database created successfully!")