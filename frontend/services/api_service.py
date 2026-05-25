"""
Serviço de dados mockado.

A integração real com a API FastAPI/MongoDB será feita depois substituindo
os métodos desta classe por chamadas HTTP (ex.: httpx.AsyncClient).
A interface pública deve ser mantida para não quebrar o frontend.
"""
from __future__ import annotations

from datetime import date, timedelta
from typing import Optional
from utils.constants import STATUS_ATIVO, STATUS_DEVOLVIDO, STATUS_ATRASADO
from utils.helpers import is_overdue


class APIService:
    def __init__(self) -> None:
        self._next_book_id = 1
        self._next_student_id = 1
        self._next_loan_id = 1

        self.books: list[dict] = []
        self.students: list[dict] = []
        self.loans: list[dict] = []

        self._seed()

    # ---------------- Seed ----------------
    def _seed(self) -> None:
        livros = [
            ("Dom Casmurro", "Machado de Assis", "Romance", "9788535910663", 5, 3),
            ("O Pequeno Príncipe", "Antoine de Saint-Exupéry", "Infantil", "9788595081512", 4, 2),
            ("1984", "George Orwell", "Ficção", "9788535914849", 3, 3),
            ("A Revolução dos Bichos", "George Orwell", "Ficção", "9788535909555", 2, 1),
            ("Memórias Póstumas de Brás Cubas", "Machado de Assis", "Romance", "9788508133239", 3, 2),
            ("O Cortiço", "Aluísio Azevedo", "Romance", "9788572326972", 4, 4),
        ]
        for t, a, c, isbn, qtd, disp in livros:
            self.create_book({
                "title": t, "author": a, "category": c,
                "isbn": isbn, "quantity": qtd, "available": disp,
            })

        alunos = [
            ("Ana Souza", "2025001", "9º A", "(11) 99999-1111", "ana@escola.com"),
            ("Bruno Lima", "2025002", "9º B", "(11) 99999-2222", "bruno@escola.com"),
            ("Carla Mendes", "2025003", "8º A", "(11) 99999-3333", "carla@escola.com"),
            ("Diego Rocha", "2025004", "7º A", "(11) 99999-4444", "diego@escola.com"),
            ("Eduarda Pires", "2025005", "9º A", "(11) 99999-5555", "eduarda@escola.com"),
        ]
        for n, m, t, tel, em in alunos:
            self.create_student({
                "name": n, "registration": m, "class_name": t,
                "phone": tel, "email": em,
            })

        hoje = date.today()
        emprestimos = [
            (1, 1, hoje - timedelta(days=3), hoje + timedelta(days=11), None),
            (2, 2, hoje - timedelta(days=20), hoje - timedelta(days=6), None),  # atrasado
            (3, 4, hoje - timedelta(days=30), hoje - timedelta(days=16),
             hoje - timedelta(days=15)),  # devolvido
            (4, 5, hoje - timedelta(days=1), hoje + timedelta(days=13), None),
        ]
        for student_id, book_id, loan_date, due, ret in emprestimos:
            self.loans.append({
                "id": self._next_loan_id,
                "student_id": student_id,
                "book_id": book_id,
                "loan_date": loan_date,
                "due_date": due,
                "return_date": ret,
            })
            self._next_loan_id += 1

    # ---------------- Books ----------------
    def list_books(self, search: str = "") -> list[dict]:
        s = (search or "").lower().strip()
        if not s:
            return list(self.books)
        return [
            b for b in self.books
            if s in b["title"].lower()
            or s in b["author"].lower()
            or s in b["category"].lower()
            or s in b["isbn"].lower()
        ]

    def get_book(self, book_id: int) -> Optional[dict]:
        return next((b for b in self.books if b["id"] == book_id), None)

    def create_book(self, data: dict) -> dict:
        book = {
            "id": self._next_book_id,
            "title": data.get("title", ""),
            "author": data.get("author", ""),
            "category": data.get("category", ""),
            "isbn": data.get("isbn", ""),
            "quantity": int(data.get("quantity", 0)),
            "available": int(data.get("available", data.get("quantity", 0))),
        }
        self.books.append(book)
        self._next_book_id += 1
        return book

    def update_book(self, book_id: int, data: dict) -> Optional[dict]:
        book = self.get_book(book_id)
        if not book:
            return None
        old_qty = book["quantity"]
        new_qty = int(data.get("quantity", old_qty))
        diff = new_qty - old_qty
        book.update({
            "title": data.get("title", book["title"]),
            "author": data.get("author", book["author"]),
            "category": data.get("category", book["category"]),
            "isbn": data.get("isbn", book["isbn"]),
            "quantity": new_qty,
            "available": max(0, book["available"] + diff),
        })
        return book

    def delete_book(self, book_id: int) -> bool:
        book = self.get_book(book_id)
        if not book:
            return False
        self.books.remove(book)
        return True

    # ---------------- Students ----------------
    def list_students(self, search: str = "") -> list[dict]:
        s = (search or "").lower().strip()
        if not s:
            return list(self.students)
        return [
            a for a in self.students
            if s in a["name"].lower()
            or s in a["registration"].lower()
            or s in a["class_name"].lower()
        ]

    def get_student(self, student_id: int) -> Optional[dict]:
        return next((a for a in self.students if a["id"] == student_id), None)

    def create_student(self, data: dict) -> dict:
        student = {
            "id": self._next_student_id,
            "name": data.get("name", ""),
            "registration": data.get("registration", ""),
            "class_name": data.get("class_name", ""),
            "phone": data.get("phone", ""),
            "email": data.get("email", ""),
        }
        self.students.append(student)
        self._next_student_id += 1
        return student

    def update_student(self, student_id: int, data: dict) -> Optional[dict]:
        s = self.get_student(student_id)
        if not s:
            return None
        s.update({
            "name": data.get("name", s["name"]),
            "registration": data.get("registration", s["registration"]),
            "class_name": data.get("class_name", s["class_name"]),
            "phone": data.get("phone", s["phone"]),
            "email": data.get("email", s["email"]),
        })
        return s

    def delete_student(self, student_id: int) -> bool:
        s = self.get_student(student_id)
        if not s:
            return False
        self.students.remove(s)
        return True

    # ---------------- Loans ----------------
    def list_loans(self) -> list[dict]:
        return list(self.loans)

    def loan_status(self, loan: dict) -> str:
        if loan.get("return_date"):
            return STATUS_DEVOLVIDO
        if is_overdue(loan.get("due_date"), False):
            return STATUS_ATRASADO
        return STATUS_ATIVO

    def create_loan(self, data: dict) -> Optional[dict]:
        book = self.get_book(int(data["book_id"]))
        student = self.get_student(int(data["student_id"]))
        if not book or not student:
            return None
        if book["available"] <= 0:
            return None
        loan = {
            "id": self._next_loan_id,
            "student_id": student["id"],
            "book_id": book["id"],
            "loan_date": data.get("loan_date") or date.today(),
            "due_date": data.get("due_date"),
            "return_date": None,
        }
        book["available"] -= 1
        self.loans.append(loan)
        self._next_loan_id += 1
        return loan

    def return_loan(self, loan_id: int) -> bool:
        loan = next((l for l in self.loans if l["id"] == loan_id), None)
        if not loan or loan["return_date"]:
            return False
        loan["return_date"] = date.today()
        book = self.get_book(loan["book_id"])
        if book:
            book["available"] = min(book["quantity"], book["available"] + 1)
        return True

    def delete_loan(self, loan_id: int) -> bool:
        loan = next((l for l in self.loans if l["id"] == loan_id), None)
        if not loan:
            return False
        # se ativo, devolve estoque
        if not loan["return_date"]:
            book = self.get_book(loan["book_id"])
            if book:
                book["available"] = min(book["quantity"], book["available"] + 1)
        self.loans.remove(loan)
        return True

    # ---------------- Dashboard ----------------
    def dashboard_stats(self) -> dict:
        total_books = sum(b["quantity"] for b in self.books)
        available_books = sum(b["available"] for b in self.books)
        loaned_books = total_books - available_books
        return {
            "total_books": total_books,
            "available_books": available_books,
            "loaned_books": loaned_books,
            "total_students": len(self.students),
            "active_loans": sum(1 for l in self.loans if not l["return_date"]),
            "overdue_loans": sum(
                1 for l in self.loans
                if not l["return_date"] and is_overdue(l["due_date"], False)
            ),
        }

    def recent_loans(self, limit: int = 5) -> list[dict]:
        return sorted(self.loans, key=lambda l: l["loan_date"], reverse=True)[:limit]


# Instância global (singleton simples)
api = APIService()
