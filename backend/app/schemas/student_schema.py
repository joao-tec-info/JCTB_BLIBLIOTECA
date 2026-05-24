from pydantic import BaseModel


class StudentCreate(BaseModel):
    nome: str
    turma: str