"""Sidebar lateral fixa."""
from nicegui import ui
from utils.constants import APP_NAME, APP_SUBTITLE, COLORS, MENU_ITEMS


def sidebar(active_route: str = "/") -> None:
    with ui.left_drawer(fixed=True, bordered=False).props(
        "width=260 behavior=desktop"
    ).style(
        f"background-color: {COLORS['surface']}; "
        f"border-right: 1px solid {COLORS['border']};"
    ):
        with ui.column().classes("w-full h-full p-4 gap-2"):
            # Logo / título
            with ui.row().classes("items-center gap-3 px-2 py-3"):
                ui.icon("auto_stories", size="32px").style(
                    f"color: {COLORS['primary']}"
                )
                with ui.column().classes("gap-0"):
                    ui.label(APP_NAME).classes("text-base font-bold")
                    ui.label(APP_SUBTITLE).classes("text-xs").style(
                        f"color: {COLORS['text_muted']}"
                    )

            ui.separator().classes("my-2")

            # Itens de menu
            for item in MENU_ITEMS:
                is_active = item["route"] == active_route
                bg = COLORS["primary_soft"] if is_active else "transparent"
                color = COLORS["primary"] if is_active else COLORS["text"]
                weight = "600" if is_active else "500"

                with ui.row().classes(
                    "w-full items-center gap-3 px-3 py-2 cursor-pointer rounded-lg"
                ).style(
                    f"background-color: {bg}; color: {color}; font-weight: {weight};"
                ).on("click", lambda r=item["route"]: ui.navigate.to(r)):
                    ui.icon(item["icon"], size="22px")
                    ui.label(item["label"]).classes("text-sm")

            ui.space()

            ui.separator().classes("my-2")
            with ui.row().classes(
                "w-full items-center gap-3 px-3 py-2 cursor-pointer rounded-lg"
            ).style(f"color: {COLORS['text_muted']}").on(
                "click", lambda: ui.notify("Configurações em breve")
            ):
                ui.icon("settings", size="22px")
                ui.label("Configurações").classes("text-sm")
