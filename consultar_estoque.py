# Função para consultar o estoque atual
def consultar_estoque():
    cursor.execute('SELECT * FROM produtos')
    produtos = cursor.fetchall()
    print('Estoque Atual:')
    for produto in produtos:
        print(f'{produto[1]} (ID: {produto[0]}) - {produto[4]} unidades disponíveis.')