"""Tela de Livros."""
from nicegui import ui

from services.api_service import api
from components.navbar import navbar
from components.sidebar import sidebar
from components.book_form import open_book_form
from utils.constants import COLORS


def books_screen() -> None:

    navbar("Livros")
    sidebar("/livros")

    with ui.column().classes("w-full p-6 gap-4").style(
        f"background-color: {COLORS['background']}; min-height: 100vh;"
    ):

        # HEADER
        with ui.row().classes("w-full items-center justify-between"):

            with ui.column().classes("gap-0"):

                ui.label("Livros").classes(
                    "text-2xl font-bold"
                )

                ui.label(
                    "Gerencie o acervo da biblioteca."
                ).classes(
                    "text-sm"
                ).style(
                    f"color: {COLORS['text_muted']}"
                )

            ui.button(
                "Adicionar livro",
                icon="add",
                on_click=lambda: open_book_form(
                    None,
                    refresh
                )
            ).props(
                "unelevated color=primary"
            )

        # CARD
        with ui.card().classes(
            "p-4 rounded-2xl no-shadow w-full"
        ).style(
            f"""
            background-color: {COLORS['surface']};
            border: 1px solid {COLORS['border']};
            """
        ):

            with ui.row().classes(
                "w-full items-center gap-3 mb-3"
            ):

                search = ui.input(
                    placeholder="Buscar por título, SBM ou categoria"
                ).classes(
                    "flex-1"
                ).props(
                    "outlined dense clearable"
                )

            container = ui.column().classes(
                "w-full"
            )

        async def refresh():

            container.clear()

            try:

                books = await api.list_books()

                termo = (search.value or "").lower().strip()

                if termo:

                    books = [
                        b for b in books
                        if termo in b["titulo"].lower()
                        or termo in b["categoria"].lower()
                        or termo in b["sbm"].lower()
                    ]

                rows = [
                    {
                        "id": b["_id"],
                        "titulo": b["titulo"],
                        "sbm": b["sbm"],
                        "categoria": b["categoria"],
                        "quantidade_total": b["quantidade_total"],
                        "quantidade_disponivel": b["quantidade_disponivel"],
                    }
                    for b in books
                ]

                columns = [
                    {
                        "name": "titulo",
                        "label": "Título",
                        "field": "titulo",
                        "align": "left",
                    },
                    {
                        "name": "sbm",
                        "label": "SBM",
                        "field": "sbm",
                        "align": "left",
                    },
                    {
                        "name": "categoria",
                        "label": "Categoria",
                        "field": "categoria",
                        "align": "left",
                    },
                    {
                        "name": "quantidade_total",
                        "label": "Total",
                        "field": "quantidade_total",
                        "align": "center",
                    },
                    {
                        "name": "quantidade_disponivel",
                        "label": "Disponível",
                        "field": "quantidade_disponivel",
                        "align": "center",
                    },
                ]

                with container:

                    ui.table(
                        columns=columns,
                        rows=rows,
                        row_key="id"
                    ).classes(
                        "w-full"
                    ).props(
                        "flat"
                    )

                    if not rows:

                        ui.label(
                            "Nenhum livro encontrado."
                        ).classes(
                            "text-center w-full p-6"
                        ).style(
                            f"color: {COLORS['text_muted']}"
                        )

            except Exception as e:

                with container:

                    ui.label(
                        "Erro ao carregar livros."
                    ).classes(
                        "text-negative text-center w-full p-6"
                    )

                ui.notify(
                    f"Erro: {str(e)}",
                    type="negative"
                )

        # PESQUISA
        async def on_search(e):

            await refresh()

        search.on(
            "update:model-value",
            on_search
        )

        # CARREGAMENTO INICIAL
        ui.timer(
            0.1,
            refresh,
            once=True
        )