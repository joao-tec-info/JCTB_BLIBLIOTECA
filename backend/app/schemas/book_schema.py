from pydantic import BaseModel
from typing import Optional


class BookCreate(BaseModel):
    titulo: str
    sbm: str
    quantidade_total: int
    categoria: Optional[str] = None