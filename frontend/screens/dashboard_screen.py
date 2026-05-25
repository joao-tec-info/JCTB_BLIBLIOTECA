"""Tela Dashboard."""
from nicegui import ui

from components.navbar import navbar
from components.sidebar import sidebar
from components.dashboard_cards import stat_card
from services.api_service import api
from utils.constants import COLORS, STATUS_COLORS
from utils.helpers import format_date


def dashboard_screen() -> None:
    navbar("Dashboard")
    sidebar("/")

    stats = api.dashboard_stats()

    with ui.column().classes("w-full p-6 gap-6").style(
        f"background-color: {COLORS['background']}; min-height: 100vh;"
    ):
        ui.label("Visão geral").classes("text-2xl font-bold")
        ui.label("Resumo do acervo e dos empréstimos da biblioteca.").classes(
            "text-sm"
        ).style(f"color: {COLORS['text_muted']}")

        with ui.row().classes("w-full gap-4 flex-wrap"):
            stat_card("Total de livros", stats["total_books"],
                      "menu_book", COLORS["primary"])
            stat_card("Disponíveis", stats["available_books"],
                      "library_books", COLORS["success"])
            stat_card("Emprestados", stats["loaned_books"],
                      "swap_horiz", COLORS["warning"])
            stat_card("Alunos cadastrados", stats["total_students"],
                      "school", "#8B5CF6")
            stat_card("Empréstimos ativos", stats["active_loans"],
                      "assignment", COLORS["primary"])
            stat_card("Atrasados", stats["overdue_loans"],
                      "warning_amber", COLORS["danger"])

        with ui.card().classes("p-5 rounded-2xl no-shadow w-full").style(
            f"background-color: {COLORS['surface']}; "
            f"border: 1px solid {COLORS['border']};"
        ):
            ui.label("Empréstimos recentes").classes("text-lg font-semibold mb-3")

            rows = []
            for l in api.recent_loans(6):
                student = api.get_student(l["student_id"])
                book = api.get_book(l["book_id"])
                status = api.loan_status(l)
                rows.append({
                    "aluno": student["name"] if student else "-",
                    "livro": book["title"] if book else "-",
                    "data": format_date(l["loan_date"]),
                    "devolucao": format_date(l["due_date"]),
                    "status": status,
                })

            columns = [
                {"name": "aluno", "label": "Aluno", "field": "aluno", "align": "left"},
                {"name": "livro", "label": "Livro", "field": "livro", "align": "left"},
                {"name": "data", "label": "Empréstimo", "field": "data", "align": "left"},
                {"name": "devolucao", "label": "Devolução", "field": "devolucao", "align": "left"},
                {"name": "status", "label": "Status", "field": "status", "align": "left"},
            ]
            table = ui.table(columns=columns, rows=rows, row_key="aluno") \
                .classes("w-full").props("flat")
            table.add_slot("body-cell-status", """
                <q-td :props="props">
                    <q-badge :color="props.value === 'Ativo' ? 'blue'
                                    : props.value === 'Devolvido' ? 'green' : 'red'"
                             :label="props.value" class="q-px-sm q-py-xs" />
                </q-td>
            """)
