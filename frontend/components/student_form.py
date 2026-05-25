"""Modal de formulário de aluno."""
from nicegui import ui
from services.api_service import api


def open_student_form(student: dict | None, on_saved) -> None:
    is_edit = student is not None
    s = student or {}

    with ui.dialog() as dialog, ui.card().classes("p-6 rounded-2xl w-[520px]"):
        ui.label("Editar Aluno" if is_edit else "Novo Aluno").classes(
            "text-xl font-bold mb-2"
        )
        ui.label("Dados do aluno.").classes("text-sm text-gray-500 mb-4")

        name = ui.input("Nome completo", value=s.get("name", "")) \
            .classes("w-full").props("outlined dense")
        with ui.row().classes("w-full gap-3 no-wrap"):
            registration = ui.input("Matrícula", value=s.get("registration", "")) \
                .classes("flex-1").props("outlined dense")
            class_name = ui.input("Turma", value=s.get("class_name", "")) \
                .classes("flex-1").props("outlined dense")
        with ui.row().classes("w-full gap-3 no-wrap"):
            phone = ui.input("Telefone", value=s.get("phone", "")) \
                .classes("flex-1").props("outlined dense")
            email = ui.input("Email", value=s.get("email", "")) \
                .classes("flex-1").props("outlined dense")

        def save():
            if not name.value or not registration.value:
                ui.notify("Nome e matrícula são obrigatórios", type="warning")
                return
            payload = {
                "name": name.value, "registration": registration.value,
                "class_name": class_name.value, "phone": phone.value,
                "email": email.value,
            }
            if is_edit:
                api.update_student(student["id"], payload)
                ui.notify("Aluno atualizado", type="positive")
            else:
                api.create_student(payload)
                ui.notify("Aluno cadastrado", type="positive")
            dialog.close()
            on_saved()

        with ui.row().classes("w-full justify-end gap-2 mt-4"):
            ui.button("Cancelar", on_click=dialog.close).props("flat")
            ui.button("Salvar", on_click=save).props("unelevated color=primary")

    dialog.open()
