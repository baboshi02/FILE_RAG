import itertools


def chunk_string(s, size):
    return [s[i : i + size] for i in range(0, len(s), size)]


def parse_to_embedd(list: list, bookname: str):
    return [
        {"_id": "page_" + str(idx), "chunk_text": chunk_text, "book_name": bookname}
        for idx, chunk_text in enumerate(list)
    ]


def chunks(iterable, batch_size=200):
    """A helper function to break an iterable into chunks of size batch_size."""
    it = iter(iterable)
    chunk = tuple(itertools.islice(it, batch_size))
    while chunk:
        yield chunk
        chunk = tuple(itertools.islice(it, batch_size))
