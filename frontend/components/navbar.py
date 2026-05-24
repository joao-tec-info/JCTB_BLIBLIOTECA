from nicegui import ui


def navbar():

    with ui.row().classes(
        'w-full bg-blue-600 p-4 items-center'
    ):

        ui.label(
            'JCTB Biblioteca'
        ).classes(
            'text-white text-xl font-bold'
        )

        ui.button(
            'Livros',
            on_click=lambda: ui.navigate.to('/')
        )

        ui.button(
            'Alunos',
            on_click=lambda: ui.navigate.to('/students')
        )

        ui.button(
            'Empréstimos',
            on_click=lambda: ui.navigate.to('/loans')
        )