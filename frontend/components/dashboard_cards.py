"""Cards de estatísticas do dashboard."""
from nicegui import ui
from utils.constants import COLORS


def stat_card(title: str, value: str | int, icon: str, color: str) -> None:
    with ui.card().classes("p-5 rounded-2xl no-shadow").style(
        f"background-color: {COLORS['surface']}; "
        f"border: 1px solid {COLORS['border']}; "
        "min-width: 220px; flex: 1;"
    ):
        with ui.row().classes("items-center justify-between w-full"):
            with ui.column().classes("gap-1"):
                ui.label(title).classes("text-sm").style(
                    f"color: {COLORS['text_muted']}"
                )
                ui.label(str(value)).classes("text-3xl font-bold").style(
                    f"color: {COLORS['text']}"
                )
            with ui.element("div").classes(
                "flex items-center justify-center rounded-xl"
            ).style(
                f"background-color: {color}22; width: 52px; height: 52px;"
            ):
                ui.icon(icon, size="28px").style(f"color: {color}")
