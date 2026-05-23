from fastapi import APIRouter
from app.config.database import db
from app.schemas.book_schema import BookCreate
from app.models.book_model import Book

router = APIRouter(prefix="/books", tags=["Books"])