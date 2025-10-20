# Função para adicionar produto
def adicionar_produto(nome, descricao, preco, quantidade):
    cursor.execute('''
    INSERT INTO produtos (nome, descricao, preco, quantidade)
    VALUES (?, ?, ?, ?)
    ''', (nome, descricao, preco, quantidade))
    conn.commit()
    print(f'Produto {nome} adicionado ao estoque.')