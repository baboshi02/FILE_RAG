from typing import Annotated
from fastapi import FastAPI, File, Form
from pydantic import BaseModel
from pymupdf import Document
from pymupdf4llm import to_markdown
from pinecone import Pinecone
from utils.chunk import chunk_string, parse_to_embedd
from utils.pdf_to_pages import pdf_to_pages
import os
import dotenv
from langchain_google_genai import ChatGoogleGenerativeAI

dotenv.load_dotenv()
from langchain_groq import ChatGroq


class Payload(BaseModel):
    username: str
    bookname: str


api_key = os.getenv("PINECONE_API_KEY")
import re
import unicodedata


def clean_ocr_text(text):
    # Normalize unicode
    text = unicodedata.normalize("NFKC", text)

    # Fix hyphenation across line breaks
    text = re.sub(r"-\s*\n\s*", "", text)

    # Replace multiple spaces/newlines
    text = re.sub(r"\n+", "\n", text)
    text = re.sub(r"[ \t]+", " ", text)

    # Strip extra whitespace
    text = text.strip()

    return text


llm = ChatGroq(
    model="llama-3.1-8b-instant",
    temperature=0,
    max_tokens=None,
    timeout=None,
    max_retries=2,
    # other params...
)
pc = Pinecone(api_key=api_key)


app = FastAPI()


@app.post("/pdf_to_text")
def pdf_to_text(pdf: Annotated[bytes, File()]):
    pages = pdf_to_pages(pdf)
    return pages


@app.get("/ask")
def ask_ai(question: str):
    response = llm.invoke([("human", question)])
    return response.content


@app.get("/")
def root():
    return {"message": "Hello world"}


@app.post("/pdf")
def post_pdf(
    username: Annotated[str, Form()],
    bookname: Annotated[str, Form()],
    pdf: Annotated[bytes, File()],
):
    index_name = username
    namespace = bookname
    document = Document(stream=pdf)
    markdown = to_markdown(document)
    chunked_string = chunk_string(markdown, 1500)
    parsed_objects = parse_to_embedd(chunked_string)
    if not pc.has_index(index_name):
        pc.create_index_for_model(
            name=index_name,
            cloud="aws",
            region="us-east-1",
            embed={"model": "llama-text-embed-v2", "field_map": {"text": "chunk_text"}},
        )
    dense_index = pc.Index(index_name)
    dense_index.upsert_records(namespace, parsed_objects)
    return {"parsed": parsed_objects}


@app.get("/pdf")
def chat_about_file(username: str, bookname: str, question: str, top_k: int | None = 3):
    index_name = username
    namespace = bookname
    if not pc.has_index(index_name):
        return {"message": "Sorry index not found"}
    dense_index = pc.Index(index_name)
    results = dense_index.search(
        namespace=namespace, query={"top_k": top_k, "inputs": {"text": question}}
    )
    filtered_results = [
        {
            "chunk_text": result_text["fields"]["chunk_text"],
            "score": result_text["_score"],
        }
        for result_text in results["result"]["hits"]
    ]
    chunked_text = [x["chunk_text"] for x in filtered_results]
    print(chunked_text)
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
