"""Modal de formulário de livro."""

from nicegui import ui

from services.api_service import api


def open_book_form(book: dict | None, on_saved) -> None:

    is_edit = book is not None

    data = {
        "titulo": book["titulo"] if is_edit else "",
        "sbm": book["sbm"] if is_edit else "",
        "categoria": book["categoria"] if is_edit else "",
        "quantidade_total": (
            book["quantidade_total"]
            if is_edit else 1
        ),
    }

    with ui.dialog() as dialog, ui.card().classes(
        "p-6 rounded-2xl w-[520px]"
    ):

        ui.label(
            "Editar Livro" if is_edit else "Novo Livro"
        ).classes(
            "text-xl font-bold mb-2"
        )

        ui.label(
            "Preencha as informações do livro."
        ).classes(
            "text-sm text-gray-500 mb-4"
        )

        # ---------------- INPUTS ----------------

        titulo = ui.input(
            "Título",
            value=data["titulo"]
        ).classes(
            "w-full"
        ).props(
            "outlined dense"
        )

        sbm = ui.input(
            "SBM",
            value=data["sbm"]
        ).classes(
            "w-full"
        ).props(
            "outlined dense"
        )

        categoria = ui.input(
            "Categoria",
            value=data["categoria"]
        ).classes(
            "w-full"
        ).props(
            "outlined dense"
        )

        quantidade_total = ui.number(
            "Quantidade total",
            value=data["quantidade_total"],
            min=1
        ).classes(
            "w-full"
        ).props(
            "outlined dense"
        )

        # ---------------- SAVE ----------------

        async def save():

            if not titulo.value:

                ui.notify(
                    "Título é obrigatório",
                    type="warning"
                )

                return

            payload = {
                "titulo": titulo.value,
                "sbm": sbm.value,
                "categoria": categoria.value,
                "quantidade_total": int(
                    quantidade_total.value or 1
                )
            }

            try:

                if is_edit:

                    await api.update_book(
                        book["_id"],
                        payload
                    )

                    ui.notify(
                        "Livro atualizado",
                        type="positive"
                    )

                else:

                    await api.create_book(
                        payload
                    )

                    ui.notify(
                        "Livro adicionado",
                        type="positive"
                    )

                dialog.close()

                await on_saved()

            except Exception as e:

                ui.notify(
                    f"Erro: {str(e)}",
                    type="negative"
                )

        # ---------------- BUTTONS ----------------

        with ui.row().classes(
            "w-full justify-end gap-2 mt-4"
        ):

            ui.button(
                "Cancelar",
                on_click=dialog.close
            ).props(
                "flat"
            )

            ui.button(
                "Salvar",
                on_click=save
            ).props(
                "unelevated color=primary"
            )

    dialog.open()