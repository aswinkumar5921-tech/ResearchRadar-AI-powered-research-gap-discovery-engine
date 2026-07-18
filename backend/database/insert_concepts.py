def insert_concepts(cursor, paper_db_id, concepts):
    print(f"Processing {len(concepts)} concepts for paper {paper_db_id}")

    if not concepts:
        return

    for concept in concepts:

        name = concept.get("display_name")

        if not name:
            continue

        # Insert concept if it doesn't exist
        cursor.execute("""
            INSERT OR IGNORE INTO concepts(name)
            VALUES (?)
        """, (name,))

        # Get concept ID
        cursor.execute("""
            SELECT id FROM concepts
            WHERE name = ?
        """, (name,))
        concept_id = cursor.fetchone()[0]

        # Link paper to concept
        cursor.execute("""
            INSERT OR IGNORE INTO paper_concepts
            (paper_id, concept_id)
            VALUES (?, ?)
        """, (paper_db_id, concept_id))