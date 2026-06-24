"""
Sistema de Biblioteca Escolar — Frontend NiceGUI.

Executar:
    pip install nicegui
    python main.py

A integração com a API FastAPI/MongoDB deve ser feita posteriormente em
services/api_service.py, mantendo a mesma interface pública.
"""
from nicegui import ui
import os
from screens.dashboard_screen import dashboard_screen
from screens.books_screen import books_screen
from screens.students_screen import students_screen
from screens.loans_screen import loans_screen
from screens.login_screen import login_screen
from utils.constants import APP_NAME, COLORS


# Estilos globais
ESTILOS_GLOBAIS = f"""
<style>
  body {{
    background-color: {COLORS['background']};
    font-family: 'Inter', 'Roboto', sans-serif;
  }}
  .q-table thead th {{
    font-weight: 600;
    color: {COLORS['text_muted']};
    background-color: {COLORS['background']};
  }}
  .q-table tbody td {{
    border-bottom: 1px solid {COLORS['border']};
  }}
</style>
"""
ui.add_head_html(
    ESTILOS_GLOBAIS,
    shared=True
)


@ui.page("/")
def page_dashboard():
    dashboard_screen()


@ui.page("/livros")
def page_books():
    books_screen()


@ui.page("/alunos")
def page_students():
    students_screen()


@ui.page("/emprestimos")
def page_loans():
    loans_screen()


@ui.page("/login")
def page_login():
    login_screen()



ui.run(
    title=APP_NAME,
    favicon="📚",
    reload=False,
    host="0.0.0.0",
    port=int(os.environ.get("PORT", 8080)),
)