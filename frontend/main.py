import flet as ft


def main(page: ft.Page):

    page.title = "JCTB Biblioteca"

    page.add(
        ft.Text("Frontend funcionando")
    )


ft.app(target=main)