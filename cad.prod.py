# coding=utf-8
import tkinter as tk
from tkinter import ttk
import crud as crud


class PrincipalBD:
    def __init__(self, win):
        self.objBD = crud.AppBD()
        # componentes
        self.lbCodigo = tk.Label(win, text='Codigo do produto: ')
        self.lblNome = tk.Label(win, text='Nome do produto ')
        self.lblPreco = tk.Label(win, text='Preço ')

        self.txtCodigo = tk.Entry(bd=3)
        self.txtNome = tk.Entry()
        self.txtPreco = tk.Entry()

        self.btnCadastrar = tk.Button(win, text='Cadastrar', command=self.fCadastrarProduto)
        self.btnAtualizar = tk.Button(win, text='Atualizar', command=self.fAtualizarProduto)
        self.btnExcluir = tk.Button(win, text='Excluir', command=self.fExcluirProduto)
        self.btnLimpar = tk.Button(win, text='Limpar', command=self.fLimparTela)

        #componentes da treeview
        self.dadosColunas =("Código", "Nome", "Preço")
        self.treeProdutos = ttk.Treeview(win, columns=self.dadosColunas,
                                         selectmode='browse')
        self.verscrlbar =ttk.Scrollbar(win, orient="vertical",
                                       command=self.treeProdutos.yview())
        self.verscrlbar.pack(side = 'right', fill = 'x')
        self.treeProdutos.configure(yscrollcommand=self.verscrlbar.set)

        self.treeProdutos.heading("Código", text="Código")
        self.treeProdutos.heading("Nome", text="Nome")
        self.treeProdutos.heading("Preço", text="Preço")

        self.treeProdutos.column("Código",minwidth = 0, width=100)
        self.treeProdutos.column("Nome", minwidth=0, width=100)
        self.treeProdutos.column("Preço", minwidth=0, width=100)

        self.treeProdutos.pack(padx=10, pady= 10)
        self.treeProdutos.bind("<< TreeviewSelect >>",
                               self.apresentarRegistrosSelecionados)


        self.lbCodigo.place(x=100, y=50)
        self.txtCodigo.place(x=250, y=50)

        self.lblNome.place(x=100, y=100)
        self.txtNome.place(x=250, y=100)

        self.lblPreco.place(x=100, y=150)
        self.txtPreco.place(x=250, y=150)

        self.btnCadastrar.place(x=100, y=200)
        self.btnAtualizar.place(x=200, y=200)
        self.btnExcluir.place(x=300, y=200)
        self.btnLimpar.place(x=400, y=200)

        self.treeProdutos.place(x=100, y=300)
        self.verscrlbar.place(x=805, y=300, height=225)
        self.carregarDadosIniciais()

    def fLer(self):
        try:
            codigo = int(self.txtCodigo.get())
            print('codigo', codigo)
            nome = self.txtNome.get()
            print('nome', nome)
            preco = float(self.txtPreco.get())
            print('preco', preco)
            print('Leitura dos Dados feita!!')
        except:
            print('Não foi possivel ler os dados.')
            return codigo, nome, preco

    def fLimparTela(self):
        try:
            self.txtCodigo.delete(0, tk.END)
            self.txtNome.delete(0, tk.END)
            self.txtPreco.delete(0, tk.END)
            print("Limpo!")
        except:
            print("Não foi possivel limpar.")

    def fCadastrarProduto(self):
        try:
            codigo, nome, preco = self.fLer()
            self.objBD.inserirDados(codigo, nome, preco)
            self.treeProdutos.insert(' ', 'end',
                                         iid=self.iid,
                                         values=(codigo, nome, preco))
            self.iid=self.iid+1
            self.id = self.id+1
            self.fLimparTela()
            print("Produto cadastrado!")
        except:
            print("Não foi possivel fazer o cadastro.")

    def fAtualizarProduto(self):
        try:
            codigo, nome, preco = self.fLer()
            self.objBD.atualizarDados(codigo, nome, preco)
            self.carregarDadosIniciais()
            self.fLimparTela()
            self.fake()
            print("Produto atualizado!!")
        except:
            print("Não foi possivel atualizar o produto.")

    def fExcluirProduto(self):
        try:
            codigo, nome, preco = self.fLer()
            self.objBD.excluirDados(codigo)
            self.carregarDadosIniciais()
            self.fLimparTela()
            print("Produto excluido!!")
        except:
            print("Não foi possivel excluir o produto")
    def apresentarRegistrosSelecionados(self, event):
        self.fLimparTela()
        for selection in self.treeProdutos.selection():
            item = self.treeProdutos.item(selection)
            codigo, nome, preco = item["values"][0:3]
            self.txtCodigo.insert(0, codigo)
            self.txtNome.insert(0, nome)
            self.txtPreco.insert(0, preco)

# carregar dados iniciais
    def carregarDadosIniciais(self):
        try:
            self.id = 0
            self.iid = 0
            registro = self.objBD.selecionarDados()
            print("Dados disponiveis no BD")
            for item in registro:
                codigo = item[0]
                nome = item[1]
                preco = item[2]
                print("Codigo = ", codigo)
                print("Nome = ", nome)
                print("Preço", preco)

                self.treeProdutos.insert(' ', 'end',
                                            iid=self.iid,
                                            values=(codigo, nome, preco))
                self.iid = self.iid + 1
                self.id = self.id + 1
                print("Dados da base")
        except:
            print("Ainda não existem dados para carregar!")

janela = tk.Tk()
principal = PrincipalBD(janela)
janela.title('Bem vindo(a) a tela de cadastro')
janela.geometry("500x500+20+10")
janela.mainloop()


