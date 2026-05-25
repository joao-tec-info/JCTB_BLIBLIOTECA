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

    state = {"search": ""}

    with ui.column().classes("w-full p-6 gap-4").style(
        f"background-color: {COLORS['background']}; min-height: 100vh;"
    ):
        with ui.row().classes("w-full items-center justify-between"):
            with ui.column().classes("gap-0"):
                ui.label("Alunos").classes("text-2xl font-bold")
                ui.label("Cadastro e gerenciamento de alunos.").classes(
                    "text-sm"
                ).style(f"color: {COLORS['text_muted']}")
            ui.button("Adicionar aluno", icon="add",
                      on_click=lambda: open_student_form(None, refresh)) \
                .props("unelevated color=primary")

        with ui.card().classes("p-4 rounded-2xl no-shadow w-full").style(
            f"background-color: {COLORS['surface']}; "
            f"border: 1px solid {COLORS['border']};"
        ):
            with ui.row().classes("w-full items-center gap-3 mb-3"):
                search = ui.input(placeholder="Buscar por nome, matrícula ou turma") \
                    .classes("flex-1").props("outlined dense clearable")
                search.on(
                    "update:model-value",
                    lambda e: (state.update(search=e.args or ""), refresh()),
                )

            container = ui.column().classes("w-full")

        def refresh():
            container.clear()
            students = api.list_students(state["search"])
            with container:
                rows = [{
                    "id": s["id"],
                    "name": s["name"],
                    "registration": s["registration"],
                    "class_name": s["class_name"],
                    "phone": s["phone"],
                    "email": s["email"],
                } for s in students]

                columns = [
                    {"name": "name", "label": "Nome", "field": "name", "align": "left"},
                    {"name": "registration", "label": "Matrícula", "field": "registration", "align": "left"},
                    {"name": "class_name", "label": "Turma", "field": "class_name", "align": "left"},
                    {"name": "phone", "label": "Telefone", "field": "phone", "align": "left"},
                    {"name": "email", "label": "Email", "field": "email", "align": "left"},
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
                table.on("edit", lambda e: open_student_form(
                    api.get_student(e.args["id"]), refresh))
                table.on("delete", lambda e: confirm_delete(e.args["id"]))

                if not rows:
                    ui.label("Nenhum aluno encontrado.").classes(
                        "text-center w-full p-6"
                    ).style(f"color: {COLORS['text_muted']}")

        def confirm_delete(sid: int):
            with ui.dialog() as d, ui.card().classes("p-5 rounded-2xl"):
                ui.label("Excluir aluno?").classes("text-lg font-bold")
                ui.label("Essa ação não pode ser desfeita.").classes(
                    "text-sm text-gray-500"
                )
                with ui.row().classes("justify-end gap-2 mt-4"):
                    ui.button("Cancelar", on_click=d.close).props("flat")

                    def do():
                        api.delete_student(sid)
                        ui.notify("Aluno excluído", type="positive")
                        d.close()
                        refresh()
                    ui.button("Excluir", on_click=do).props(
                        "unelevated color=negative"
                    )
            d.open()

        refresh()
