from models.user import User
from fastapi import APIRouter, Depends
from llm.llm import llm
from typing import Annotated
from fastapi import File, HTTPException
from utils.pdf_to_pages import pdf_to_pages
from dependencies.authorization import check_authorization

router = APIRouter(prefix="/admin", dependencies=[Depends(check_authorization)])


@router.get("/ask")
def ask_ai(question: str):
    try:
        response = llm.invoke([("human", question)])
        return response.content
    except Exception as e:
        print(e)
        raise HTTPException(400, "There seems to be an error in invoking llm")


@router.get("/")
def root():
    return {"message": "Hello world"}


@router.post("/pdf_to_text")
def pdf_to_text(pdf: Annotated[bytes, File()]):
    pages = pdf_to_pages(pdf)
    return pages


@router.delete("/users")
async def deleteUsers():
    try:
        await User.all().delete()
    except Exception as e:
        print(e)
        raise HTTPException(400, "There seems to be an error in invoking llm")


@router.get("/show_users")
async def showUsers():
    try:
        users = await User.all()
        return users
    except Exception as e:
        print(e)
        raise HTTPException(400, "There seems to be an error in invoking llm")
