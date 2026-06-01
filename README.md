# ERP — Sistema de Gestão de Estoque

> Checkpoint 4 — Desktop ERP com Python + SQLite + CustomTkinter + Matplotlib

**Autor:** Ernani Silva

---

## Sobre o projeto

Sistema desktop de gestão de inventário com CRUD completo, banco de dados persistente e dashboard de visualização. Construído seguindo o padrão de arquitetura MVC em pastas separadas.

### Funcionalidades

- Cadastro, listagem, atualização e exclusão de produtos (CRUD)
- Persistência em banco SQLite
- Interface gráfica moderna com tema escuro (CustomTkinter)
- Dashboard com gráfico de barras embutido (Matplotlib)
- Validações de campos e tratamento de erros
- Proteção contra SQL Injection (uso de placeholders `?`)

---

## Estrutura

```
checkpoint-4/
├── main.py                    # ponto de entrada
├── config/
│   └── init_banco.py          # classe BancoDados (conexão + tabelas)
├── models/
│   └── produto.py             # classe Produto (entidade)
├── controller/
│   └── produto_controller.py  # classe ProdutoController (validação + CRUD)
├── views/
│   └── tela.py                # classe Tela (GUI CustomTkinter + gráfico)
├── ANOTACOES.md               # notas de estudo
├── GUIA_ESTUDO.md             # guia completo do projeto
├── .gitignore
└── README.md
```

### Fluxo MVC

```
Tela (views)  →  Controller  →  Model + BancoDados  →  SQLite
```

A tela nunca acessa o SQLite diretamente. Toda comunicação passa pelo controller.

---

## Como rodar (Windows)

### Pré-requisitos

- **Python 3.10+** instalado com a opção **"Add Python to PATH"** marcada na instalação
- Confira no terminal:
  ```cmd
  python --version
  ```

### Instalação

```cmd
:: Clonar repositório
git clone <url-do-repo>
cd checkpoint-4

:: Criar ambiente virtual
python -m venv .venv

:: Ativar venv (Windows)
.venv\Scripts\activate

:: Instalar dependências
pip install customtkinter matplotlib pyinstaller
```

Após ativar o venv, o terminal deve mostrar `(.venv)` no início da linha.

### Executar

```cmd
python main.py
```

A janela vai abrir e o banco `estoque.db` será criado automaticamente na primeira execução.

---

## Como usar a aplicação

### Cadastrar produto
1. Deixe o campo **ID** vazio
2. Preencha **Nome**, **Quantidade** e **Preço**
3. Clique em **Gravar Produto**

### Atualizar produto
1. Copie o **ID** do produto da lista para o campo ID
2. Edite os campos
3. Clique em **Atualizar**

### Excluir produto
1. Copie o **ID** do produto da lista para o campo ID
2. Clique em **Excluir**

### Visualizar gráfico
- Clique em **Gerar Gráfico** — exibe gráfico de barras com quantidade em estoque por produto

---

## Gerar executável (.exe) — Windows

Com o venv ativo, dentro da pasta `checkpoint-4`:

```cmd
pyinstaller --onefile --windowed main.py
```

Com ícone customizado (opcional — coloque um `icone.ico` na pasta antes):

```cmd
pyinstaller --onefile --windowed --icon=icone.ico main.py
```

**Flags:**
- `--onefile` — gera um único `.exe`
- `--windowed` — sem console preto aparecendo junto
- `--icon=` — define o ícone do executável

O executável final fica em `dist\main.exe`. Pode copiar pra Área de Trabalho e rodar com clique duplo.

### Distribuição do executável

O `.exe` NÃO é versionado no repositório (limite do GitHub: 100MB por arquivo, e binários incham o histórico do Git). Para disponibilizá-lo:

1. No GitHub, acesse a aba **Releases** do repositório
2. Clique em **"Create a new release"**
3. Crie uma tag (ex: `v1.0`) e adicione título/descrição
4. Anexe o `main.exe` em **"Attach binaries"**
5. Publique a release

Releases é a forma padrão do GitHub para distribuir binários compilados.

---

## Conceitos aplicados

- **POO**: classes (`BancoDados`, `Produto`, `ProdutoController`, `Tela`), atributos com `self`, métodos
- **MVC**: separação clara entre Model, View e Controller em pastas
- **SQLite**: `sqlite3.connect`, `cursor.execute`, placeholders `?`, `try/finally` pra fechar conexão
- **Gerenciador de contexto**: `with conexao` para commit/rollback automático
- **Tratamento de erros**: `try/except` em conversões e operações de banco
- **GUI moderna**: CustomTkinter com tema escuro, frames, grid layout
- **Matplotlib embutido**: integração via `FigureCanvasTkAgg`

---

## Stack

- [Python 3](https://www.python.org/)
- [SQLite](https://www.sqlite.org/)
- [CustomTkinter](https://customtkinter.tomschimansky.com/)
- [Matplotlib](https://matplotlib.org/)
- [PyInstaller](https://pyinstaller.org/)
