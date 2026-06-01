# Roteiro de Apresentação — Checkpoint 4

Lê em voz natural. Pausa onde tem "// PAUSA". Os títulos em **negrito** são pra você se localizar — não precisa falar.

---

## 1. ABERTURA — 30 segundos

Boa tarde. Apresento meu Checkpoint 4: um Sistema de Gestão de Estoque, ou ERP, desenvolvido em Python.

O projeto é uma aplicação desktop com interface gráfica que permite cadastrar, listar, atualizar e excluir produtos. Tudo é persistido em um banco SQLite, e há um dashboard com gráfico de barras pra visualizar o estoque.

A arquitetura segue o padrão MVC — Model, View, Controller — com cada camada em sua própria pasta.

// PAUSA

---

## 2. ESTRUTURA DO PROJETO — 1 minuto

Antes de entrar no código, deixa eu mostrar a estrutura. // (abre o explorador do VS Code)

- Na raiz tenho o `main.py`, que é só o ponto de entrada da aplicação.
- A pasta `config` tem a configuração e a classe de conexão com o banco de dados.
- A pasta `models` tem a entidade Produto.
- A pasta `controller` tem a lógica de negócio e validações.
- A pasta `views` tem a interface gráfica em CustomTkinter.
- Tem também o `README.md`, `.gitignore` e um guia de estudo.

O fluxo é: a tela conversa com o controller, o controller conversa com o banco. A tela nunca acessa o SQLite diretamente. É a regra de ouro do MVC.

// PAUSA

---

## 3. CONFIG / INIT_BANCO — 1 minuto

// (abre config/init_banco.py)

Aqui temos a configuração do banco. Definimos a classe `BancoDados`, que é responsável por iniciar e gerenciar o SQLite, no arquivo `estoque.db`.

No construtor `__init__`, defino o atributo `self.nome_arquivo` que guarda o nome do banco. Coloquei como parâmetro com valor padrão, então a classe é reutilizável.

A classe tem dois métodos:

O `conectar` retorna uma conexão SQLite. Opto por abrir e fechar uma conexão por operação, em vez de manter uma conexão longa — é o padrão recomendado em SQLite.

O `criar_tabelas` executa o `CREATE TABLE IF NOT EXISTS produtos`. Esse "IF NOT EXISTS" garante idempotência: posso chamar a função várias vezes sem dar erro.

Aqui no final do arquivo, eu instancio a classe e chamo o `criar_tabelas` — assim, quando esse arquivo for importado, o banco já estará pronto.

// PAUSA

---

## 4. MODELS / PRODUTO — 45 segundos

// (abre models/produto.py)

Aqui está a entidade Produto — o "M" do MVC. É a representação em memória de um item do estoque.

A classe tem quatro atributos: id, nome, quantidade e preço. Defini o id como opcional, com valor padrão None, porque quando crio um produto novo ele ainda não tem ID — quem gera é o SQLite via AUTOINCREMENT. Mas quando leio um produto do banco, eu passo o ID que veio do SELECT.

Também sobrescrevi o método `__str__`, que define como o objeto vira texto. Quando faço `print(produto)`, em vez de aparecer aquela representação padrão do Python com endereço de memória, aparece nome, quantidade e preço formatado.

// PAUSA

---

## 5. CONTROLLER — 2 minutos

// (abre controller/produto_controller.py)

Esse é o cérebro do sistema. A classe `ProdutoController` faz a ponte entre a tela e o banco.

No construtor, eu instancio a classe `BancoDados` e guardo no atributo `self.banco`. Assim todos os métodos da classe têm acesso ao banco.

Os métodos estão divididos em dois grupos:

O primeiro grupo é o CRUD — `inserir`, `listar_produtos`, `atualizar` e `deletar`. Cada um abre uma conexão, executa o SQL e fecha no `finally`. Uso `try` e `finally` pra garantir que a conexão fecha mesmo se der erro, e o `with conexao` pra ter commit automático em caso de sucesso ou rollback em caso de erro.

Importante destacar: todo SQL usa placeholders com interrogação. Isso é a regra de ouro pra evitar SQL Injection. O driver do SQLite escapa os valores automaticamente.

O segundo grupo são os métodos de validação: `processar_cadastro`, `processar_atualizacao` e `processar_exclusao`. Esses são os métodos chamados pela tela. Eles validam três coisas: se os campos estão vazios, se a conversão de texto pra número funciona — usando try-except ValueError — e se os valores não são negativos.

Em caso de erro, retornam uma tupla com False e a mensagem. Em caso de sucesso, instanciam um Produto, chamam o método CRUD interno, e retornam True com mensagem de sucesso.

// PAUSA

---

## 6. VIEWS / TELA — 2 minutos

// (abre views/tela.py)

Aqui está a interface gráfica em CustomTkinter.

A classe `Tela` herda de `ctk.CTk` — ou seja, ela JÁ é uma janela do CustomTkinter, por herança.

No construtor, chamo `super().__init__()` pra inicializar a janela base, defino título e tamanho, e crio uma instância do controller que guardo em `self.controller`.

Uso layout em grid pra dividir a janela em duas colunas. A coluna da esquerda tem peso zero — tamanho fixo. A da direita tem peso um — expande quando a janela cresce.

Dentro do painel da esquerda, monto o formulário: campos CTkEntry pra ID, Nome, Quantidade e Preço, e botões CTkButton pra Gravar, Atualizar, Excluir, Limpar e Gerar Gráfico. Cada botão usa o parâmetro `command` pra apontar pro método correspondente.

No painel da direita, em cima tem uma CTkTextbox que mostra a lista de produtos, e embaixo um frame onde o gráfico do Matplotlib é renderizado.

Os métodos `gravar`, `atualizar`, `excluir` seguem todos o mesmo padrão: leio os campos com `.get()`, mando pro controller via `processar_*`, recebo a tupla com sucesso e mensagem, e mostro um messagebox de info ou erro. Em caso de sucesso, limpo os campos com `.delete` e recarrego a lista.

Pro dashboard, busco os produtos pelo controller, separo em duas listas — nomes e quantidades — crio uma Figure do Matplotlib com `ax.bar`, e uso o `FigureCanvasTkAgg` que é a ponte entre Matplotlib e Tkinter. Ele converte a figura num widget que eu posso empacotar no frame normalmente.

// PAUSA

---

## 7. MAIN — 20 segundos

// (abre main.py)

O `main.py` é só o ponto de entrada. Importa a classe Tela, instancia, e chama o `mainloop` — que é o loop de eventos do Tkinter, fica processando eventos até o usuário fechar a janela.

O `if __name__ == "__main__"` garante que isso só executa quando o arquivo é rodado direto, não quando importado.

// PAUSA

---

## 8. DEMO AO VIVO — 3 minutos

Agora vou rodar a aplicação. // (executa python main.py)

A janela abre e o banco `estoque.db` é criado automaticamente.

Primeiro vou cadastrar três produtos. // (cadastra Arroz, Feijão, Macarrão)

Note que após salvar, os campos limpam automaticamente — é UX. E a lista atualiza em tempo real.

Agora vou demonstrar as validações. // (deixa campo vazio, clica Gravar) — aparece o popup vermelho "Campos vazios".

E se eu digitar texto inválido no preço — // (digita "abc" no preço, clica Gravar) — outro popup vermelho: "Erro nos números".

Pra atualizar, copio o ID do produto da lista. // (digita 1 no ID, muda os campos, clica Atualizar) — popup verde de sucesso, e a lista atualiza.

Pra excluir, mesmo princípio — // (coloca ID, clica Excluir).

Agora o dashboard: // (clica Gerar Gráfico) — aparece o gráfico de barras mostrando a quantidade em estoque de cada produto.

E pra provar a persistência, vou fechar a aplicação e reabrir. // (fecha, reabre) — os dados continuam lá. O banco SQLite persistiu tudo.

// PAUSA

---

## 9. FECHAMENTO — 30 segundos

Resumindo as decisões arquiteturais do projeto:

- Separação estrita de camadas, seguindo o padrão MVC
- Prepared statements em todo SQL pra prevenir SQL Injection
- Try-finally pra garantir liberação de recursos
- Validação centralizada no controller, deixando a view burra e o model anêmico
- Tratamento de erros explícito via tupla de retorno, em vez de exceções propagadas

Todo o código está versionado em repositório privado no GitHub, com `.gitignore` configurado e README completo.

Obrigado pela atenção.

---

## EXTRAS — Perguntas que podem cair e respostas curtas

**"O que é POO?"**
> Programação Orientada a Objetos. É um paradigma onde organizo o código em classes, que são moldes pra criar objetos. Cada objeto encapsula dados — atributos — e comportamentos — métodos.

**"O que é `self`?"**
> Referência ao próprio objeto. Quando chamo `obj.metodo()`, o Python passa `obj` como `self` automaticamente. Permite que o método acesse os atributos do objeto.

**"O que é MVC?"**
> Padrão arquitetural que separa o sistema em três camadas: Model — dados e banco; View — interface; Controller — lógica e validação. Cada uma tem uma responsabilidade só, o que facilita manutenção.

**"Por que `try/finally` em vez de só `try/except`?"**
> O `finally` SEMPRE roda, com erro ou sem. Garante que a conexão fecha mesmo se algo quebrar no meio.

**"O que `with conexao` faz?"**
> É o context manager da conexão SQLite. Faz commit automático se tudo deu certo, ou rollback se deu erro.

**"Por que usou classes em vez de funções soltas?"**
> Pra praticar POO e porque classes encapsulam estado e comportamento, o que torna o código mais robusto e fácil de manter conforme o projeto cresce.

**"Por que o id é opcional?"**
> Porque quando crio um produto novo ele ainda não tem ID — quem gera é o SQLite via AUTOINCREMENT. Mas quando leio do banco, preciso carregar o ID dentro do objeto pra poder atualizar e excluir depois.

**"O que é AUTOINCREMENT?"**
> É um modificador do SQLite que faz com que IDs nunca sejam reutilizados, mesmo após exclusão. Garante integridade referencial e auditabilidade.

**"Por que o `.exe` não está no repositório?"**
> Não versionei o binário porque ele excede o limite de 100MB do GitHub por arquivo, e binários incham o histórico do Git. A forma correta de distribuir é via GitHub Releases.

**"Como o Matplotlib aparece dentro do Tkinter?"**
> Uso o `FigureCanvasTkAgg`, que é um backend do Matplotlib. Ele converte uma Figure em um widget Tk legítimo, que eu posso empacotar no frame normalmente.

**"O que é herança?"**
> Quando uma classe herda métodos e atributos de outra. Minha classe Tela herda de `ctk.CTk`, então ela JÁ é uma janela — não preciso criar do zero.

**"O que `super().__init__()` faz?"**
> Chama o construtor da classe pai. É necessário porque é a `ctk.CTk` que inicializa todo o subsistema gráfico. Sem essa chamada, a janela não funciona.

---

## CHECKLIST ANTES DE GRAVAR

- [ ] App rodando: `python main.py` abre a janela
- [ ] Banco `estoque.db` apagado pra demo limpa
- [ ] VS Code com a estrutura visível na esquerda
- [ ] Bloco de notas com esse roteiro na segunda tela
- [ ] Áudio testado, microfone OK
- [ ] Resolução de tela: 1080p ou superior
- [ ] Aplicações desnecessárias fechadas
- [ ] Notificações silenciadas
