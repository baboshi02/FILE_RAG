from models.user import User
from fastapi import APIRouter, Depends
from llm.llm import llm
from typing import Annotated
from fastapi import File
from utils.pdf_to_pages import pdf_to_pages
from dependencies.authorization import check_authorization

router = APIRouter(prefix="/admin", dependencies=[Depends(check_authorization)])


@router.get("/ask")
def ask_ai(question: str):
    response = llm.invoke([("human", question)])
    return response.content


@router.get("/")
def root():
    return {"message": "Hello world"}


@router.post("/pdf_to_text")
def pdf_to_text(pdf: Annotated[bytes, File()]):
    pages = pdf_to_pages(pdf)
    return pages


@router.delete("/users")
async def deleteUsers():
    await User.all().delete()


@router.get("/show_users")
async def showUsers():
    users = await User.all()
    return users
