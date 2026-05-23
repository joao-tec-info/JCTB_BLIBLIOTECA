from fastapi import APIRouter
from app.config.database import db
from app.schemas.book_schema import BookCreate
from app.models.book_model import Book

router = APIRouter(prefix="/books", tags=["Books"])

@router.post("/")
def create_book(book: BookCreate):

    new_book = Book(
        titulo=book.titulo,
        sbm=book.sbm,
        quantidade_total=book.quantidade_total,
        categoria=book.categoria
    )

    result = db.books.insert_one(new_book.to_dict())

    return {
        "message": "Livro criado com sucesso",
        "id": str(result.inserted_id)
    }

@router.get("/")
def get_books():

    books = list(db.books.find())

    for b in books:
        b["_id"] = str(b["_id"])

    return books

from bson import ObjectId


@router.get("/{book_id}")
def get_book(book_id: str):

    book = db.books.find_one({"_id": ObjectId(book_id)})

    if not book:
        return {"error": "Livro não encontrado"}

    book["_id"] = str(book["_id"])
    return book

@router.put("/{book_id}")
def update_book(book_id: str, book: BookCreate):

    db.books.update_one(
        {"_id": ObjectId(book_id)},
        {"$set": book.dict()}
    )

    return {"message": "Livro atualizado"}

@router.delete("/{book_id}")
def delete_book(book_id: str):

    db.books.delete_one({"_id": ObjectId(book_id)})

    return {"message": "Livro deletado"}
