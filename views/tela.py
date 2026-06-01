import customtkinter as ctk
from tkinter import messagebox
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

from controller.produto_controller import ProdutoController


ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")


class Tela(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.controller = ProdutoController()

        self.title("ERP - Sistema de Gestão de Estoque")
        self.geometry("1000x600")

        self.grid_columnconfigure(0, weight=0)
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)

        self._montar_formulario()
        self._montar_painel_direito()

        self.atualizar_lista()

    def _montar_formulario(self):
        frame = ctk.CTkFrame(self, width=300)
        frame.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")

        titulo = ctk.CTkLabel(
            frame,
            text="Cadastro de Produto",
            font=("Arial", 18, "bold"),
        )
        titulo.pack(pady=15)

        self.entry_id = ctk.CTkEntry(frame, placeholder_text="ID (atualizar/excluir)")
        self.entry_id.pack(pady=5, padx=20, fill="x")

        self.entry_nome = ctk.CTkEntry(frame, placeholder_text="Nome do produto")
        self.entry_nome.pack(pady=5, padx=20, fill="x")

        self.entry_qtd = ctk.CTkEntry(frame, placeholder_text="Quantidade")
        self.entry_qtd.pack(pady=5, padx=20, fill="x")

        self.entry_preco = ctk.CTkEntry(frame, placeholder_text="Preço (ex: 19.90)")
        self.entry_preco.pack(pady=5, padx=20, fill="x")

        ctk.CTkButton(
            frame, text="Gravar Produto", command=self.gravar
        ).pack(pady=8, padx=20, fill="x")

        ctk.CTkButton(
            frame, text="Atualizar", command=self.atualizar
        ).pack(pady=8, padx=20, fill="x")

        ctk.CTkButton(
            frame,
            text="Excluir",
            fg_color="#a83232",
            hover_color="#7a2424",
            command=self.excluir,
        ).pack(pady=8, padx=20, fill="x")

        ctk.CTkButton(
            frame,
            text="Limpar Campos",
            fg_color="gray",
            command=self.limpar_campos,
        ).pack(pady=8, padx=20, fill="x")

        ctk.CTkButton(
            frame, text="Gerar Gráfico", command=self.gerar_grafico
        ).pack(pady=20, padx=20, fill="x")

    def _montar_painel_direito(self):
        painel = ctk.CTkFrame(self)
        painel.grid(row=0, column=1, padx=10, pady=10, sticky="nsew")
        painel.grid_columnconfigure(0, weight=1)
        painel.grid_rowconfigure(0, weight=1)
        painel.grid_rowconfigure(1, weight=1)

        self.textbox = ctk.CTkTextbox(painel, font=("Courier", 13))
        self.textbox.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")

        self.frame_grafico = ctk.CTkFrame(painel)
        self.frame_grafico.grid(row=1, column=0, padx=10, pady=10, sticky="nsew")
        self.canvas_grafico = None

    def limpar_campos(self):
        self.entry_id.delete(0, "end")
        self.entry_nome.delete(0, "end")
        self.entry_qtd.delete(0, "end")
        self.entry_preco.delete(0, "end")

    def gravar(self):
        ok, msg = self.controller.processar_cadastro(
            self.entry_nome.get(),
            self.entry_qtd.get(),
            self.entry_preco.get(),
        )
        if ok:
            messagebox.showinfo("Sucesso", msg)
            self.limpar_campos()
            self.atualizar_lista()
        else:
            messagebox.showerror("Erro", msg)

    def atualizar(self):
        ok, msg = self.controller.processar_atualizacao(
            self.entry_id.get(),
            self.entry_nome.get(),
            self.entry_qtd.get(),
            self.entry_preco.get(),
        )
        if ok:
            messagebox.showinfo("Sucesso", msg)
            self.limpar_campos()
            self.atualizar_lista()
        else:
            messagebox.showerror("Erro", msg)

    def excluir(self):
        ok, msg = self.controller.processar_exclusao(self.entry_id.get())
        if ok:
            messagebox.showinfo("Sucesso", msg)
            self.limpar_campos()
            self.atualizar_lista()
        else:
            messagebox.showerror("Erro", msg)

    def atualizar_lista(self):
        produtos = self.controller.listar_produtos()
        self.textbox.delete("1.0", "end")
        self.textbox.insert("end", f"{'ID':<5}{'NOME':<30}{'QTD':>8}{'PREÇO':>10}\n")
        self.textbox.insert("end", "-" * 55 + "\n")
        for p in produtos:
            self.textbox.insert(
                "end",
                f"{p.id:<5}{p.nome:<30}{p.quantidade:>8}{p.preco:>10.2f}\n",
            )

    def gerar_grafico(self):
        produtos = self.controller.listar_produtos()

        if not produtos:
            messagebox.showwarning("Aviso", "Sem produtos para plotar.")
            return

        nomes = [p.nome for p in produtos]
        quantidades = [p.quantidade for p in produtos]

        if self.canvas_grafico is not None:
            self.canvas_grafico.get_tk_widget().destroy()

        fig = Figure(figsize=(5, 3), dpi=100)
        ax = fig.add_subplot(111)
        ax.bar(nomes, quantidades, color="#1f77b4")
        ax.set_title("Quantidade em Estoque por Produto")
        ax.set_ylabel("Quantidade")
        fig.autofmt_xdate(rotation=30)
        fig.tight_layout()

        self.canvas_grafico = FigureCanvasTkAgg(fig, master=self.frame_grafico)
        self.canvas_grafico.draw()
        self.canvas_grafico.get_tk_widget().pack(fill="both", expand=True)
