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
        
    def emprestar(self):
        if self.quantidade_disponivel > 0:
            self.quantidade_disponivel -= 1
            return True

        return False
    
    def devolver(self):
        if self.quantidade_disponivel < self.quantidade_total:
            self.quantidade_disponivel += 1

    def to_dict(self):
        return {
            "titulo": self.titulo,
            "sbm": self.sbm,
            "quantidade_total": self.quantidade_total,
            "quantidade_disponivel": self.quantidade_disponivel,
            "categoria": self.categoria
        }