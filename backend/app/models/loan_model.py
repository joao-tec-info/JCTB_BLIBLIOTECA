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