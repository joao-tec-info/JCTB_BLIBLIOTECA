"""Modal de formulário de livro."""
from nicegui import ui
from services.api_service import api


def open_book_form(book: dict | None, on_saved) -> None:
    is_edit = book is not None
    data = {
        "title": book["title"] if is_edit else "",
        "author": book["author"] if is_edit else "",
        "category": book["category"] if is_edit else "",
        "isbn": book["isbn"] if is_edit else "",
        "quantity": book["quantity"] if is_edit else 1,
        "available": book["available"] if is_edit else 1,
    }

    with ui.dialog() as dialog, ui.card().classes("p-6 rounded-2xl w-[520px]"):
        ui.label("Editar Livro" if is_edit else "Novo Livro").classes(
            "text-xl font-bold mb-2"
        )
        ui.label("Preencha as informações do livro.").classes(
            "text-sm text-gray-500 mb-4"
        )

        title = ui.input("Título", value=data["title"]).classes("w-full").props("outlined dense")
        author = ui.input("Autor", value=data["author"]).classes("w-full").props("outlined dense")
        with ui.row().classes("w-full gap-3 no-wrap"):
            category = ui.input("Categoria", value=data["category"]) \
                .classes("flex-1").props("outlined dense")
            isbn = ui.input("ISBN", value=data["isbn"]) \
                .classes("flex-1").props("outlined dense")
        with ui.row().classes("w-full gap-3 no-wrap"):
            quantity = ui.number("Quantidade total", value=data["quantity"], min=0) \
                .classes("flex-1").props("outlined dense")
            available = ui.number("Quantidade disponível", value=data["available"], min=0) \
                .classes("flex-1").props("outlined dense")

        def save():
            if not title.value or not author.value:
                ui.notify("Título e autor são obrigatórios", type="warning")
                return
            payload = {
                "title": title.value, "author": author.value,
                "category": category.value, "isbn": isbn.value,
                "quantity": int(quantity.value or 0),
                "available": int(available.value or 0),
            }
            if is_edit:
                api.update_book(book["id"], payload)
                ui.notify("Livro atualizado", type="positive")
            else:
                api.create_book(payload)
                ui.notify("Livro adicionado", type="positive")
            dialog.close()
            on_saved()

        with ui.row().classes("w-full justify-end gap-2 mt-4"):
            ui.button("Cancelar", on_click=dialog.close).props("flat")
            ui.button("Salvar", on_click=save).props("unelevated color=primary")

    dialog.open()
