# Função para registrar saída do estoque
def registrar_saida(produto_id, quantidade):
    # Verificando a quantidade disponível no estoque
    cursor.execute('''
    SELECT quantidade FROM produtos WHERE id = ?
    ''', (produto_id,))
    estoque_atual = cursor.fetchone()[0]
    
    if estoque_atual >= quantidade:
        cursor.execute('''
        INSERT INTO saidas (produto_id, quantidade)
        VALUES (?, ?)
        ''', (produto_id, quantidade))
        
        # Atualizando a quantidade no estoque
        cursor.execute('''
        UPDATE produtos
        SET quantidade = quantidade - ?
        WHERE id = ?
        ''', (quantidade, produto_id))
        
        conn.commit()
        print(f'Saída de {quantidade} unidades registrada para o produto ID {produto_id}.')
    else:
        print('Estoque insuficiente para a saída.')