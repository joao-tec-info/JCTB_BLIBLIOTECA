"""Modal de formulário de empréstimo."""
from datetime import date
from nicegui import ui
from services.api_service import api
from utils.helpers import default_due_date, parse_date


def open_loan_form(on_saved) -> None:
    students = api.list_students()
    books = [b for b in api.list_books() if b["available"] > 0]

    student_options = {s["id"]: f'{s["name"]} — {s["registration"]}' for s in students}
    book_options = {
        b["id"]: f'{b["title"]} ({b["available"]} disp.)' for b in books
    }

    with ui.dialog() as dialog, ui.card().classes("p-6 rounded-2xl w-[520px]"):
        ui.label("Novo Empréstimo").classes("text-xl font-bold mb-2")
        ui.label("Selecione o aluno e o livro.").classes(
            "text-sm text-gray-500 mb-4"
        )

        if not student_options:
            ui.label("Cadastre alunos antes de registrar empréstimos.") \
                .classes("text-sm text-red-500")
        if not book_options:
            ui.label("Nenhum livro disponível para empréstimo.") \
                .classes("text-sm text-red-500")

        student_sel = ui.select(student_options, label="Aluno") \
            .classes("w-full").props("outlined dense")
        book_sel = ui.select(book_options, label="Livro") \
            .classes("w-full").props("outlined dense")

        with ui.row().classes("w-full gap-3 no-wrap"):
            loan_date_in = ui.input(
                "Data do empréstimo", value=date.today().isoformat()
            ).classes("flex-1").props("outlined dense type=date")
            due_date_in = ui.input(
                "Devolução prevista", value=default_due_date().isoformat()
            ).classes("flex-1").props("outlined dense type=date")

        def save():
            if not student_sel.value or not book_sel.value:
                ui.notify("Selecione aluno e livro", type="warning")
                return
            result = api.create_loan({
                "student_id": student_sel.value,
                "book_id": book_sel.value,
                "loan_date": parse_date(loan_date_in.value) or date.today(),
                "due_date": parse_date(due_date_in.value) or default_due_date(),
            })
            if not result:
                ui.notify("Não foi possível registrar o empréstimo", type="negative")
                return
            ui.notify("Empréstimo registrado", type="positive")
            dialog.close()
            on_saved()

        with ui.row().classes("w-full justify-end gap-2 mt-4"):
            ui.button("Cancelar", on_click=dialog.close).props("flat")
            ui.button("Registrar", on_click=save).props("unelevated color=primary")

    dialog.open()
