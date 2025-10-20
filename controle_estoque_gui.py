import tkinter as tk
from tkinter import messagebox

# Funções de interface gráfica para adicionar produtos e registrar entradas
def adicionar_produto_gui():
    nome = entry_nome.get()
    descricao = entry_descricao.get()
    preco = float(entry_preco.get())
    quantidade = int(entry_quantidade.get())
    adicionar_produto(nome, descricao, preco, quantidade)
    messagebox.showinfo("Sucesso", f"Produto {nome} adicionado ao estoque!")

def registrar_entrada_gui():
    produto_id = int(entry_produto_id.get())
    quantidade = int(entry_quantidade_entrada.get())
    registrar_entrada(produto_id, quantidade)
    messagebox.showinfo("Sucesso", f"Entrada registrada para o produto ID {produto_id}.")

def registrar_saida_gui():
    produto_id = int(entry_produto_id_saida.get())
    quantidade = int(entry_quantidade_saida.get())
    registrar_saida(produto_id, quantidade)
    messagebox.showinfo("Sucesso", f"Saída registrada para o produto ID {produto_id}.")

def consultar_estoque_gui():
    cursor.execute('SELECT * FROM produtos')
    produtos = cursor.fetchall()
    estoque_text.delete(1.0, tk.END)
    for produto in produtos:
        estoque_text.insert(tk.END, f'{produto[1]} (ID: {produto[0]}) - {produto[4]} unidades disponíveis.\n')

# Criando a janela principal
root = tk.Tk()
root.title("Controle de Estoque")

# Adicionando os campos para a interface
label_nome = tk.Label(root, text="Nome do Produto:")
label_nome.grid(row=0, column=0)
entry_nome = tk.Entry(root)
entry_nome.grid(row=0, column=1)

label_descricao = tk.Label(root, text="Descrição:")
label_descricao.grid(row=1, column=0)
entry_descricao = tk.Entry(root)
entry_descricao.grid(row=1, column=1)

label_preco = tk.Label(root, text="Preço:")
label_preco.grid(row=2, column=0)
entry_preco = tk.Entry(root)
entry_preco.grid(row=2, column=1)

label_quantidade = tk.Label(root, text="Quantidade:")
label_quantidade.grid(row=3, column=0)
entry_quantidade = tk.Entry(root)
entry_quantidade.grid(row=3, column=1)

btn_adicionar = tk.Button(root, text="Adicionar Produto", command=adicionar_produto_gui)
btn_adicionar.grid(row=4, column=0, columnspan=2)

# Campos para registrar entradas
label_produto_id = tk.Label(root, text="ID do Produto:")
label_produto_id.grid(row=5, column=0)
entry_produto_id = tk.Entry(root)
entry_produto_id.grid(row=5, column=1)

label_quantidade_entrada = tk.Label(root, text="Quantidade de Entrada:")
label_quantidade_entrada.grid(row=6, column=0)
entry_quantidade_entrada = tk.Entry(root)
entry_quantidade_entrada.grid(row=6, column=1)

btn_entrada = tk.Button(root, text="Registrar Entrada", command=registrar_entrada_gui)
btn_entrada.grid(row=7, column=0, columnspan=2)

# Campos para registrar saídas
label_produto_id_saida = tk.Label(root, text="ID do Produto (Saída):")
label_produto_id_saida.grid(row=8, column=0)
entry_produto_id_saida = tk.Entry(root)
entry_produto_id_saida.grid(row=8, column=1)

label_quantidade_saida = tk.Label(root, text="Quantidade de Saída:")
label_quantidade_saida.grid(row=9, column=0)
entry_quantidade_saida = tk.Entry(root)
entry_quantidade_saida.grid(row=9, column=1)

btn_saida = tk.Button(root, text="Registrar Saída", command=registrar_saida_gui)
btn_saida.grid(row=10, column=0, columnspan=2)

# Campo para consultar estoque
btn_estoque = tk.Button(root, text="Consultar Estoque", command=consultar_estoque_gui)
btn_estoque.grid(row=11, column=0, columnspan=2)

estoque_text = tk.Text(root, height=10, width=50)
estoque_text.grid(row=12, column=0, columnspan=2)

root.mainloop()