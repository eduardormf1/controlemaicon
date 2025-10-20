from flask import Flask, render_template, request, redirect, url_for, flash
import db  # Importando as funções de banco de dados
import locale

app = Flask(__name__)
app.secret_key = 's3cr3t'  # Para mensagens flash

# Configurar o locale para moeda brasileira (R$)
locale.setlocale(locale.LC_ALL, 'pt_BR.UTF-8')  # Configura para usar a moeda brasileira

# Verificar se o banco de dados existe e criar se necessário
db.verificar_banco()

# Adicionar a coluna preco_custo se não existir
db.adicionar_preco_custo()

# Página principal
@app.route('/')
def index():
    produtos = db.get_produtos()  # Usando a função do db.py
    
    # Transformando cada produto em um dicionário para permitir a modificação
    produtos_formatados = []
    for produto in produtos:
        produto_dict = dict(produto)  # Convertendo o sqlite3.Row em um dicionário
        produto_dict['preco'] = locale.currency(produto_dict['preco'], grouping=True)  # Preço de venda
        produto_dict['preco_custo'] = locale.currency(produto_dict['preco_custo'], grouping=True)  # Preço de custo
        
        # Calculando o total de vendas do produto
        total_vendas = db.somar_vendas(produto_dict['id'])
        produto_dict['total_vendas'] = locale.currency(total_vendas, grouping=True)  # Total de vendas formatado

        produtos_formatados.append(produto_dict)

    # Passando os produtos formatados para o template
    return render_template('index.html', produtos=produtos_formatados)

# Adicionar produto
@app.route('/adicionar', methods=['POST'])
def adicionar_produto():
    nome = request.form['nome']
    descricao = request.form['descricao']
    preco = float(request.form['preco'])
    preco_custo = float(request.form['preco_custo'])  # Novo campo para preço de custo
    quantidade = int(request.form['quantidade'])
    
    db.adicionar_produto(nome, descricao, preco, preco_custo, quantidade)  # Passando o preco_custo
    flash(f'Produto {nome} adicionado ao estoque!', 'success')
    return redirect(url_for('index'))

# Registrar entrada no estoque
@app.route('/entrada', methods=['POST'])
def registrar_entrada():
    produto_id = int(request.form['produto_id'])
    quantidade = int(request.form['quantidade'])
    
    db.registrar_entrada(produto_id, quantidade)  # Usando a função do db.py
    flash(f'Entrada de {quantidade} unidades registrada!', 'success')
    return redirect(url_for('index'))

# Registrar saída no estoque
@app.route('/saida', methods=['POST'])
def registrar_saida():
    produto_id = int(request.form['produto_id'])
    quantidade = int(request.form['quantidade'])
    
    db.registrar_saida(produto_id, quantidade)  # Usando a função do db.py
    flash(f'Saída de {quantidade} unidades registrada!', 'success')
    return redirect(url_for('index'))

# Registrar venda
@app.route('/venda', methods=['POST'])
def registrar_venda():
    produto_id = int(request.form['produto_id'])
    quantidade = int(request.form['quantidade'])
    metodo_pagamento = request.form['metodo_pagamento']
    
    db.registrar_venda(produto_id, quantidade, metodo_pagamento)  # Usando a função do db.py
    flash(f"Venda registrada. Total: R${quantidade * db.get_produtos()[produto_id-1]['preco']:.2f} com pagamento via {metodo_pagamento}.", 'success')
    return redirect(url_for('index'))

# Remover produto do estoque
@app.route('/remover', methods=['POST'])
def remover_produto():
    produto_id = int(request.form['produto_id'])
    quantidade = int(request.form['quantidade'])

    if quantidade <= 0:
        flash('A quantidade deve ser maior que zero!', 'danger')
        return redirect(url_for('index'))

    # Verifica a quantidade disponível no estoque
    conn = db.conectar_db()
    cursor = conn.cursor()
    cursor.execute('''
    SELECT quantidade FROM produtos WHERE id = ?
    ''', (produto_id,))
    estoque_atual = cursor.fetchone()[0]

    if estoque_atual < quantidade:
        flash('Estoque insuficiente!', 'danger')
        return redirect(url_for('index'))

    # Atualiza a quantidade no estoque
    cursor.execute('''
    UPDATE produtos
    SET quantidade = quantidade - ?
    WHERE id = ?
    ''', (quantidade, produto_id))
    conn.commit()
    conn.close()

    flash(f'{quantidade} unidades removidas do estoque!', 'success')
    return redirect(url_for('index'))

# Excluir produto do estoque
@app.route('/excluir', methods=['POST'])
def excluir_produto():
    produto_id = int(request.form['produto_id'])

    # Conectar ao banco de dados
    conn = db.conectar_db()
    cursor = conn.cursor()

    # Excluir o produto do banco de dados
    cursor.execute('''
    DELETE FROM produtos WHERE id = ?
    ''', (produto_id,))
    conn.commit()
    conn.close()

    flash('Produto excluído do estoque!', 'success')
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)