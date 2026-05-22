# services/loan_service.py

from app.models.loan_model import Loan


class LoanService:

    @staticmethod
    def create_loan(
        aluno,
        livro,
        data_emprestimo,
        data_devolucao
    ):

        sucesso = livro.emprestar()

        if not sucesso:
            return None

        loan = Loan(
            aluno=aluno.to_dict(),
            livro=livro.to_dict(),
            data_emprestimo=data_emprestimo,
            data_devolucao=data_devolucao
        )

        return loan

    @staticmethod
    def return_loan(loan, livro):

        livro.devolver()

        loan.marcar_devolvido()

        return loan