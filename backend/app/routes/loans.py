from fastapi import APIRouter, HTTPException
from bson import ObjectId

from app.schemas.loan_schema import LoanCreate
from app.services.loan_service import LoanService
from app.config.database import db


router = APIRouter(
    prefix="/loans",
    tags=["Loans"]
)


@router.post("/")
def create_loan(data: LoanCreate):

    return LoanService.create_loan(data)


@router.get("/")
def get_loans():

    loans = list(db.loans.find())

    for loan in loans:
        loan["_id"] = str(loan["_id"])

    return loans


@router.put("/{loan_id}/return")
def return_loan(loan_id: str):

    loan = db.loans.find_one({
        "_id": ObjectId(loan_id)
    })

    if not loan:
        raise HTTPException(
            status_code=404,
            detail="Empréstimo não encontrado"
        )

    if loan.get("devolvido"):
        raise HTTPException(
            status_code=400,
            detail="Livro já devolvido"
        )

    # marca empréstimo como devolvido
    db.loans.update_one(
        {"_id": ObjectId(loan_id)},
        {
            "$set": {
                "devolvido": True
            }
        }
    )

    # devolve quantidade disponível do livro
    db.books.update_one(
        {
            "_id": ObjectId(
                loan["livro"]["_id"]
            )
        },
        {
            "$inc": {
                "quantidade_disponivel": 1
            }
        }
    )

    return {
        "message": "Livro devolvido com sucesso"
    }