class Book:
    def __init__(
        self,
        titulo,
        sbm,
        quantidade_total,
        categoria
    ):
        self.titulo = titulo
        self.sbm = sbm
        self.quantidade_total = quantidade_total
        self.quantidade_disponivel = quantidade_total
        self.categoria = categoria