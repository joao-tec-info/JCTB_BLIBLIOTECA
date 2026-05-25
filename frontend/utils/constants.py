"""Constantes globais do sistema."""

APP_NAME = "Biblioteca Escolar"
APP_SUBTITLE = "Sistema de Gerenciamento"

# Paleta de cores (azul institucional + branco + tons suaves)
COLORS = {
    "primary": "#1E66F5",        # Azul principal
    "primary_dark": "#1747B5",   # Azul escuro (hover)
    "primary_soft": "#E8F0FE",   # Azul muito claro (fundos)
    "secondary": "#64748B",      # Cinza azulado
    "background": "#F5F7FB",     # Fundo geral
    "surface": "#FFFFFF",        # Cards / superfícies
    "text": "#0F172A",           # Texto principal
    "text_muted": "#64748B",     # Texto secundário
    "success": "#16A34A",
    "warning": "#F59E0B",
    "danger": "#DC2626",
    "border": "#E2E8F0",
}

# Status de empréstimos
STATUS_ATIVO = "Ativo"
STATUS_DEVOLVIDO = "Devolvido"
STATUS_ATRASADO = "Atrasado"

STATUS_COLORS = {
    STATUS_ATIVO: "blue",
    STATUS_DEVOLVIDO: "green",
    STATUS_ATRASADO: "red",
}

# Itens do menu lateral
MENU_ITEMS = [
    {"label": "Dashboard", "icon": "dashboard", "route": "/"},
    {"label": "Livros", "icon": "menu_book", "route": "/livros"},
    {"label": "Alunos", "icon": "school", "route": "/alunos"},
    {"label": "Empréstimos", "icon": "swap_horiz", "route": "/emprestimos"},
]
