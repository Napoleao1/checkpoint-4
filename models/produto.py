class Produto:
    def __init__(self, nome, quantidade, preco, id=None):
        self.id = id
        self.nome = nome
        self.quantidade = quantidade
        self.preco = preco

    def __str__(self):
        return f"{self.nome} | Qtd: {self.quantidade} | R$ {self.preco:.2f}"
