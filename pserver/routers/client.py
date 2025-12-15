from typing import Annotated
from fastapi import APIRouter, Depends, Form, File
from utils.pdf_to_pages import pdf_to_pages
from utils.chunk import parse_to_embedd, chunk_string
from llm.llm import llm
from pinecone import Pinecone
from dependencies.authorization import check_authorization
import dotenv
import os

router = APIRouter(dependencies=[Depends(check_authorization)])

dotenv.load_dotenv()

PINECONE_API_KEY = os.getenv("PINECONE_API_KEY")
pc = Pinecone(api_key=PINECONE_API_KEY)
PC_MODEL = os.getenv("PC_MODEL") or ""


@router.post("/pdf")
def post_pdf(
    username: Annotated[str, Form()],
    bookname: Annotated[str, Form()],
    pdf: Annotated[bytes, File()],
):
    index_name = username
    namespace = bookname
    pages = pdf_to_pages(pdf)
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
    # pyright enable
    dense_index = pc.Index(index_name)
    parsed_objects = parse_to_embedd(pages)
    for chunk in chunk_string(parsed_objects, 96):
        print("chunk: ", chunk)
        dense_index.upsert_records(namespace, chunk)
    return {"parsed": parsed_objects}


@router.get("/pdf")
def chat_about_file(username: str, bookname: str, question: str, top_k: int | None = 3):
    index_name = username
    namespace = bookname
    if not pc.has_index(index_name):
        return {"message": "Sorry index not found"}
    dense_index = pc.Index(index_name)
    results = dense_index.search(
        namespace=namespace, query={"top_k": top_k, "inputs": {"text": question}}  # type: ignore
    )
    filtered_results = [
        {
            "chunk_text": result_text["fields"]["chunk_text"],
            "score": result_text["_score"],
        }
        for result_text in results["result"]["hits"]
    ]
    chunked_text = [x["chunk_text"] for x in filtered_results]
    messages = [
        (
            "system",
            "You are a helpful assistant that uses RAG to answer questions provided from the following three top snippets answer the question",
        )
    ]
    messages.extend([("human", chunk) for chunk in chunked_text])
    messages.append(("human", question))
    response = llm.invoke(messages)
    return response.content
