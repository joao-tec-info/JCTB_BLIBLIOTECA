from app.models.book_model import Book
from app.models.student_model import Student
from app.services.loan_service import LoanService


def main():

    aluno = Student(
    "João",
    "2º Ano A"
)

    livro = Book(
    "Dom Casmurro",
    "123456",
    10,
    "Romance"
)

    emprestimo = LoanService.create_loan(
        aluno,
        livro,
        "22/05/2026",
        "29/05/2026"
    )

    if emprestimo:

        print("Empréstimo realizado!")

        print(emprestimo.aluno)

        print(emprestimo.livro)

    else:

        print("Livro indisponível")


if __name__ == "__main__":
    main()