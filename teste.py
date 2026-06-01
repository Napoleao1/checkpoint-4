from controller.produto_controller import ProdutoController
from models.produto import Produto

controller = ProdutoController()

# 1. Inserir 3 produtos
controller.inserir(Produto("Arroz Tio João 5kg", 42, 28.90))
controller.inserir(Produto("Feijão Carioca 1kg", 30, 8.50))
controller.inserir(Produto("Macarrão Espaguete", 15, 4.20))

# 2. Listar todos
print()
print("=== ESTOQUE ATUAL ===")
produtos = controller.listar_produtos()
for p in produtos:
    print(p)
