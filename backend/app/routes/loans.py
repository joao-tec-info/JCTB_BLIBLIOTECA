from fastapi import APIRouter

from app.schemas.loan_schema import LoanCreate
from app.services.loan_service import LoanService


router = APIRouter(
    prefix="/loans",
    tags=["Loans"]
)

@router.post("/")
def create_loan(data: LoanCreate):

    return LoanService.create_loan(data)

from app.config.database import db


@router.get("/")
def get_loans():

    loans = list(db.loans.find())

    for loan in loans:
        loan["_id"] = str(loan["_id"])

    return loans

