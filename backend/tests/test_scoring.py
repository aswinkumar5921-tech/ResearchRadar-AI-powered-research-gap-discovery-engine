from backend.services.scoring import compute_gap_score

score = compute_gap_score(
    semantic=0.90,
    trend=0.80,
    citation=0.60,
    bridge=0.70,
    graph=0.50,
)

print(score)