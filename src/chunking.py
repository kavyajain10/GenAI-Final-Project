import re


def chunk_contract(text, max_words=250, overlap_words=50):
    """Split a contract into chunks of up to `max_words` words.

    Splits on blank lines (CUAD paragraphs), merges short paragraphs together,
    and cuts very long paragraphs into overlapping windows.
    Each chunk keeps its character offsets so text[start:end] == chunk["text"].
    """
    paras = [(m.start(), m.end())
             for m in re.finditer(r"\S(?:.*?\S)?(?=\n\s*\n|\Z)", text, flags=re.S)]

    pieces = []
    for s, e in paras:
        words = [(m.start() + s, m.end() + s) for m in re.finditer(r"\S+", text[s:e])]
        if len(words) <= max_words:
            pieces.append((s, e, len(words)))
            continue
        step = max_words - overlap_words
        for i in range(0, len(words), step):
            w = words[i:i + max_words]
            pieces.append((w[0][0], w[-1][1], len(w)))
            if i + max_words >= len(words):
                break

    chunks, cur = [], None
    for s, e, n in pieces:
        if cur and cur[2] + n <= max_words:
            cur = (cur[0], e, cur[2] + n)
        else:
            if cur:
                chunks.append(cur)
            cur = (s, e, n)
    if cur:
        chunks.append(cur)

    return [{"text": text[s:e], "start": s, "end": e} for s, e, _ in chunks]