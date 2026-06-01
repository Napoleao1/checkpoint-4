# Checkpoint-4 — Sistema de Controle de Estoque

## Contexto do projeto
- **O que é:** Sistema de controle de estoque em Python com SQLite.
- **Estrutura:** MVC (`config/`, `controller/`, `models/`, `views/`).
- **Banco escolhido:** SQLite (arquivo `.db` local).
- **Abordagem escolhida:** POO (classe `BancoDados`) — Forma 7 da explicação.

## O que eu aprendi hoje

### 1. Conexão com SQLite
- `sqlite3.connect("nome.db")` cria/abre o arquivo do banco automaticamente.
- Se o arquivo não existir, o SQLite cria.
- Se existir, ele só abre.

### 2. Cursor
- O **cursor** é quem executa SQL e lê resultados.
- Analogia: conexão = porta do restaurante / cursor = garçom.
- Uma conexão pode ter vários cursores.

### 3. `with` (gerenciador de contexto)
- `with conexao:` faz **commit automático** se tudo der certo.
- Faz **rollback automático** se der erro.
- **ATENÇÃO:** no SQLite, o `with` NÃO fecha a conexão — só faz commit/rollback.

### 4. `try / except / finally`
- `try`: código que PODE dar erro.
- `except`: SÓ executa se der erro.
- `finally`: SEMPRE executa (com ou sem erro).
- Uso clássico: fechar conexão/arquivo no `finally`.

### 5. Padrão "profissional" de conexão
```python
conexao = conectar()
try:
    with conexao:
        cursor = conexao.cursor()
        cursor.execute(...)
except sqlite3.Error as e:
    print(f"Erro: {e}")
finally:
    conexao.close()
```

### 6. Classe (POO) aplicada ao banco
- `__init__(self, ...)` é o construtor (roda quando criamos o objeto).
- `self.atributo` guarda dados dentro do objeto.
- Cada `BancoDados(...)` cria uma **instância nova**, independente.
- Permite criar vários bancos diferentes com o mesmo código (abstração).

## Esqueleto que vou continuar em casa

### `config/init_banco.py`
```python
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
                        quantidade INTEGER NOT NULL DEFAULT 0,
                        preco REAL NOT NULL
                    )
                """)
        except sqlite3.Error as e:
            print(f"Erro ao criar tabela: {e}")
        finally:
            conexao.close()
```

## Próximos passos do projeto
1. Finalizar `criar_tabelas()` na classe `BancoDados`.
2. Criar `models/produto.py` (entidade Produto).
3. Criar `controller/produto_controller.py` (inserir, listar, atualizar, deletar).
4. Criar `views/` (interface no terminal pra começar).
5. Considerar tabelas adicionais: `categorias`, `fornecedores`, `movimentacoes`.

## Tipos de dados SQLite
| Tipo | Para | Exemplo |
|---|---|---|
| `INTEGER` | números inteiros | 42 |
| `REAL` | decimais | 19.99 |
| `TEXT` | texto | "arroz" |
| `BLOB` | binário (raro) | imagens |

## Dicas que aprendi
- **Sempre usar** `return` na função `conectar()` (esqueci uma vez!).
- `.close()` precisa de parênteses pra executar — sem parênteses, só "olha" o método.
- Convenção: SQL no Python escrito em `"""..."""` (triple string) pra ficar multi-linha.
- Boa prática: uma conexão por operação, não uma conexão "global".
- Underscore `_` antes do nome (ex: `_criar_produtos`) = função "interna" / privada.

## Formas de criar várias tabelas (vistas hoje)
1. Tudo numa função só
2. Uma função por tabela
3. Funções internas `_criar_X(cursor)` + uma `criar_tabelas()` orquestradora
4. Lista de SQLs com loop
5. Dicionário (nome + SQL)
6. Arquivo `.sql` separado + `executescript()`
7. **Classe (POO)** ← escolhi essa

---

*Continuei nessa sessão com o Claude no trabalho. Em casa vou retomar daqui.*
