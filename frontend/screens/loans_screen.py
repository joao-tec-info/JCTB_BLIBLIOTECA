"""Tela de Empréstimos."""
from nicegui import ui

from components.navbar import navbar
from components.sidebar import sidebar
from components.loan_form import open_loan_form
from services.api_service import api
from utils.constants import COLORS
from utils.helpers import format_date


def loans_screen() -> None:
    navbar("Empréstimos")
    sidebar("/emprestimos")

    state = {"tab": "ativos"}

    with ui.column().classes("w-full p-6 gap-4").style(
        f"background-color: {COLORS['background']}; min-height: 100vh;"
    ):
        with ui.row().classes("w-full items-center justify-between"):
            with ui.column().classes("gap-0"):
                ui.label("Empréstimos").classes("text-2xl font-bold")
                ui.label("Controle de retiradas e devoluções.").classes(
                    "text-sm"
                ).style(f"color: {COLORS['text_muted']}")
            ui.button("Novo empréstimo", icon="add",
                      on_click=lambda: open_loan_form(refresh)) \
                .props("unelevated color=primary")

        with ui.card().classes("p-4 rounded-2xl no-shadow w-full").style(
            f"background-color: {COLORS['surface']}; "
            f"border: 1px solid {COLORS['border']};"
        ):
            with ui.tabs().classes("w-full").props("dense align=left") as tabs:
                ui.tab("ativos", label="Ativos")
                ui.tab("historico", label="Histórico")
            tabs.value = state["tab"]
            tabs.on(
                "update:model-value",
                lambda e: (state.update(tab=e.args), refresh()),
            )

            container = ui.column().classes("w-full mt-3")

        def refresh():
            container.clear()
            loans = api.list_loans()
            if state["tab"] == "ativos":
                loans = [l for l in loans if not l["return_date"]]
            else:
                loans = [l for l in loans if l["return_date"]]

            rows = []
            for l in loans:
                student = api.get_student(l["student_id"])
                book = api.get_book(l["book_id"])
                rows.append({
                    "id": l["id"],
                    "aluno": student["name"] if student else "-",
                    "livro": book["title"] if book else "-",
                    "emprestimo": format_date(l["loan_date"]),
                    "devolucao_prevista": format_date(l["due_date"]),
                    "devolucao": format_date(l["return_date"]),
                    "status": api.loan_status(l),
                    "ativo": l["return_date"] is None,
                })

            with container:
                columns = [
                    {"name": "aluno", "label": "Aluno", "field": "aluno", "align": "left"},
                    {"name": "livro", "label": "Livro", "field": "livro", "align": "left"},
                    {"name": "emprestimo", "label": "Empréstimo", "field": "emprestimo", "align": "left"},
                    {"name": "devolucao_prevista", "label": "Prev. devolução",
                     "field": "devolucao_prevista", "align": "left"},
                    {"name": "devolucao", "label": "Devolvido em",
                     "field": "devolucao", "align": "left"},
                    {"name": "status", "label": "Status", "field": "status", "align": "left"},
                    {"name": "actions", "label": "Ações", "field": "actions", "align": "right"},
                ]
                table = ui.table(columns=columns, rows=rows, row_key="id") \
                    .classes("w-full").props("flat")

                table.add_slot("body-cell-status", """
                    <q-td :props="props">
                        <q-badge :color="props.value === 'Ativo' ? 'blue'
                                        : props.value === 'Devolvido' ? 'green' : 'red'"
                                 :label="props.value" class="q-px-sm q-py-xs" />
                    </q-td>
                """)
                table.add_slot("body-cell-actions", r"""
                    <q-td :props="props" class="text-right">
                        <q-btn v-if="props.row.ativo" flat dense color="positive"
                               label="Devolver" icon="check"
                               @click="() => $parent.$emit('return', props.row)" />
                        <q-btn flat round dense icon="delete" color="negative"
                               @click="() => $parent.$emit('delete', props.row)" />
                    </q-td>
                """)
                table.on("return", lambda e: do_return(e.args["id"]))
                table.on("delete", lambda e: do_delete(e.args["id"]))

                if not rows:
                    ui.label("Nenhum empréstimo encontrado.").classes(
                        "text-center w-full p-6"
                    ).style(f"color: {COLORS['text_muted']}")

        def do_return(loan_id: int):
            if api.return_loan(loan_id):
                ui.notify("Livro devolvido", type="positive")
            else:
                ui.notify("Não foi possível devolver", type="warning")
            refresh()

        def do_delete(loan_id: int):
            api.delete_loan(loan_id)
            ui.notify("Empréstimo removido", type="positive")
            refresh()

        refresh()
