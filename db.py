import sqlite3

# Função para conectar ao banco de dados
def conectar_db():
    conn = sqlite3.connect('estoque.db')
    conn.row_factory = sqlite3.Row  # Para acessar as colunas pelo nome
    return conn

# Função para criar o banco de dados e as tabelas
def criar_banco():
    conn = conectar_db()
    cursor = conn.cursor()

    # Criar tabela de produtos
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS produtos (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nome TEXT NOT NULL,
        descricao TEXT,
        preco REAL NOT NULL,
        preco_custo REAL NOT NULL,
        quantidade INTEGER NOT NULL
    )
    ''')

    # Criar tabela de vendas
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

    # Confirmar as mudanças e fechar a conexão
    conn.commit()
    conn.close()

# Função para verificar se o banco de dados existe e criar se necessário
def verificar_banco():
    try:
        conectar_db()
    except sqlite3.DatabaseError:
        criar_banco()

# Função para adicionar a coluna preco_custo à tabela produtos, se não existir
def adicionar_preco_custo():
    conn = conectar_db()
    cursor = conn.cursor()
    try:
        # Tenta adicionar a coluna preco_custo se ela não existir
        cursor.execute('''
        ALTER TABLE produtos ADD COLUMN preco_custo REAL DEFAULT 0
        ''')
        conn.commit()
    except sqlite3.OperationalError:
        # Se a coluna já existir, a exceção será capturada e ignorada
        pass
    finally:
        conn.close()

# Função para obter todos os produtos
def get_produtos():
    conn = conectar_db()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM produtos")
    produtos = cursor.fetchall()
    conn.close()
    return produtos

# Função para adicionar um produto
def adicionar_produto(nome, descricao, preco, preco_custo, quantidade):
    conn = conectar_db()
    cursor = conn.cursor()
    cursor.execute('''
    INSERT INTO produtos (nome, descricao, preco, preco_custo, quantidade)
    VALUES (?, ?, ?, ?, ?)
    ''', (nome, descricao, preco, preco_custo, quantidade))
    conn.commit()
    conn.close()

# Função para registrar entrada
def registrar_entrada(produto_id, quantidade):
    conn = conectar_db()
    cursor = conn.cursor()
    cursor.execute('''
    UPDATE produtos
    SET quantidade = quantidade + ?
    WHERE id = ?
    ''', (quantidade, produto_id))
    conn.commit()
    conn.close()

# Função para registrar saída
def registrar_saida(produto_id, quantidade):
    conn = conectar_db()
    cursor = conn.cursor()
    cursor.execute('''
    SELECT quantidade FROM produtos WHERE id = ?
    ''', (produto_id,))
    estoque_atual = cursor.fetchone()[0]
    
    if estoque_atual >= quantidade:
        cursor.execute('''
        UPDATE produtos
        SET quantidade = quantidade - ?
        WHERE id = ?
        ''', (quantidade, produto_id))
        conn.commit()
    conn.close()

# Função para registrar venda
def registrar_venda(produto_id, quantidade, metodo_pagamento):
    conn = conectar_db()
    cursor = conn.cursor()
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
    conn.close()

# Função para calcular o total de vendas de um produto
def somar_vendas(produto_id):
    conn = conectar_db()
    cursor = conn.cursor()
    cursor.execute('''
    SELECT SUM(valor_total) FROM vendas WHERE produto_id = ?
    ''', (produto_id,))
    total_vendas = cursor.fetchone()[0]
    conn.close()
    return total_vendas if total_vendas else 0  # Retorna 0 se não houver vendas