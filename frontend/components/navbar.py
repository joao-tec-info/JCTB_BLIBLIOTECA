"""Navbar superior."""
from nicegui import ui
from utils.constants import APP_NAME, COLORS


def navbar(page_title: str = "") -> None:
    with ui.header(elevated=False).classes(
        "items-center justify-between px-6 py-3"
    ).style(
        f"background-color: {COLORS['surface']}; "
        f"color: {COLORS['text']}; "
        f"border-bottom: 1px solid {COLORS['border']};"
    ):
        with ui.row().classes("items-center gap-3"):
            ui.icon("menu_book", size="28px").style(f"color: {COLORS['primary']}")
            with ui.column().classes("gap-0"):
                ui.label(APP_NAME).classes("text-base font-bold")
                if page_title:
                    ui.label(page_title).classes("text-xs").style(
                        f"color: {COLORS['text_muted']}"
                    )

        with ui.row().classes("items-center gap-3"):
            ui.button(icon="notifications", on_click=lambda: ui.notify("Sem notificações")) \
                .props("flat round dense").style(f"color: {COLORS['secondary']}")
            with ui.row().classes("items-center gap-2"):
                ui.avatar("F", color="primary", text_color="white", size="32px")
                with ui.column().classes("gap-0"):
                    ui.label("Funcionário").classes("text-sm font-semibold")
                    ui.label("Biblioteca").classes("text-xs").style(
                        f"color: {COLORS['text_muted']}"
                    )
