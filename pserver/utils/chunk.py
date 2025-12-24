import itertools
from pinecone.db_data import Index
from pinecone import Pinecone, PineconeApiException
from config import PC_MODEL, PINECONE_API_KEY
from fastapi import HTTPException


def chunk_pages(s, size):
    return [s[i : i + size] for i in range(0, len(s), size)]


def parse_to_embedd(list: list, bookname: str):
    return [
        {"_id": "page_" + str(idx), "chunk_text": chunk_text, "book_name": bookname}
        for idx, chunk_text in enumerate(list)
    ]


def chunk_upsert(namespace: str, dense_index: Index, chunked_pages: list) -> None:
    try:
        for chunk in chunked_pages:
            dense_index.upsert_records(namespace=namespace, records=chunk)
    except PineconeApiException as e:
        print(e)
        raise HTTPException(400, detail="Sorry book is too big")


def chunks(iterable, batch_size=200):
    """A helper function to break an iterable into chunks of size batch_size."""
    it = iter(iterable)
    chunk = tuple(itertools.islice(it, batch_size))
    while chunk:
        yield chunk
        chunk = tuple(itertools.islice(it, batch_size))


def init_pc(index_name: str) -> Index:
    try:
        pc = Pinecone(api_key=PINECONE_API_KEY)
        if not pc.has_index(index_name):
            pc.create_index_for_model(
                name=index_name,
                cloud="aws",
                region="us-east-1",
                embed={
                    "model": PC_MODEL,
                    "field_map": {"text": "chunk_text"},
                },  # type: ignore
            )
        dense_index = pc.Index(index_name)
        return dense_index
    except Exception as e:
        print(e)
        raise HTTPException(
            400, detail="there seems to be error connectiong to pinecone"
        )


def clean_embedded_pages(pages: list):
    return [obj for obj in pages if obj.get("chunk_text") and obj["chunk_text"].strip()]
