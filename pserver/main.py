from typing import Annotated
from fastapi import FastAPI, File
from pymupdf import Document
from pymupdf4llm import to_markdown
from pinecone import Pinecone
from utils.chunk import chunk_string, parse_to_embedd
import os
import dotenv

dotenv.load_dotenv()
api_key = os.getenv("PINECONE_API_KEY")

pc = Pinecone(api_key=api_key)


app = FastAPI()


@app.get("/")
def root():
    return {"message": "Hello world"}


@app.post("/pdf")
def get_pdf(pdf: Annotated[bytes, File()]):
    document = Document(stream=pdf)
    markdown = to_markdown(document)
    chunked_string = chunk_string(markdown, 1500)
    parsed_objects = parse_to_embedd(chunked_string)
    index_name = "testing-pdf"
    if not pc.has_index(index_name):
        pc.create_index_for_model(
            name=index_name,
            cloud="aws",
            region="us-east-1",
            embed={"model": "llama-text-embed-v2", "field_map": {"text": "chunk_text"}},
        )
    dense_index = pc.Index(index_name)
    dense_index.upsert_records("book", parsed_objects)
    return {"parsed": parsed_objects}


@app.post("/files/")
def post_file(pdf: Annotated[bytes, File()]):
    document = Document(stream=pdf)
    markdown = to_markdown(document)
    print("file content: ", markdown)
    return {"markdown": markdown}
