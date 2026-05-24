# services/loan_service.py

from bson import ObjectId

from app.config.database import db
from app.models.loan_model import Loan


class LoanService:

    @staticmethod
    def create_loan(data):

        aluno = db.students.find_one({
            "_id": ObjectId(data.student_id)
        })

        if not aluno:
            return {
                "error": "Aluno não encontrado"
            }

        livro = db.books.find_one({
            "_id": ObjectId(data.book_id)
        })

        if not livro:
            return {
                "error": "Livro não encontrado"
            }

        if livro["quantidade_disponivel"] <= 0:
            return {
                "error": "Livro indisponível"
            }

        db.books.update_one(
            {
                "_id": ObjectId(data.book_id)
            },
            {
                "$inc": {
                    "quantidade_disponivel": -1
                }
            }
        )

        loan = Loan(
            aluno={
                "_id": str(aluno["_id"]),
                "nome": aluno["nome"]
            },

            livro={
                "_id": str(livro["_id"]),
                "titulo": livro["titulo"]
            },

            data_emprestimo=data.data_emprestimo,
            data_devolucao=data.data_devolucao
        )

        result = db.loans.insert_one(
            loan.to_dict()
        )

        return {
            "message": "Empréstimo realizado",
            "id": str(result.inserted_id)
        }

    @staticmethod
    def return_loan(loan_id):

        loan = db.loans.find_one({
            "_id": ObjectId(loan_id)
        })

        if not loan:
            return {
                "error": "Empréstimo não encontrado"
            }

        if loan["devolvido"]:
            return {
                "error": "Livro já devolvido"
            }

        book_id = loan["livro"]["_id"]

        db.books.update_one(
            {
                "_id": ObjectId(book_id)
            },
            {
                "$inc": {
                    "quantidade_disponivel": 1
                }
            }
        )

        db.loans.update_one(
            {
                "_id": ObjectId(loan_id)
            },
            {
                "$set": {
                    "devolvido": True
                }
            }
        )

        return {
            "message": "Livro devolvido"
        }