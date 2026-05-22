class Loan:
    def __init__(
        self,
        aluno,
        livro,
        data_emprestimo,
        data_devolucao
    ):
        self.aluno = aluno
        self.livro = livro
        self.data_emprestimo = data_emprestimo
        self.data_devolucao = data_devolucao
        self.devolvido = False
        
    def marcar_devolvido(self):
        self.devolvido = True

    def to_dict(self):
        return {
            "aluno": self.aluno,
            "livro": self.livro,
            "data_emprestimo": self.data_emprestimo,
            "data_devolucao": self.data_devolucao,
            "devolvido": self.devolvido
        }