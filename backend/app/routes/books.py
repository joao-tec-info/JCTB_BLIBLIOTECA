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