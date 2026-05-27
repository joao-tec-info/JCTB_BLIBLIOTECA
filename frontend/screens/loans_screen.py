"""Tela de Empréstimos."""

from datetime import date

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

    state = {
        "tab": "ativos"
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
                    "Empréstimos"
                ).classes(
                    "text-2xl font-bold"
                )

                ui.label(
                    "Controle de retiradas e devoluções."
                ).classes(
                    "text-sm"
                ).style(
                    f"color: {COLORS['text_muted']}"
                )

            ui.button(
                "Novo empréstimo",
                icon="add",
                on_click=lambda: open_loan_form(
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

            with ui.tabs().classes(
                "w-full"
            ).props(
                "dense align=left"
            ) as tabs:

                ui.tab(
                    "ativos",
                    label="Ativos"
                )

                ui.tab(
                    "historico",
                    label="Histórico"
                )

            tabs.value = state["tab"]

            tabs.on(
                "update:model-value",
                lambda e: (
                    state.update(tab=e.args),
                    refresh()
                )
            )

            container = ui.column().classes(
                "w-full mt-3"
            )

        # REFRESH

        async def refresh():

            container.clear()

            try:

                loans = await api.list_loans()

                rows = []

                for loan in loans:

                    devolvido = loan.get(
                        "devolvido",
                        False
                    )

                    if state["tab"] == "ativos":

                        if devolvido:
                            continue

                    else:

                        if not devolvido:
                            continue

                    data_devolucao = loan.get(
                        "data_devolucao"
                    )

                    status = "Ativo"

                    if devolvido:
                        status = "Devolvido"

                    else:

                        try:

                            if data_devolucao:

                                vencimento = date.fromisoformat(
                                    data_devolucao
                                )

                                if vencimento < date.today():
                                    status = "Atrasado"

                        except:
                            pass

                    rows.append({

                        "id": loan["_id"],

                        "aluno": loan["aluno"]["nome"],

                        "livro": loan["livro"]["titulo"],

                        "emprestimo": format_date(
                            loan["data_emprestimo"]
                        ),

                        "devolucao_prevista": format_date(
                            loan["data_devolucao"]
                        ),

                        "status": status,

                    })

                with container:

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
                            "name": "emprestimo",
                            "label": "Empréstimo",
                            "field": "emprestimo",
                            "align": "left"
                        },

                        {
                            "name": "devolucao_prevista",
                            "label": "Prev. devolução",
                            "field": "devolucao_prevista",
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
                        row_key="id"
                    ).classes(
                        "w-full"
                    ).props(
                        "flat"
                    )

                    table.add_slot(
                        "body-cell-status",
                        """
                        <q-td :props="props">

                            <q-badge
                                :color="
                                    props.value === 'Ativo'
                                    ? 'blue'
                                    : props.value === 'Devolvido'
                                    ? 'green'
                                    : 'red'
                                "
                                :label="props.value"
                                class="q-px-sm q-py-xs"
                            />

                        </q-td>
                        """
                    )

                    if not rows:

                        ui.label(
                            "Nenhum empréstimo encontrado."
                        ).classes(
                            "text-center w-full p-6"
                        ).style(
                            f"color: {COLORS['text_muted']}"
                        )

            except Exception as e:

                with container:

                    ui.label(
                        f"Erro ao carregar empréstimos: {str(e)}"
                    ).classes(
                        "text-negative"
                    )

        ui.timer(
            0.1,
            refresh,
            once=True
        )