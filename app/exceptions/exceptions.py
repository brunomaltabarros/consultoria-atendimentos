class ExcecaoAplicacao(Exception):
    def __init__(self, messagem: str):
        self.messagem = messagem
        super().__init__(self.messagem)

class ExcecaoNaoEncontrado(ExcecaoAplicacao):
    pass

class ExcecaoConflito(ExcecaoAplicacao):
    pass