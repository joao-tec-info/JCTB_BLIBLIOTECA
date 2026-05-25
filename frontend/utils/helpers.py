"""Funções utilitárias."""
from datetime import date, datetime, timedelta


def format_date(d) -> str:
    """Formata uma data para dd/mm/aaaa."""
    if d is None:
        return "-"
    if isinstance(d, str):
        try:
            d = datetime.fromisoformat(d).date()
        except ValueError:
            return d
    if isinstance(d, datetime):
        d = d.date()
    return d.strftime("%d/%m/%Y")


def parse_date(s: str):
    """Converte string ISO para date."""
    if not s:
        return None
    try:
        return datetime.fromisoformat(s).date()
    except ValueError:
        return None


def is_overdue(due_date, returned: bool) -> bool:
    """Verifica se um empréstimo está atrasado."""
    if returned or due_date is None:
        return False
    if isinstance(due_date, str):
        due_date = parse_date(due_date)
    return due_date < date.today()


def default_due_date(days: int = 14) -> date:
    """Data padrão de devolução (14 dias a partir de hoje)."""
    return date.today() + timedelta(days=days)
