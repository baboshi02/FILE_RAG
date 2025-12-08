from typing import Annotated
from fastapi import FastAPI, File
from pymupdf import Document
from pymupdf4llm import to_markdown


app = FastAPI()


@app.get("/")
def root():
    return {"message": "Hello world"}


@app.post("/files/")
def post_file(pdf: Annotated[bytes, File()]):
    document = Document(stream=pdf)
    markdown = to_markdown(document)
    print("file content: ", markdown)
    return {"markdown": markdown}
