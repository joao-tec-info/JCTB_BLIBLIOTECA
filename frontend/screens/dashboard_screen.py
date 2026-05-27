"""Tela Dashboard."""
from datetime import date

from nicegui import ui

from components.navbar import navbar
from components.sidebar import sidebar
from components.dashboard_cards import stat_card
from services.api_service import api
from utils.constants import COLORS
from utils.helpers import format_date


def dashboard_screen() -> None:
    navbar("Dashboard")
    sidebar("/")

    with ui.column().classes("w-full p-6 gap-6").style(
        f"background-color: {COLORS['background']}; min-height: 100vh;"
    ):

        ui.label("Visão geral").classes("text-2xl font-bold")

        ui.label(
            "Resumo do acervo e dos empréstimos da biblioteca."
        ).classes(
            "text-sm"
        ).style(
            f"color: {COLORS['text_muted']}"
        )

        stats_container = ui.row().classes("w-full gap-4 flex-wrap")

        recent_container = ui.column().classes("w-full")

        async def refresh_dashboard():

            # =========================
            # BUSCAR DADOS DA API
            # =========================
            books = await api.list_books()
            students = await api.list_students()
            loans = await api.list_loans()

            # =========================
            # CALCULAR ESTATÍSTICAS
            # =========================
            total_books = sum(
                b.get("quantidade_total", 0)
                for b in books
            )

            available_books = sum(
                b.get("quantidade_disponivel", 0)
                for b in books
            )

            loaned_books = total_books - available_books

            active_loans = sum(
                1 for l in loans
                if not l.get("devolvido")
            )

            overdue_loans = sum(
                1 for l in loans
                if (
                    not l.get("devolvido")
                    and l.get("data_devolucao")
                    and date.fromisoformat(l["data_devolucao"]) < date.today()
                )
            )

            # =========================
            # CARDS
            # =========================
            stats_container.clear()

            with stats_container:

                stat_card(
                    "Total de livros",
                    total_books,
                    "menu_book",
                    COLORS["primary"]
                )

                stat_card(
                    "Disponíveis",
                    available_books,
                    "library_books",
                    COLORS["success"]
                )

                stat_card(
                    "Emprestados",
                    loaned_books,
                    "swap_horiz",
                    COLORS["warning"]
                )

                stat_card(
                    "Alunos cadastrados",
                    len(students),
                    "school",
                    "#8B5CF6"
                )

                stat_card(
                    "Empréstimos ativos",
                    active_loans,
                    "assignment",
                    COLORS["primary"]
                )

                stat_card(
                    "Atrasados",
                    overdue_loans,
                    "warning_amber",
                    COLORS["danger"]
                )

            # =========================
            # TABELA DE EMPRÉSTIMOS
            # =========================
            recent_container.clear()

            with recent_container:

                with ui.card().classes(
                    "p-5 rounded-2xl no-shadow w-full"
                ).style(
                    f"background-color: {COLORS['surface']}; "
                    f"border: 1px solid {COLORS['border']};"
                ):

                    ui.label(
                        "Empréstimos recentes"
                    ).classes(
                        "text-lg font-semibold mb-3"
                    )

                    recent_loans = loans[:6]

                    rows = []

                    for loan in recent_loans:

                        status = (
                            "Devolvido"
                            if loan.get("devolvido")
                            else "Ativo"
                        )

                        rows.append({
                            "aluno": loan["aluno"]["nome"],
                            "livro": loan["livro"]["titulo"],
                            "data": format_date(
                                loan["data_emprestimo"]
                            ),
                            "devolucao": format_date(
                                loan["data_devolucao"]
                            ),
                            "status": status,
                        })

                    columns = [
                        {
                            "name": "aluno",
                            "label": "Aluno",
                            "field": "aluno",
                            "align": "left"
                        },
                        {
                            "name": "livro",
                            "label": "Livro",
                            "field": "livro",
                            "align": "left"
                        },
                        {
                            "name": "data",
                            "label": "Empréstimo",
                            "field": "data",
                            "align": "left"
                        },
                        {
                            "name": "devolucao",
                            "label": "Devolução",
                            "field": "devolucao",
                            "align": "left"
                        },
                        {
                            "name": "status",
                            "label": "Status",
                            "field": "status",
                            "align": "left"
                        },
                    ]

                    table = ui.table(
                        columns=columns,
                        rows=rows,
                        row_key="aluno"
                    ).classes(
                        "w-full"
                    ).props(
                        "flat"
                    )

                    table.add_slot("body-cell-status", """
                        <q-td :props="props">
                            <q-badge
                                :color="
                                    props.value === 'Ativo'
                                    ? 'blue'
                                    : 'green'
                                "
                                :label="props.value"
                                class="q-px-sm q-py-xs"
                            />
                        </q-td>
                    """)

        ui.timer(
            1,
            refresh_dashboard,
            once=True
        )