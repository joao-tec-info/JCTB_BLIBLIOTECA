"""Modal de formulário de aluno."""

from nicegui import ui

from services.api_service import api


def open_student_form(student: dict |None, on_saved) -> None:

    is_edit = student is not None

    s = student or {}

    with ui.dialog() as dialog, ui.card().classes(
        "p-6 rounded-2xl w-[520px]"
    ):

        ui.label(
            "Editar Aluno" if is_edit else "Novo Aluno"
        ).classes(
            "text-xl font-bold mb-2"
        )

        ui.label(
            "Dados do aluno."
        ).classes(
            "text-sm text-gray-500 mb-4"
        )

        # ---------------- INPUTS ----------------

        nome = ui.input(
            "Nome completo",
            value=s.get("nome", "")
        ).classes(
            "w-full"
        ).props(
            "outlined dense"
        )

        turma = ui.input(
            "Turma",
            value=s.get("turma", "")
        ).classes(
            "w-full"
        ).props(
            "outlined dense"
        )

        # ---------------- SAVE ----------------

        async def save():

            if not nome.value:

                ui.notify(
                    "Nome é obrigatório",
                    type="warning"
                )

                return

            payload = {

                "nome": nome.value,
                "turma": turma.value,

            }

            try:

                if is_edit:

                    await api.update_student(
                        s["id"],
                        payload
                    )

                    ui.notify(
                        "Aluno atualizado",
                        type="positive"
                    )

                else:

                    await api.create_student(
                        payload
                    )

                    ui.notify(
                        "Aluno cadastrado",
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