import sqlite3

class BancoDados:  
    def __init__(self, nome_arquivo="estoque.db"):
        self.nome_arquivo = nome_arquivo
        
    
    def conectar(self):
        return sqlite3.connect(self.nome_arquivo)
        
        
    def criar_tabelas(self):
        conexao = self.conectar()
        try:
            with conexao:
                cursor = conexao.cursor()
                cursor.execute("""
                    CREATE TABLE IF NOT EXISTS produtos (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        nome TEXT NOT NULL,
                        quantidade INTEGER NOT NULL,
                        preco REAL NOT NULL
                    )
                    """)
        except sqlite3.Error as e:
            print(f"Erro ao criar tabela: {e}")
        finally:
            conexao.close()
            
            
banco = BancoDados()
banco.criar_tabelas()
