# Função para registrar entrada no estoque
def registrar_entrada(produto_id, quantidade):
    cursor.execute('''
    INSERT INTO entradas (produto_id, quantidade)
    VALUES (?, ?)
    ''', (produto_id, quantidade))
    
    # Atualizando a quantidade no estoque
    cursor.execute('''
    UPDATE produtos
    SET quantidade = quantidade + ?
    WHERE id = ?
    ''', (quantidade, produto_id))
    
    conn.commit()
    print(f'Entrada de {quantidade} unidades registrada para o produto ID {produto_id}.')