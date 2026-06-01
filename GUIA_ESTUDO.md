# Guia de Estudo — Checkpoint 4 (ERP de Estoque)

Guia pra estudar offline e entender cada peça do projeto.
Leia em ordem. Não pule seções — uma depende da outra.

---

## 1. Visão geral

### O que é o projeto

Sistema desktop ERP de gestão de inventário:
- **CRUD** completo de produtos
- **SQLite** persistente
- **GUI** com CustomTkinter (tema escuro)
- **Dashboard** com Matplotlib embutido
- **MVC** em pastas separadas

### Estrutura do projeto

```
checkpoint-4/
├── main.py                          # ponto de entrada (roda o app)
├── config/
│   └── init_banco.py                # classe BancoDados
├── models/
│   └── produto.py                   # classe Produto
├── controller/
│   └── produto_controller.py        # classe ProdutoController
├── views/
│   └── tela.py                      # classe Tela (GUI)
├── README.md
├── .gitignore
└── GUIA_ESTUDO.md
```

### Fluxo MVC (regra de ouro)

```
Tela  →  Controller  →  Model (BancoDados)  →  SQLite
```

- A **Tela** NUNCA acessa SQLite direto
- O **Controller** valida E faz a ponte
- O **Model** só executa SQL
- Nunca pula etapa

---

## 2. POO em Python — fundamentos

### 2.1. Classe vs Objeto

**Classe** = a fôrma, a receita
**Objeto (instância)** = o produto feito a partir da fôrma

```python
class Carro:
    pass

c1 = Carro()       # um objeto
c2 = Carro()       # outro objeto independente
```

`c1` e `c2` são objetos diferentes. Mexer num não afeta o outro.

### 2.2. `__init__` (construtor)

Roda **automaticamente** quando o objeto é criado.

```python
class Carro:
    def __init__(self, cor):
        self.cor = cor

c1 = Carro("vermelho")
print(c1.cor)        # "vermelho"
```

### 2.3. `self`

`self` é a referência ao **próprio objeto**. Sempre é o primeiro parâmetro de todo método.

Quando você escreve `c1.acelerar()`, o Python por baixo chama `Carro.acelerar(c1)`. O `c1` é passado como `self` automaticamente.

```python
class Carro:
    def __init__(self):
        self.velocidade = 0

    def acelerar(self):
        self.velocidade += 10

c1 = Carro()
c1.acelerar()
c1.acelerar()
print(c1.velocidade)   # 20
```

### 2.4. Atributo vs variável local

```python
class Carro:
    def __init__(self):
        self.cor = "azul"     # ATRIBUTO — fica no objeto
        marca = "Toyota"      # VARIÁVEL LOCAL — morre quando __init__ termina
```

Use `self.` quando quiser que a informação seja **acessada por outros métodos** do mesmo objeto.

### 2.5. Método

Função dentro de uma classe. Sempre tem `self` como 1º parâmetro.

```python
class Calculadora:
    def somar(self, a, b):
        return a + b

calc = Calculadora()
print(calc.somar(2, 3))   # 5
```

### 2.6. Construtor com herança (CustomTkinter)

Quando uma classe herda de outra (`class Tela(ctk.CTk):`), o `__init__` da classe pai NÃO roda automaticamente. Você precisa chamar:

```python
class Tela(ctk.CTk):
    def __init__(self):
        super().__init__()       # chama o __init__ de ctk.CTk
        self.title("Meu app")
```

`super()` é o "pai". Sem `super().__init__()`, a janela CustomTkinter não funciona.

---

## 3. Padrões de banco que se repetem

Toda operação no SQLite segue o mesmo esqueleto:

```python
def alguma_operacao(self):
    conexao = self.banco.conectar()
    try:
        with conexao:
            cursor = conexao.cursor()
            cursor.execute("SQL", (parametros,))
            # se for SELECT, faz cursor.fetchall()
    except sqlite3.Error as e:
        print(f"Erro: {e}")
    finally:
        conexao.close()
```

### Por que essa estrutura?

- **`try/finally`** — `finally` SEMPRE roda. Garante que `conexao.close()` execute mesmo se der erro
- **`with conexao:`** — commit automático se tudo deu certo, rollback automático se deu erro
- **`cursor`** — quem executa SQL e lê resultados
- **`?` placeholders** — protegem contra SQL Injection (regra de ouro)
- **`(id,)`** — tupla de 1 elemento PRECISA da vírgula

### Diferença `try/except` vs `try/finally`

- `except` — só roda SE der erro do tipo especificado
- `finally` — SEMPRE roda, com ou sem erro

Usamos os dois juntos: `except` pra capturar e logar erros de SQL, `finally` pra garantir que a conexão fecha.

### `?` placeholder — por quê?

**Vulnerável (NUNCA faça):**
```python
cursor.execute(f"INSERT INTO produtos VALUES ('{nome}', {preco})")
# Se nome for "Arroz'); DROP TABLE produtos; --" → DESASTRE
```

**Seguro (sempre faça):**
```python
cursor.execute(
    "INSERT INTO produtos (nome, preco) VALUES (?, ?)",
    (nome, preco)
)
# O sqlite3 escapa os valores automaticamente
```

---

## 4. `config/init_banco.py` — a fundação

### Responsabilidade
Saber se conectar ao SQLite e criar as tabelas. Não conhece produtos.

### Código atual

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
```

### Detalhes

- **`nome_arquivo="estoque.db"`** — parâmetro com valor padrão. Pode ser sobrescrito: `BancoDados("outro.db")`
- **Últimas 2 linhas** — criam o banco quando o arquivo é importado pela primeira vez. Isso garante que a tabela exista antes do controller usá-la

---

## 5. `models/produto.py` — entidade

### Responsabilidade
Representar UM produto em memória. Não fala com banco.

### Código atual

```python
class Produto:
    def __init__(self, nome, quantidade, preco, id=None):
        self.id = id
        self.nome = nome
        self.quantidade = quantidade
        self.preco = preco

    def __str__(self):
        return f"{self.nome} | Qtd: {self.quantidade} | R$ {self.preco:.2f}"
```

### Detalhes

- **`id=None`** — valor padrão. Quando você cria um Produto "novo" (ainda não salvo), não tem ID. Quando o controller lê do banco, passa o ID
- **`__str__`** — define como `print(produto)` exibe. Sem isso, Python imprime algo tipo `<__main__.Produto object at 0x...>`
- **`{self.preco:.2f}`** — formata o número com 2 casas decimais

---

## 6. `controller/produto_controller.py` — o cérebro

### Responsabilidade
- Validar dados que vêm da tela
- Converter texto para número
- Chamar SQL do banco
- Retornar `(ok, mensagem)` pra tela saber se foi sucesso

### Estrutura geral

A classe tem 9 métodos divididos em 3 grupos:

**CRUD puro** (executa SQL):
- `inserir(produto)`
- `listar_produtos()`
- `atualizar(id, produto)`
- `deletar(id)`

**Validação + ponte** (validam strings, criam Produto, chamam o CRUD):
- `processar_cadastro(nome, qtd, preco)`
- `processar_atualizacao(id, nome, qtd, preco)`
- `processar_exclusao(id)`

A tela chama os métodos `processar_*`. Esses validam, e SE tudo OK, chamam os CRUDs internos.

### Exemplo — `processar_cadastro`

```python
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
```

**Passo a passo:**
1. Se algum campo veio vazio → retorna erro
2. Tenta converter texto pra número. Se falhar (usuário digitou "abc") → retorna erro
3. Se número for negativo → retorna erro
4. Cria objeto `Produto`
5. Chama `self.inserir(produto)` — o método que tem o SQL
6. Retorna sucesso

### Por que retornar tupla `(bool, str)`?

A tela precisa saber:
1. **Se deu certo** (mostrar popup verde) ou erro (popup vermelho)
2. **Qual mensagem** mostrar

Retornar uma tupla resolve as duas coisas em uma chamada:

```python
ok, msg = self.controller.processar_cadastro(...)
if ok:
    messagebox.showinfo("Sucesso", msg)
else:
    messagebox.showerror("Erro", msg)
```

### `try/except ValueError`

`int("abc")` ou `float("abc")` lançam `ValueError`. Sem o `try`, o programa quebra. Com o `try`, a gente captura e retorna mensagem amigável.

---

## 7. `views/tela.py` — a interface

### Responsabilidade
- Desenhar a janela
- Pegar input do usuário
- Chamar o controller
- Mostrar resultados (popup, listagem, gráfico)

### CustomTkinter — conceitos

**Janela principal** — herda de `ctk.CTk`:
```python
class Tela(ctk.CTk):
    def __init__(self):
        super().__init__()       # OBRIGATÓRIO
        self.title("Meu app")
        self.geometry("1000x600")
```

**Widgets** — botões, campos, labels, frames:
```python
botao = ctk.CTkButton(self, text="Clica", command=self.minha_funcao)
campo = ctk.CTkEntry(self, placeholder_text="Digite aqui")
label = ctk.CTkLabel(self, text="Texto")
frame = ctk.CTkFrame(self)        # container
```

**Layouts** — `pack` (empilha) ou `grid` (linhas/colunas):
```python
botao.pack(pady=10)                      # empilha
botao.grid(row=0, column=0)              # tabela
```

**Pegar / setar valor de Entry:**
```python
texto = campo.get()                      # lê
campo.delete(0, "end")                   # limpa
```

**Mostrar popups:**
```python
from tkinter import messagebox
messagebox.showinfo("Título", "Mensagem")
messagebox.showerror("Título", "Erro")
messagebox.showwarning("Título", "Aviso")
```

**Iniciar a janela:**
```python
if __name__ == "__main__":
    app = Tela()
    app.mainloop()       # mantém a janela aberta esperando interação
```

### Layout do projeto

```
┌──────────────────────────────────────────────────────┐
│  TELA PRINCIPAL                                       │
│  ┌──────────────┐  ┌──────────────────────────────┐  │
│  │ FORMULÁRIO   │  │  LISTAGEM (textbox)          │  │
│  │              │  │                              │  │
│  │ [ID]         │  │  ID  NOME      QTD  PREÇO    │  │
│  │ [Nome]       │  │  1   Arroz     42   28.90    │  │
│  │ [Qtd]        │  │  2   Feijão    30   8.50     │  │
│  │ [Preço]      │  │                              │  │
│  │              │  ├──────────────────────────────┤  │
│  │ [Gravar]     │  │  GRÁFICO (Matplotlib)        │  │
│  │ [Atualizar]  │  │                              │  │
│  │ [Excluir]    │  │  ▓ ▓ ▓                       │  │
│  │ [Limpar]     │  │  ▓ ▓ ▓                       │  │
│  │ [Gráfico]    │  │  ▓ ▓ ▓                       │  │
│  └──────────────┘  └──────────────────────────────┘  │
└──────────────────────────────────────────────────────┘
```

- Coluna 0 (formulário): largura fixa
- Coluna 1 (lista + gráfico): expande quando a janela cresce
- Painel direito é dividido em 2 linhas: textbox em cima, frame do gráfico embaixo

### Matplotlib embutido

A "cola mágica" pra colocar gráfico Matplotlib dentro do CustomTkinter:

```python
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

fig = Figure(figsize=(5, 3), dpi=100)
ax = fig.add_subplot(111)
ax.bar(["A", "B", "C"], [10, 20, 15])

canvas = FigureCanvasTkAgg(fig, master=meu_frame)
canvas.draw()
canvas.get_tk_widget().pack(fill="both", expand=True)
```

- `Figure` — a figura do Matplotlib (não usar `plt.figure()` que é GUI-própria)
- `FigureCanvasTkAgg` — converte a figura em widget Tkinter
- `master=meu_frame` — onde a figura vai morar

### Por que destruir o canvas antes de plotar de novo

```python
if self.canvas_grafico is not None:
    self.canvas_grafico.get_tk_widget().destroy()
```

Sem isso, cada clique em "Gerar Gráfico" EMPILHA um novo canvas. Em 5 cliques, 5 gráficos na tela.

Com isso, o antigo é destruído antes do novo aparecer.

---

## 8. `main.py` — ponto de entrada

```python
from views.tela import Tela


if __name__ == "__main__":
    app = Tela()
    app.mainloop()
```

**Por que tão curto?** Porque o `main.py` só DEVE iniciar o app. Toda a lógica está nos arquivos certos do MVC.

**Por que `if __name__ == "__main__":`?** Pra que esse bloco só rode quando você executa `python main.py` direto. Se outro arquivo importar `main.py`, não dispara.

---

## 9. Como rodar

```bash
# Da raiz do checkpoint-4
cd /caminho/para/checkpoint-4

# Primeira vez — criar venv e instalar
python3 -m venv .venv
source .venv/bin/activate
pip install customtkinter matplotlib pyinstaller

# Mac com Python do Homebrew (se _tkinter faltar):
brew install python-tk@3.14    # ajustar versão

# Rodar
python main.py
```

---

## 10. Gerar `.exe` (Fase 5)

**SÓ FUNCIONA NO WINDOWS.** No Mac gera binário Mac, não `.exe`.

### Passo a passo

```bash
cd checkpoint-4
pyinstaller --onefile --windowed --icon=icone.ico main.py
```

- `--onefile` — gera UM `.exe` único
- `--windowed` — não abre console preto junto
- `--icon=icone.ico` — opcional

O `.exe` fica em `dist/main.exe`.

### Problemas comuns

| Sintoma | Causa | Solução |
|---|---|---|
| Falha "module not found" | Rodou pyinstaller no Python errado | Usar o do venv: `.venv\Scripts\pyinstaller.exe` |
| `.exe` abre e fecha | Erro silencioso | Rodar sem `--windowed` pra ver erro |
| `.exe` muito grande (~100MB) | Matplotlib + Tkinter pesam | Normal |
| Banco não aparece | `.exe` cria `estoque.db` na pasta onde foi executado | Esperado |

---

## 11. Roteiro pra apresentação

### Sugestão de 5-10 min

**1. Contextualizar (30s)**
> "ERP de gestão de estoque com CRUD completo, banco SQLite, GUI moderna em CustomTkinter e dashboard com Matplotlib."

**2. Mostrar a estrutura MVC (1-2 min)**
> "Segui o padrão MVC em pastas separadas. `config/` tem a classe de conexão. `models/` tem a entidade Produto. `controller/` faz validação e ponte. `views/` tem a tela. `main.py` na raiz inicia tudo."

**3. Percorrer cada arquivo (3-4 min)**

- **`config/init_banco.py`** — "Classe BancoDados. Tem `conectar()` e `criar_tabelas()` com `CREATE TABLE IF NOT EXISTS`. Usa `try/finally` pra garantir que a conexão fecha."

- **`models/produto.py`** — "Classe Produto, entidade simples. ID é opcional pra produtos ainda não salvos."

- **`controller/produto_controller.py`** — "Faz duas coisas: tem os métodos de CRUD que executam SQL, e tem os métodos `processar_*` que validam antes de chamar o CRUD. Toda função SQL usa placeholders `?` pra evitar SQL Injection."

- **`views/tela.py`** — "Classe Tela herda de `ctk.CTk`. Layout em grid: formulário à esquerda, lista e gráfico à direita. Cada botão chama um método `processar_*` do controller e mostra popup conforme o resultado."

**4. Demo (2-3 min)**
- Cadastra 3 produtos
- Atualiza um (mostra que precisa do ID)
- Exclui um
- Gera gráfico
- Fecha e abre de novo → dados persistem no SQLite

**5. Detalhes técnicos que valem ponto (1 min)**
- "Placeholders `?` em todo SQL contra SQL Injection"
- "`try/except ValueError` na conversão pra número"
- "View nunca importa sqlite3 — fluxo é Tela → Controller → Model → SQLite"
- "Limpo os campos depois de cada operação (UX)"
- "Tema escuro com CustomTkinter"

### Perguntas comuns

**"Por que classes em vez de funções soltas?"**
> "Pra praticar POO e porque o código fica mais organizado conforme cresce. Classes encapsulam estado e comportamento."

**"O que é `self`?"**
> "Referência ao próprio objeto. Quando chamo `obj.metodo()`, Python passa `obj` como `self` automaticamente."

**"Por que `try/finally` em vez de só `try/except`?"**
> "`finally` SEMPRE roda. Garante que `conexao.close()` execute mesmo se algo quebrar no meio."

**"O que `with conexao` faz?"**
> "Commit automático se tudo deu certo, rollback se deu erro. É o context manager da conexão SQLite."

**"O que é MVC?"**
> "Padrão de separação: Model (dados/banco), View (interface), Controller (lógica/validação). Cada um tem uma responsabilidade — facilita manutenção e teste."

---

## 12. Checklist final

- [ ] `config/init_banco.py` cria a tabela produtos
- [ ] `models/produto.py` tem a classe Produto com `__str__`
- [ ] `controller/produto_controller.py` tem CRUD + métodos `processar_*`
- [ ] `views/tela.py` GUI funcionando: cadastra, lista, atualiza, exclui, gráfico
- [ ] `main.py` na raiz inicia o app
- [ ] Banco `estoque.db` persiste entre execuções (fecha e abre, dados ficam)
- [ ] Campos limpam depois de salvar
- [ ] Validação de campo vazio mostra popup vermelho
- [ ] Validação de "abc" no preço mostra popup vermelho
- [ ] Tema escuro aplicado
- [ ] Gráfico de barras gera corretamente
- [ ] `.gitignore` na raiz
- [ ] `README.md` com nome no topo
- [ ] (Opcional) `.exe` gerado no Windows
- [ ] Repositório no GitHub com colega adicionado como colaborador
- [ ] Link na planilha de entregas

---

## 13. Erros comuns e soluções

| Erro | Significa | Solução |
|---|---|---|
| `ModuleNotFoundError: No module named 'customtkinter'` | Não instalou ou rodando Python errado | Ativar venv e instalar |
| `No module named '_tkinter'` (Mac) | Python sem suporte Tk | `brew install python-tk@3.14` |
| `'NoneType' object has no attribute 'cursor'` | `conectar()` sem `return` | Adicionar `return` |
| `no such table: produtos` | Tabela não foi criada | Garantir que `init_banco.py` foi importado (cria a tabela ao importar) |
| `near "?": syntax error` | Número de `?` ≠ número de valores | Conferir tuple |
| `not enough values to unpack` | SELECT retorna menos colunas que esperado | Conferir SELECT |
| `ValueError: could not convert string to float` | Usuário digitou texto em campo numérico | Já tratado com `try/except` |
| Janela abre e fecha imediatamente | Falta `app.mainloop()` | Adicionar no `__main__` |

---

## 14. Resumo 1 página

**Estrutura MVC:**
```
main.py
config/init_banco.py      → class BancoDados
models/produto.py         → class Produto
controller/produto_controller.py → class ProdutoController
views/tela.py             → class Tela (ctk.CTk)
```

**Fluxo:** Tela → Controller → BancoDados → SQLite

**POO:** class, `__init__(self)`, `self.atributo`, métodos com `self`, `super().__init__()` em herança.

**SQL seguro:** sempre `?` placeholder, tupla `(valor,)` com vírgula.

**Padrão BD:**
```python
conexao = self.banco.conectar()
try:
    with conexao:
        cursor = conexao.cursor()
        cursor.execute(...)
except sqlite3.Error as e:
    print(...)
finally:
    conexao.close()
```

**Controller retorna `(ok, msg)`** — tupla pra tela saber se sucesso/erro.

**GUI:** herda `ctk.CTk`, `super().__init__()`, widgets com `grid()/pack()`, botão com `command=funcao`.

**Matplotlib:** `Figure() → ax.bar() → FigureCanvasTkAgg(fig, master=frame) → canvas.get_tk_widget().pack()`.

**.exe (Windows):** `pyinstaller --onefile --windowed main.py`.

Bora apresentar! 🚀
