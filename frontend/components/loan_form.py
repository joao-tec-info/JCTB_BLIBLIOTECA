"""Modal de formulário de empréstimo."""

from datetime import date, timedelta

from nicegui import ui

from services.api_service import api


def open_loan_form(on_saved) -> None:

    with ui.dialog() as dialog, ui.card().classes(
        "p-6 rounded-2xl w-[520px]"
    ):

        ui.label(
            "Novo Empréstimo"
        ).classes(
            "text-xl font-bold mb-2"
        )

        ui.label(
            "Selecione o aluno e o livro."
        ).classes(
            "text-sm text-gray-500 mb-4"
        )

        loading = ui.label(
            "Carregando dados..."
        )

        # COMPONENTES

        student_sel = ui.select(
            {},
            label="Aluno"
        ).classes(
            "w-full"
        ).props(
            "outlined dense"
        )

        book_sel = ui.select(
            {},
            label="Livro"
        ).classes(
            "w-full"
        ).props(
            "outlined dense"
        )

        with ui.row().classes(
            "w-full gap-3 no-wrap"
        ):

            loan_date = ui.input(
                "Data do empréstimo",
                value=date.today().isoformat()
            ).classes(
                "flex-1"
            ).props(
                "outlined dense type=date"
            )

            due_date = ui.input(
                "Devolução prevista",
                value=(
                    date.today() + timedelta(days=7)
                ).isoformat()
            ).classes(
                "flex-1"
            ).props(
                "outlined dense type=date"
            )

        # LOAD DATA

        async def load_data():

            try:

                students = await api.list_students()

                books = await api.list_books()

                # somente disponíveis

                books = [

                    b for b in books

                    if b["quantidade_disponivel"] > 0

                ]

                student_sel.options = {

                    s["_id"]: (
                        f'{s["nome"]} '
                        f'({s["turma"]})'
                    )

                    for s in students
                }

                book_sel.options = {

                    b["_id"]: (
                        f'{b["titulo"]} '
                        f'({b["quantidade_disponivel"]} disponíveis)'
                    )

                    for b in books
                }

                loading.set_visibility(False)

            except Exception as e:

                loading.text = (
                    f"Erro ao carregar dados: {str(e)}"
                )

        # SAVE

        async def save():

            if not student_sel.value:

                ui.notify(
                    "Selecione um aluno",
                    type="warning"
                )

                return

            if not book_sel.value:

                ui.notify(
                    "Selecione um livro",
                    type="warning"
                )

                return

            payload = {

                "student_id": student_sel.value,

                "book_id": book_sel.value,

                "data_emprestimo": loan_date.value,

                "data_devolucao": due_date.value,

            }

            try:

                await api.create_loan(
                    payload
                )

                ui.notify(
                    "Empréstimo registrado",
                    type="positive"
                )

                dialog.close()

                await on_saved()

            except Exception as e:

                ui.notify(
                    f"Erro: {str(e)}",
                    type="negative"
                )

        # BUTTONS

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
                "Registrar",
                on_click=save
            ).props(
                "unelevated color=primary"
            )

        ui.timer(
            0.1,
            load_data,
            once=True
        )

    dialog.open()