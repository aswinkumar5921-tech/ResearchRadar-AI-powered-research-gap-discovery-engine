import sqlite3
from collections import defaultdict

DB_PATH = "data/sqlite/research.db"


def get_topic_trend(topic: str):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute("""
        SELECT p.publication_year
        FROM papers p
        JOIN paper_concepts pc
            ON p.id = pc.paper_id
        JOIN concepts c
            ON pc.concept_id = c.id
        WHERE LOWER(c.name) LIKE ?
        ORDER BY p.publication_year
    """, (f"%{topic.lower()}%",))

    years = cursor.fetchall()
    conn.close()

    trend = defaultdict(int)

    for (year,) in years:
        if year is not None:
            trend[year] += 1

    return dict(sorted(trend.items()))

def calculate_growth(trend):

    years = sorted(trend.keys())

    if len(years) < 2:
        return 0

    first = trend[years[0]]
    last = trend[years[-1]]

    if first == 0:
        return 100

    return ((last - first) / first) * 100

if __name__ == "__main__":

    topic = input("Enter topic: ")

    trend = get_topic_trend(topic)

    print("\nPublication Trend\n")

    if not trend:
        print("No papers found.")
    else:
        for year, count in trend.items():
            print(f"{year}: {count}")
        growth = calculate_growth(trend)
        print(f"\nGrowth: {growth:.2f}%")