from flask import Flask, render_template, request, redirect, url_for
import sqlite3

app = Flask(__name__)

DATABASE = 'comp2.db'

def criar_tabela():
    with sqlite3.connect(DATABASE) as con:
        cur = con.cursor()
        cur.execute('CREATE TABLE IF NOT EXISTS usuarios(id integer PRIMARY KEY, nome TEXT NOT NULL, site TEXT NOT NULL, descricao TEXT NOT NULL, data_final DATE, valor TEXT NOT NULL, nivel TEXT NOT NULL, categoria TEXT NOT NULL)')
        con.commit()

criar_tabela()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/pagina_inicial.html')
def pagina_inicial():
    return render_template('pagina_inicial.html')

@app.route('/pagina_um.html')
def pagina_um():
    return render_template('pagina_um.html')

@app.route('/pagina_dois.html')
def pagina_dois():
    pesquisa_padrao = '0'  # Defina o valor padrão desejado

    with sqlite3.connect(DATABASE) as con:
        cur = con.cursor()
        resultado = cur.execute('SELECT nome, site, categoria FROM usuarios WHERE categoria LIKE ?', ('%' + pesquisa_padrao + '%',)).fetchall()

    return render_template('pagina_dois.html', resultados=resultado or [])

@app.route('/processar_pesquisa', methods=['POST'])
def processar_pesquisa():
    pesquisa_palavra = request.form.get('termo_pesquisa', '')  # Provide default value if pesquisa_palavra is None
    categoria = request.form.getlist('categoria')
    nivel = request.form.getlist('nivel')

    with sqlite3.connect(DATABASE) as con:
        cur = con.cursor()
        if categoria and nivel:
            query = '''SELECT nome, descricao, nivel, valor, data_final, site FROM usuarios WHERE (nome LIKE ? OR descricao LIKE ?) AND categoria IN ({}) AND nivel IN ({})'''.format(','.join(['?']*len(categoria)), ','.join(['?']*len(niveis)))
            params = ['%' + nivel + '%', categoria] * 2  # Duplicate pesquisa_palavra
            params += categoria + nivel
            cur.execute(query, params)
        else:
            query = '''SELECT nome, descricao, nivel, valor, data_final, categoria, site FROM usuarios WHERE nome LIKE ? OR descricao LIKE ?'''
            params = ['%' + pesquisa_palavra + '%']
            cur.execute(query, params)

        resultado = cur.fetchall()

    if resultado:
        return render_template('pagina_dois.html', resultados=resultado)
    else:
        return render_template('pagina_dois.html', resultados=[])



@app.route('/seu-script-de-processamento', methods=['POST'])
def processar_formulario():
    nome = request.form.get('nome')
    site = request.form.get('site')
    descricao = request.form.get('descricao')
    data_final = request.form.get('data_final')
    valor = request.form.get('valor')
    nivel = request.form.getlist('nivel')
    nivel_str = ', '.join(nivel)
    categoria = request.form.get('categoria')

    

    if nome and site and descricao and categoria and data_final and valor and nivel and categoria is not None:
        with sqlite3.connect(DATABASE) as con:
            cur = con.cursor()
            id
            cur.execute('INSERT INTO usuarios (nome, site, descricao, data_final, valor, nivel, categoria) VALUES (?,?,?,?,?,?,?)', (nome, site, descricao, data_final, valor, nivel_str, categoria))
            con.commit()
            return redirect(url_for('index'))
    return redirect(url_for('index'))

def new_func(nivel):
    return nivel


if __name__ == '__main__':
    app.run(debug=True)