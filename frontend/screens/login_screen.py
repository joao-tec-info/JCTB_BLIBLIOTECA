"""Tela de Login (visual, sem autenticação real)."""
from nicegui import ui
from utils.constants import APP_NAME, APP_SUBTITLE, COLORS


def login_screen() -> None:
    with ui.element("div").classes(
        "w-full min-h-screen flex items-center justify-center"
    ).style(f"background-color: {COLORS['background']};"):
        with ui.card().classes("p-8 rounded-2xl no-shadow w-[400px]").style(
            f"background-color: {COLORS['surface']}; "
            f"border: 1px solid {COLORS['border']};"
        ):
            with ui.column().classes("items-center w-full gap-2 mb-4"):
                ui.icon("auto_stories", size="48px").style(
                    f"color: {COLORS['primary']}"
                )
                ui.label(APP_NAME).classes("text-xl font-bold")
                ui.label(APP_SUBTITLE).classes("text-sm").style(
                    f"color: {COLORS['text_muted']}"
                )

            ui.input("Usuário").classes("w-full").props("outlined dense")
            ui.input("Senha", password=True, password_toggle_button=True) \
                .classes("w-full").props("outlined dense")

            ui.button("Entrar", on_click=lambda: ui.navigate.to("/")) \
                .classes("w-full mt-3").props("unelevated color=primary")

            ui.label("Sistema interno da biblioteca escolar.").classes(
                "text-xs text-center mt-3"
            ).style(f"color: {COLORS['text_muted']}")
