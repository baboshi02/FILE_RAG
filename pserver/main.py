from typing import Annotated
from fastapi import FastAPI, File, Form
from pydantic import BaseModel
from pymupdf import Document
from pymupdf4llm import to_markdown
from pinecone import Pinecone
from tortoise import Tortoise
from utils.chunk import chunk_string, parse_to_embedd
from utils.pdf_to_pages import pdf_to_pages
import os
import dotenv
from langchain_google_genai import ChatGoogleGenerativeAI
from models.user import User
from jose import jwt

dotenv.load_dotenv()
from langchain_groq import ChatGroq


api_key = os.getenv("PINECONE_API_KEY")


llm = ChatGroq(
    model="llama-3.1-8b-instant",
    temperature=0,
    max_tokens=None,
    timeout=None,
    max_retries=2,
)
pc = Pinecone(api_key=api_key)


app = FastAPI()


class SignInPayload(BaseModel):
    email: str
    password: str
    username: str


@app.delete("/users")
async def deleteUsers():
    await Tortoise.init(
        db_url="postgres://baboshi:baboshi@localhost:5432/mydatabase",
        modules={"models": ["models.user"]},
    )
    await Tortoise.generate_schemas()
    await User.all().delete()


@app.get("/show_users")
async def showUsers():
    await Tortoise.init(
        db_url="postgres://baboshi:baboshi@localhost:5432/mydatabase",
        modules={"models": ["models.user"]},
    )
    await Tortoise.generate_schemas()
    users = await User.all()
    return users


@app.post("/signin")
async def signin(payload: SignInPayload):
    await Tortoise.init(
        db_url="postgres://baboshi:baboshi@localhost:5432/mydatabase",
        modules={"models": ["models.user"]},
    )
    await Tortoise.generate_schemas()
    email = payload.email
    password = payload.password
    username = payload.username
    await User.create(email=email, password=password, username=username)
    jwt_secret = os.getenv("JWT_SECRET") or "secret"
    token = jwt.encode(
        {"email": email, "username": username}, jwt_secret, algorithm="HS256"
    )
    return {"token": token}


class LoginPayload(BaseModel):
    email: str
    password: str


@app.post("/login")
async def login(payload: LoginPayload):
    await Tortoise.init(
        db_url="postgres://baboshi:baboshi@localhost:5432/mydatabase",
        modules={"models": ["models.user"]},
    )
    await Tortoise.generate_schemas()
    email = payload.email
    password = payload.password
    try:
        user = await User.get(email=email, password=password)
    except Exception:
        return {"message": "No user with given credentials"}
    jwt_secret = os.getenv("JWT_SECRET") or "secret"
    token = jwt.encode(
        {"email": user.email, "username": user.username}, jwt_secret, algorithm="HS256"
    )
    return {"token": token}


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
    pages = pdf_to_pages(pdf)
    if not pc.has_index(index_name):
        pc.create_index_for_model(
            name=index_name,
            cloud="aws",
            region="us-east-1",
            embed={"model": "llama-text-embed-v2", "field_map": {"text": "chunk_text"}},
        )
    dense_index = pc.Index(index_name)
    parsed_objects = parse_to_embedd(pages)
    for chunk in chunks(parsed_objects, 96):
        print("chunk: ", chunk)
        dense_index.upsert_records(namespace, chunk)
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
