from typing import Annotated
from fastapi import APIRouter, Depends, Form, File, HTTPException
from utils.pdf_to_pages import pdf_to_pages
from utils.chunk import parse_to_embedd, chunk_string
from llm.llm import llm
from pinecone import Pinecone
from dependencies.authorization import check_authorization
from config import PC_MODEL, PINECONE_API_KEY

router = APIRouter(dependencies=[Depends(check_authorization)])
pc = Pinecone(api_key=PINECONE_API_KEY)
index_name = "pdf-rag"


def init_pc(index_name: str) -> Pinecone:
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
    return pc


@router.post("/pdf")
def post_pdf(
    bookname: Annotated[str, Form()],
    pdf: Annotated[bytes, File()],
    username: Annotated[str, Depends(check_authorization)],
):
    namespace = username
    pages = pdf_to_pages(pdf)
    try:
        pc = init_pc(index_name)
    except Exception as e:
        print(e)
        raise HTTPException(
            400, detail="there seems to be error connectiong to pinecone"
        )
    dense_index = pc.Index(index_name)
    parsed_objects = parse_to_embedd(pages, bookname)
    cleaned_objects = [
        obj for obj in parsed_objects 
        if obj.get("chunk_text") and obj["chunk_text"].strip()
    ]
    for chunk in chunk_string(cleaned_objects, 96):
        dense_index.upsert_records(namespace=namespace,records=chunk)
    return {"parsed": parsed_objects}


@router.get("/pdf")
def chat_about_file(
    username: Annotated[str, Depends(check_authorization)],
    bookname: str,
    question: str,
    top_k: int | None = 3,
):
    namespace = username
    try:
        if not pc.has_index(index_name):
            return {"message": "Sorry index not found"}
        dense_index = pc.Index(index_name)
        results = dense_index.search(
            namespace=namespace, query={"top_k": top_k, "inputs": {"text": question}, "filter": {"book_name": bookname}}  # type: ignore
        )
    except Exception as e:
        print(e)
        raise HTTPException(400, "Error while querying for pdf")
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
    try:
        response = llm.invoke(messages)
        return response.content
    except Exception as e:
        print(e)
        raise HTTPException(400, "Error while connecting to llm")
