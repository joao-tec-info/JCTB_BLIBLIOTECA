from nicegui import ui

from services.api_service import ApiService


@ui.page('/')
async def books_screen():

    ui.label(
        'Livros'
    ).classes(
        'text-3xl font-bold'
    )

    books = await ApiService.get_books()

    for book in books:

        with ui.card().classes('w-full'):

            ui.label(
                book['titulo']
            ).classes(
                'text-xl font-bold'
            )

            ui.label(
                f"SBM: {book['sbm']}"
            )

            ui.label(
                f"Disponíveis: {book['quantidade_disponivel']}"
            )