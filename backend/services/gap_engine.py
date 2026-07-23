from backend.services.scoring import compute_gap_score
from backend.services.trend_analysis import (
    get_trend_from_papers,
    calculate_growth
)
from backend.services.citation_analysis import analyze_papers
from backend.embeddings.similarity_search import (
    search_similar_papers
)
class GapEngine:

    def __init__(self):
        print("Research Gap Engine Initialized")

    def analyze(self, query):

        papers = search_similar_papers(query)

        if not papers:
            return {
                "query": query,
                "error": "No similar papers found."
            }

        trend = get_trend_from_papers(papers)
        growth = calculate_growth(trend)

        citation = analyze_papers(papers)

        semantic_score = papers[0]["similarity"]

        trend_score = min(max(growth / 100, 0), 1)

        citation_score = min(
            citation["average_citations"] / 100,
            1
        )

        bridge_score = 0.5
        graph_score = 0.5

        gap_score = compute_gap_score(
            semantic=semantic_score,
            trend=trend_score,
            citation=citation_score,
            bridge=bridge_score,
            graph=graph_score
        )

        recommendation = (
            "Excellent research opportunity."
            if gap_score >= 80
            else "Promising research direction."
            if gap_score >= 60
            else "Well-established research area."
        )

        return {
            "query": query,
            "semantic_score": round(semantic_score, 3),
            "trend_score": round(trend_score, 3),
            "citation_score": round(citation_score, 3),
            "bridge_score": bridge_score,
            "graph_score": graph_score,
            "gap_score": round(gap_score, 2),
            "recommendation": recommendation,
            "publication_trend": trend,
            "citation_analysis": citation,
            "top_papers": papers
        }

if __name__ == "__main__":

    engine = GapEngine()

    output = engine.analyze(
        input("Enter research topic: ")
    )

    print(output)