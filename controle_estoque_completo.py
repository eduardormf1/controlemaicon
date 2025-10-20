import sqlite3
import shutil
import tkinter as tk
from tkinter import messagebox
from tkinter import font as tkfont

# Criação do Banco de Dados e Tabelas
conn = sqlite3.connect('estoque.db')
cursor = conn.cursor()

# Criando a tabela de produtos
cursor.execute('''
CREATE TABLE IF NOT EXISTS produtos (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nome TEXT NOT NULL,
    descricao TEXT,
    preco REAL NOT NULL,
    quantidade INTEGER NOT NULL
)
''')

# Criando a tabela de entradas de estoque
cursor.execute('''
CREATE TABLE IF NOT EXISTS entradas (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    produto_id INTEGER,
    quantidade INTEGER,
    data TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (produto_id) REFERENCES produtos(id)
)
''')

# Criando a tabela de saídas de estoque
cursor.execute('''
CREATE TABLE IF NOT EXISTS saidas (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    produto_id INTEGER,
    quantidade INTEGER,
    data TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (produto_id) REFERENCES produtos(id)
)
''')

# Criando a tabela de vendas
cursor.execute('''
CREATE TABLE IF NOT EXISTS vendas (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    produto_id INTEGER,
    quantidade INTEGER,
    valor_total REAL,
    data TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    metodo_pagamento TEXT,
    FOREIGN KEY (produto_id) REFERENCES produtos(id)
)
''')

# Criando a tabela de usuários
cursor.execute('''
CREATE TABLE IF NOT EXISTS usuarios (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nome TEXT NOT NULL,
    senha TEXT NOT NULL,
    tipo TEXT NOT NULL
)
''')

# Confirmando as mudanças no banco
conn.commit()

# Funções de Manipulação de Estoque e Vendas

def adicionar_produto(nome, descricao, preco, quantidade):
    cursor.execute('''
    INSERT INTO produtos (nome, descricao, preco, quantidade)
    VALUES (?, ?, ?, ?)
    ''', (nome, descricao, preco, quantidade))
    conn.commit()

def registrar_entrada(produto_id, quantidade):
    cursor.execute('''
    INSERT INTO entradas (produto_id, quantidade)
    VALUES (?, ?)
    ''', (produto_id, quantidade))
    
    cursor.execute('''
    UPDATE produtos
    SET quantidade = quantidade + ?
    WHERE id = ?
    ''', (quantidade, produto_id))
    
    conn.commit()

def registrar_saida(produto_id, quantidade):
    cursor.execute('''
    SELECT quantidade FROM produtos WHERE id = ?
    ''', (produto_id,))
    estoque_atual = cursor.fetchone()[0]
    
    if estoque_atual >= quantidade:
        cursor.execute('''
        INSERT INTO saidas (produto_id, quantidade)
        VALUES (?, ?)
        ''', (produto_id, quantidade))
        
        cursor.execute('''
        UPDATE produtos
        SET quantidade = quantidade - ?
        WHERE id = ?
        ''', (quantidade, produto_id))
        
        conn.commit()
    else:
        messagebox.showwarning("Aviso", "Estoque insuficiente!")

def registrar_venda(produto_id, quantidade, metodo_pagamento):
    cursor.execute('''
    SELECT preco FROM produtos WHERE id = ?
    ''', (produto_id,))
    preco = cursor.fetchone()[0]
    valor_total = preco * quantidade
    
    cursor.execute('''
    INSERT INTO vendas (produto_id, quantidade, valor_total, metodo_pagamento)
    VALUES (?, ?, ?, ?)
    ''', (produto_id, quantidade, valor_total, metodo_pagamento))
    
    cursor.execute('''
    UPDATE produtos
    SET quantidade = quantidade - ?
    WHERE id = ?
    ''', (quantidade, produto_id))
    
    conn.commit()

def gerar_relatorio_entradas():
    cursor.execute('''
    SELECT produtos.nome, entradas.quantidade, entradas.data
    FROM entradas
    JOIN produtos ON entradas.produto_id = produtos.id
    ''')
    entradas = cursor.fetchall()
    return entradas

def gerar_relatorio_saidas():
    cursor.execute('''
    SELECT produtos.nome, saidas.quantidade, saidas.data
    FROM saidas
    JOIN produtos ON saidas.produto_id = produtos.id
    ''')
    saidas = cursor.fetchall()
    return saidas

def backup_banco():
    shutil.copy('estoque.db', 'backup_estoque.db')

# Interface Gráfica (Tkinter)

root = tk.Tk()
root.title("Controle de Estoque")
root.geometry("600x600")
root.config(bg="#F4F4F9")

font_titulo = tkfont.Font(family="Helvetica", size=16, weight="bold")
font_label = tkfont.Font(family="Arial", size=12)
font_entrada = tkfont.Font(family="Arial", size=12)

frame = tk.Frame(root, bg="#F4F4F9")
frame.pack(pady=20)

titulo = tk.Label(frame, text="Controle de Estoque", font=font_titulo, bg="#F4F4F9", fg="#4A90E2")
titulo.grid(row=0, column=0, columnspan=2, pady=10)

# Campos de Entrada de Dados
label_nome = tk.Label(frame, text="Nome do Produto:", font=font_label, bg="#F4F4F9")
label_nome.grid(row=1, column=0, sticky="w", padx=10)
entry_nome = tk.Entry(frame, font=font_entrada, bd=2, relief="solid", width=25)
entry_nome.grid(row=1, column=1, padx=10, pady=5)

label_descricao = tk.Label(frame, text="Descrição:", font=font_label, bg="#F4F4F9")
label_descricao.grid(row=2, column=0, sticky="w", padx=10)
entry_descricao = tk.Entry(frame, font=font_entrada, bd=2, relief="solid", width=25)
entry_descricao.grid(row=2, column=1, padx=10, pady=5)

label_preco = tk.Label(frame, text="Preço:", font=font_label, bg="#F4F4F9")
label_preco.grid(row=3, column=0, sticky="w", padx=10)
entry_preco = tk.Entry(frame, font=font_entrada, bd=2, relief="solid", width=25)
entry_preco.grid(row=3, column=1, padx=10, pady=5)

label_quantidade = tk.Label(frame, text="Quantidade:", font=font_label, bg="#F4F4F9")
label_quantidade.grid(row=4, column=0, sticky="w", padx=10)
entry_quantidade = tk.Entry(frame, font=font_entrada, bd=2, relief="solid", width=25)
entry_quantidade.grid(row=4, column=1, padx=10, pady=5)

# Botões
def adicionar_produto_gui():
    nome = entry_nome.get()
    descricao = entry_descricao.get()
    try:
        preco = float(entry_preco.get())
        quantidade = int(entry_quantidade.get())
        if nome and preco >= 0 and quantidade >= 0:
            adicionar_produto(nome, descricao, preco, quantidade)
            messagebox.showinfo("Sucesso", "Produto adicionado com sucesso!")
            entry_nome.delete(0, tk.END)
            entry_descricao.delete(0, tk.END)
            entry_preco.delete(0, tk.END)
            entry_quantidade.delete(0, tk.END)
        else:
            messagebox.showerror("Erro", "Preencha todos os campos corretamente.")
    except ValueError:
        messagebox.showerror("Erro", "Preço e quantidade devem ser valores numéricos.")

btn_adicionar = tk.Button(frame, text="Adicionar Produto", command=adicionar_produto_gui, font=font_label, bg="#4A90E2", fg="white", bd=0, width=20, height=2)
btn_adicionar.grid(row=5, column=0, columnspan=2, pady=10)

def consultar_estoque_gui():
    estoque_text.delete('1.0', tk.END)
    cursor.execute('SELECT id, nome, descricao, preco, quantidade FROM produtos')
    produtos = cursor.fetchall()
    if produtos:
        estoque_text.insert(tk.END, "ID | Nome | Descrição | Preço | Quantidade\n")
        estoque_text.insert(tk.END, "-"*60 + "\n")
        for prod in produtos:
            estoque_text.insert(tk.END, f"{prod[0]} | {prod[1]} | {prod[2]} | R${prod[3]:.2f} | {prod[4]}\n")
    else:
        estoque_text.insert(tk.END, "Nenhum produto cadastrado.")

btn_estoque = tk.Button(frame, text="Consultar Estoque", command=consultar_estoque_gui, font=font_label, bg="#50E3C2", fg="white", bd=0, width=20, height=2)
btn_estoque.grid(row=6, column=0, columnspan=2, pady=10)

estoque_text = tk.Text(frame, height=10, width=50, font=font_label, bd=2, relief="solid")
estoque_text.grid(row=7, column=0, columnspan=2, padx=10, pady=5)

label_produto_id = tk.Label(frame, text="ID do Produto (Entrada):", font=font_label, bg="#F4F4F9")
label_produto_id.grid(row=8, column=0, sticky="w", padx=10)
entry_produto_id = tk.Entry(frame, font=font_entrada, bd=2, relief="solid", width=25)
entry_produto_id.grid(row=8, column=1, padx=10, pady=5)

label_quantidade_entrada = tk.Label(frame, text="Quantidade de Entrada:", font=font_label, bg="#F4F4F9")
label_quantidade_entrada.grid(row=9, column=0, sticky="w", padx=10)
entry_quantidade_entrada = tk.Entry(frame, font=font_entrada, bd=2, relief="solid", width=25)
entry_quantidade_entrada.grid(row=9, column=1, padx=10, pady=5)

def registrar_entrada_gui():
    try:
        produto_id = int(entry_produto_id.get())
        quantidade = int(entry_quantidade_entrada.get())
        registrar_entrada(produto_id, quantidade)
        messagebox.showinfo("Sucesso", "Entrada registrada com sucesso!")
    except ValueError:
        messagebox.showerror("Erro", "Por favor, insira valores válidos para ID e quantidade.")

btn_entrada = tk.Button(frame, text="Registrar Entrada", command=registrar_entrada_gui, font=font_label, bg="#50E3C2", fg="white", bd=0, width=20, height=2)
btn_entrada.grid(row=10, column=0, columnspan=2, pady=10)

label_produto_id_saida = tk.Label(frame, text="ID do Produto (Saída):", font=font_label, bg="#F4F4F9")
label_produto_id_saida.grid(row=11, column=0, sticky="w", padx=10)
entry_produto_id_saida = tk.Entry(frame, font=font_entrada, bd=2, relief="solid", width=25)
entry_produto_id_saida.grid(row=11, column=1, padx=10, pady=5)

label_quantidade_saida = tk.Label(frame, text="Quantidade de Saída:", font=font_label, bg="#F4F4F9")
label_quantidade_saida.grid(row=12, column=0, sticky="w", padx=10)
entry_quantidade_saida = tk.Entry(frame, font=font_entrada, bd=2, relief="solid", width=25)
entry_quantidade_saida.grid(row=12, column=1, padx=10, pady=5)

def registrar_saida_gui():
    try:
        produto_id = int(entry_produto_id_saida.get())
        quantidade = int(entry_quantidade_saida.get())
        registrar_saida(produto_id, quantidade)
        messagebox.showinfo("Sucesso", "Saída registrada com sucesso!")
    except ValueError:
        messagebox.showerror("Erro", "Por favor, insira valores válidos para ID e quantidade.")

btn_saida = tk.Button(frame, text="Registrar Saída", command=registrar_saida_gui, font=font_label, bg="#50E3C2", fg="white", bd=0, width=20, height=2)
btn_saida.grid(row=13, column=0, columnspan=2, pady=10)

root.mainloop()