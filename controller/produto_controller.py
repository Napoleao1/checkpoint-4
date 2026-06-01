from config.init_banco import BancoDados
from models.produto import Produto
import sqlite3


class ProdutoController:
    def __init__(self):
        self.banco = BancoDados()

    def inserir(self, produto):
        conexao = self.banco.conectar()
        try:
            with conexao:
                cursor = conexao.cursor()
                cursor.execute(
                    "INSERT INTO produtos (nome, quantidade, preco) VALUES (?, ?, ?)",
                    (produto.nome, produto.quantidade, produto.preco),
                )
        except sqlite3.Error as e:
            print(f"Erro ao inserir: {e}")
        finally:
            conexao.close()

    def listar_produtos(self):
        conexao = self.banco.conectar()
        produtos = []
        try:
            with conexao:
                cursor = conexao.cursor()
                cursor.execute(
                    "SELECT id, nome, quantidade, preco FROM produtos ORDER BY id"
                )
                linhas = cursor.fetchall()
                for id_p, nome, quantidade, preco in linhas:
                    produtos.append(Produto(nome, quantidade, preco, id=id_p))
        except sqlite3.Error as e:
            print(f"Erro ao listar: {e}")
        finally:
            conexao.close()
        return produtos

    def atualizar(self, id_produto, produto):
        conexao = self.banco.conectar()
        try:
            with conexao:
                cursor = conexao.cursor()
                cursor.execute(
                    "UPDATE produtos SET nome = ?, quantidade = ?, preco = ? WHERE id = ?",
                    (produto.nome, produto.quantidade, produto.preco, id_produto),
                )
        except sqlite3.Error as e:
            print(f"Erro ao atualizar: {e}")
        finally:
            conexao.close()

    def deletar(self, id_produto):
        conexao = self.banco.conectar()
        try:
            with conexao:
                cursor = conexao.cursor()
                cursor.execute(
                    "DELETE FROM produtos WHERE id = ?",
                    (id_produto,),
                )
        except sqlite3.Error as e:
            print(f"Erro ao deletar: {e}")
        finally:
            conexao.close()

    def processar_cadastro(self, nome, quantidade, preco):
        if nome == "" or quantidade == "" or preco == "":
            return False, "Campos vazios!"

        try:
            quantidade_int = int(quantidade)
            preco_float = float(preco)
        except ValueError:
            return False, "Erro nos números! Quantidade inteiro, preço decimal."

        if quantidade_int < 0 or preco_float < 0:
            return False, "Valores não podem ser negativos!"

        produto = Produto(nome, quantidade_int, preco_float)
        self.inserir(produto)
        return True, "Produto cadastrado!"

    def processar_atualizacao(self, id_produto, nome, quantidade, preco):
        if id_produto == "" or nome == "" or quantidade == "" or preco == "":
            return False, "Campos vazios!"

        try:
            id_int = int(id_produto)
            quantidade_int = int(quantidade)
            preco_float = float(preco)
        except ValueError:
            return False, "Erro nos números!"

        produto = Produto(nome, quantidade_int, preco_float)
        self.atualizar(id_int, produto)
        return True, "Produto atualizado!"

    def processar_exclusao(self, id_produto):
        if id_produto == "":
            return False, "Selecione um produto pelo ID!"

        try:
            id_int = int(id_produto)
        except ValueError:
            return False, "ID inválido!"

        self.deletar(id_int)
        return True, "Produto excluído!"
