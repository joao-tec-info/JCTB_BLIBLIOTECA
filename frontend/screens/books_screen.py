"""Tela de Livros."""
from nicegui import ui

from components.navbar import navbar
from components.sidebar import sidebar
from components.book_form import open_book_form
from services.api_service import api
from utils.constants import COLORS


def books_screen() -> None:
    navbar("Livros")
    sidebar("/livros")

    state = {"search": ""}

    with ui.column().classes("w-full p-6 gap-4").style(
        f"background-color: {COLORS['background']}; min-height: 100vh;"
    ):
        with ui.row().classes("w-full items-center justify-between"):
            with ui.column().classes("gap-0"):
                ui.label("Livros").classes("text-2xl font-bold")
                ui.label("Gerencie o acervo da biblioteca.").classes(
                    "text-sm"
                ).style(f"color: {COLORS['text_muted']}")
            ui.button("Adicionar livro", icon="add",
                      on_click=lambda: open_book_form(None, refresh)) \
                .props("unelevated color=primary")

        with ui.card().classes("p-4 rounded-2xl no-shadow w-full").style(
            f"background-color: {COLORS['surface']}; "
            f"border: 1px solid {COLORS['border']};"
        ):
            with ui.row().classes("w-full items-center gap-3 mb-3"):
                search = ui.input(placeholder="Buscar por título, autor, categoria ou ISBN") \
                    .classes("flex-1").props("outlined dense clearable")
                search.on(
                    "update:model-value",
                    lambda e: (state.update(search=e.args or ""), refresh()),
                )

            container = ui.column().classes("w-full")

        def refresh():
            container.clear()
            books = api.list_books(state["search"])
            with container:
                rows = [{
                    "id": b["id"],
                    "title": b["title"],
                    "author": b["author"],
                    "category": b["category"],
                    "isbn": b["isbn"],
                    "quantity": b["quantity"],
                    "available": b["available"],
                } for b in books]

                columns = [
                    {"name": "title", "label": "Título", "field": "title", "align": "left"},
                    {"name": "author", "label": "Autor", "field": "author", "align": "left"},
                    {"name": "category", "label": "Categoria", "field": "category", "align": "left"},
                    {"name": "isbn", "label": "ISBN", "field": "isbn", "align": "left"},
                    {"name": "quantity", "label": "Total", "field": "quantity", "align": "center"},
                    {"name": "available", "label": "Disponível", "field": "available", "align": "center"},
                    {"name": "actions", "label": "Ações", "field": "actions", "align": "right"},
                ]
                table = ui.table(columns=columns, rows=rows, row_key="id") \
                    .classes("w-full").props("flat")

                table.add_slot("body-cell-actions", r"""
                    <q-td :props="props" class="text-right">
                        <q-btn flat round dense icon="edit" color="primary"
                               @click="() => $parent.$emit('edit', props.row)" />
                        <q-btn flat round dense icon="delete" color="negative"
                               @click="() => $parent.$emit('delete', props.row)" />
                    </q-td>
                """)
                table.on("edit", lambda e: open_book_form(
                    api.get_book(e.args["id"]), refresh))
                table.on("delete", lambda e: confirm_delete(e.args["id"]))

                if not rows:
                    ui.label("Nenhum livro encontrado.").classes(
                        "text-center w-full p-6"
                    ).style(f"color: {COLORS['text_muted']}")

        def confirm_delete(book_id: int):
            with ui.dialog() as d, ui.card().classes("p-5 rounded-2xl"):
                ui.label("Excluir livro?").classes("text-lg font-bold")
                ui.label("Essa ação não pode ser desfeita.").classes(
                    "text-sm text-gray-500"
                )
                with ui.row().classes("justify-end gap-2 mt-4"):
                    ui.button("Cancelar", on_click=d.close).props("flat")

                    def do():
                        api.delete_book(book_id)
                        ui.notify("Livro excluído", type="positive")
                        d.close()
                        refresh()
                    ui.button("Excluir", on_click=do).props(
                        "unelevated color=negative"
                    )
            d.open()

        refresh()
