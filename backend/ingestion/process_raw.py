def reconstruct_abstract(inverted_index):
    if not inverted_index:
        return ""

    words = []

    for word, positions in inverted_index.items():
        for pos in positions:
            words.append((pos, word))

    words.sort()

    return " ".join(word for pos, word in words)