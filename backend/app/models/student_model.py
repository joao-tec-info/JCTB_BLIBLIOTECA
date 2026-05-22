class Student:
    def __init__(self, nome, turma):
        self.nome = nome
        self.turma = turma

    def to_dict(self):
        return {
            "nome": self.nome,
            "turma": self.turma
        }
    
    