from typing import Annotated
from fastapi import APIRouter, Depends, Form, File, HTTPException
from models.user import Books, User
from utils.pdf_to_pages import pdf_to_pages
from utils.chunk import (
    parse_to_embedd,
    chunk_pages,
    init_pc,
    clean_embedded_pages,
    chunk_upsert,
)
from llm.llm import llm
from pinecone import Pinecone
from dependencies.authorization import check_authorization
from config import PINECONE_API_KEY
from tortoise.exceptions import MultipleObjectsReturned, DoesNotExist


router = APIRouter(dependencies=[Depends(check_authorization)])
index_name = "pdf-rag"


@router.get("/books")
async def get_books(username: Annotated[str, Depends(check_authorization)]):
    user = await User.get(username=username)
    books = await Books.filter(owner=user)
    return books


# TODO: Refactor this endpoint to have one big try block with seperate except blocks
# TODO: Change the jwt token to include id rather that username
@router.post("/pdf")
async def post_pdf(
    bookname: Annotated[str, Form()],
    pdf: Annotated[bytes, File()],
    username: Annotated[str, Depends(check_authorization)],
):
    namespace = username
    pages = pdf_to_pages(pdf)
    dense_index = init_pc(index_name)
    embedded_pages = parse_to_embedd(pages, bookname)
    cleaned_embedded_pages = clean_embedded_pages(embedded_pages)
    chunked_pages = chunk_pages(cleaned_embedded_pages, 96)
    chunk_upsert(namespace, dense_index, chunked_pages)
    try:
        user = await User.get(username=username)
        await Books.create(
            title=bookname,
            owner=user,
        )
    except MultipleObjectsReturned:
        raise HTTPException(400, detail="Multiple Users with username found")
    except DoesNotExist:
        raise HTTPException(404, detail="User with username does not exist")
    except Exception as e:
        print(e)
        raise HTTPException(400, detail="Unknown error occured")
    return {"message": "Successfully uploaded book"}


def ask_llm(top_results_text: list[str], question: str):
    messages = [
        (
            "system",
            "You are a helpful assistant that uses RAG to answer questions provided from the following three top snippets answer the question",
        )
    ]
    messages.extend([("human", result) for result in top_results_text])
    messages.append(("human", question))
    try:
        response = llm.invoke(messages)
        return response.content
    except Exception as e:
        print(e)
        raise HTTPException(400, "Error while connecting to llm")


# TODO: Increase abstraction layer
@router.get("/pdf")
async def chat_about_file(
    username: Annotated[str, Depends(check_authorization)],
    book_id: int,
    question: str,
    top_k: int | None = 3,
):
    namespace = username
    try:
        user = await User.get(username=username)
        book = await Books.get(owner=user, id=book_id).values("title")
    except DoesNotExist or MultipleObjectsReturned:
        raise HTTPException(400, detail="User or Book couldn't be found")
    dense_index = init_pc(index_name)
    try:
        top_results = dense_index.search(
            namespace=namespace, query={"top_k": top_k, "inputs": {"text": question}, "filter": {"book_name": book["title"]}}  # type: ignore
        )
    except Exception as e:
        print(e)
        raise HTTPException(400, "Error while querying for pdf")
    formatted_top_results = [
        {
            "chunk_text": result_text["fields"]["chunk_text"],
            "score": result_text["_score"],
        }
        for result_text in top_results["result"]["hits"]
    ]
    top_results_text = [result["chunk_text"] for result in formatted_top_results]
    answer = ask_llm(top_results_text, question)
    return answer
