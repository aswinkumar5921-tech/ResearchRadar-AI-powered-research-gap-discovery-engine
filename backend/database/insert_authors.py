def insert_authors(cursor, paper_db_id, authorships):

    if not authorships:
        return

    for author_info in authorships:

        author = author_info.get("author")

        if not author:
            continue

        name = author.get("display_name")

        if not name:
            continue

        # Insert author if new
        cursor.execute("""
        INSERT OR IGNORE INTO authors(name)
        VALUES (?)
        """, (name,))

        # Get author id
        cursor.execute("""
        SELECT id FROM authors
        WHERE name=?
        """, (name,))

        author_id = cursor.fetchone()[0]

        # Create relationship
        cursor.execute("""
        INSERT OR IGNORE INTO paper_authors
        (paper_id, author_id)
        VALUES (?, ?)
        """, (paper_db_id, author_id))