from backend.config.settings import GAP_WEIGHTS

def normalize(value, minimum, maximum):

    if maximum == minimum:
        return 0

    return (value - minimum) / (maximum - minimum)


def compute_gap_score(
    semantic,
    trend,
    citation,
    bridge,
    graph,
):

    score = (
        GAP_WEIGHTS["semantic"] * semantic
        + GAP_WEIGHTS["trend"] * trend
        + GAP_WEIGHTS["citation"] * citation
        + GAP_WEIGHTS["bridge"] * bridge
        + GAP_WEIGHTS["graph"] * graph
    )

    return round(score * 100, 2)