import sqlite3

DB_PATH = "data/sqlite/research.db"


def analyze_topic(topic: str):

    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute("""
        SELECT
            p.title,
            p.publication_year,
            p.cited_by_count
        FROM papers p
        JOIN paper_concepts pc
            ON p.id = pc.paper_id
        JOIN concepts c
            ON pc.concept_id = c.id
        WHERE LOWER(c.name) LIKE ?
    """, (f"%{topic.lower()}%",))

    rows = cursor.fetchall()

    conn.close()

    if not rows:
        return None

    total_citations = sum(r[2] or 0 for r in rows)
    average = total_citations / len(rows)

    recent = [
        r for r in rows
        if r[1] is not None and r[1] >= 2023
    ]

    recent_low = [
        r for r in recent
        if (r[2] or 0) < 10
    ]

    return {
        "papers": len(rows),
        "average_citations": average,
        "recent_papers": len(recent),
        "recent_low_citation": len(recent_low),
        "details": rows
    }

def analyze_papers(papers):

    if not papers:
        return None

    total = len(papers)

    total_citations = sum(
        p.get("citations", 0)
        for p in papers
    )

    average = total_citations / total

    recent = [
        p
        for p in papers
        if p.get("year") and p["year"] >= 2023
    ]

    recent_low = [
        p
        for p in recent
        if p.get("citations", 0) < 10
    ]

    return {
        "papers": total,
        "average_citations": average,
        "recent_papers": len(recent),
        "recent_low_citation": len(recent_low)
    }
if __name__ == "__main__":

    topic = input("Enter topic: ")

    result = analyze_topic(topic)

    if not result:
        print("No papers found.")
    else:

        print("\nCitation Analysis")
        print("-" * 40)

        print("Total Papers:", result["papers"])
        print("Average Citations:", round(result["average_citations"], 2))
        print("Recent Papers:", result["recent_papers"])
        print("Recent Low Citation Papers:", result["recent_low_citation"])