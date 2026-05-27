"""Tela de Alunos."""

from nicegui import ui

from components.navbar import navbar
from components.sidebar import sidebar
from components.student_form import open_student_form
from services.api_service import api
from utils.constants import COLORS


def students_screen() -> None:

    navbar("Alunos")
    sidebar("/alunos")

    state = {
        "search": ""
    }

    with ui.column().classes(
        "w-full p-6 gap-4"
    ).style(
        f"background-color: {COLORS['background']}; min-height: 100vh;"
    ):

        # HEADER

        with ui.row().classes(
            "w-full items-center justify-between"
        ):

            with ui.column().classes("gap-0"):

                ui.label(
                    "Alunos"
                ).classes(
                    "text-2xl font-bold"
                )

                ui.label(
                    "Cadastro e gerenciamento de alunos."
                ).classes(
                    "text-sm"
                ).style(
                    f"color: {COLORS['text_muted']}"
                )

            ui.button(
                "Adicionar aluno",
                icon="add",
                on_click=lambda: open_student_form(
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
                    placeholder="Buscar por nome ou turma"
                ).classes(
                    "flex-1"
                ).props(
                    "outlined dense clearable"
                )

                search.on(
                    "update:model-value",
                    lambda e: (
                        state.update(
                            search=e.args or ""
                        ),
                        refresh()
                    )
                )

            container = ui.column().classes("w-full")

        # REFRESH

        async def refresh():

            container.clear()

            try:

                students = await api.list_students()

                search_text = (
                    state["search"]
                    .lower()
                    .strip()
                )

                if search_text:

                    students = [
                        s for s in students
                        if (
                            search_text in s["nome"].lower()
                            or search_text in s["turma"].lower()
                        )
                    ]

                with container:

                    rows = [

                        {
                            "id": s["_id"],
                            "nome": s["nome"],
                            "turma": s["turma"],
                        }

                        for s in students
                    ]

                    columns = [

                        {
                            "name": "nome",
                            "label": "Nome",
                            "field": "nome",
                            "align": "left"
                        },

                        {
                            "name": "turma",
                            "label": "Turma",
                            "field": "turma",
                            "align": "left"
                        },

                        {
                            "name": "actions",
                            "label": "Ações",
                            "field": "actions",
                            "align": "right"
                        },

                    ]

                    table = ui.table(
                        columns=columns,
                        rows=rows,
                        row_key="id"
                    ).classes(
                        "w-full"
                    ).props(
                        "flat"
                    )

                    table.add_slot(
                        "body-cell-actions",
                        r"""
                        <q-td :props="props" class="text-right">

                            <q-btn
                                flat
                                round
                                dense
                                icon="edit"
                                color="primary"
                                @click="() => $parent.$emit('edit', props.row)"
                            />

                            <q-btn
                                flat
                                round
                                dense
                                icon="delete"
                                color="negative"
                                @click="() => $parent.$emit('delete', props.row)"
                            />

                        </q-td>
                        """
                    )

                    table.on(
                        "edit",
                        lambda e: open_student_form(
                            e.args,
                            refresh
                        )
                    )

                    table.on(
                        "delete",
                        lambda e: confirm_delete(
                            e.args["id"]
                        )
                    )

                    if not rows:

                        ui.label(
                            "Nenhum aluno encontrado."
                        ).classes(
                            "text-center w-full p-6"
                        ).style(
                            f"color: {COLORS['text_muted']}"
                        )

            except Exception as e:

                with container:

                    ui.label(
                        f"Erro ao carregar alunos: {str(e)}"
                    ).classes(
                        "text-negative"
                    )

        # DELETE

        def confirm_delete(student_id: str):

            with ui.dialog() as d, ui.card().classes(
                "p-5 rounded-2xl"
            ):

                ui.label(
                    "Excluir aluno?"
                ).classes(
                    "text-lg font-bold"
                )

                ui.label(
                    "Essa ação não pode ser desfeita."
                ).classes(
                    "text-sm text-gray-500"
                )

                with ui.row().classes(
                    "justify-end gap-2 mt-4"
                ):

                    ui.button(
                        "Cancelar",
                        on_click=d.close
                    ).props(
                        "flat"
                    )

                    async def do():

                        try:

                            await api.delete_student(
                                student_id
                            )

                            ui.notify(
                                "Aluno excluído",
                                type="positive"
                            )

                            d.close()

                            await refresh()

                        except Exception as e:

                            ui.notify(
                                str(e),
                                type="negative"
                            )

                    ui.button(
                        "Excluir",
                        on_click=do
                    ).props(
                        "unelevated color=negative"
                    )

            d.open()

        ui.timer(
            0.1,
            refresh,
            once=True
        )