def chunk_string(s, size):
    return [s[i : i + size] for i in range(0, len(s), size)]


def parse_to_embedd(list):
    return [
        {"_id": "page_" + str(idx), "chunk_text": chunk_text}
        for idx, chunk_text in enumerate(list)
    ]
