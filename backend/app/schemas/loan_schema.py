from pydantic import BaseModel


class LoanCreate(BaseModel):

    student_id: str
    book_id: str

    data_emprestimo: str
    data_devolucao: str