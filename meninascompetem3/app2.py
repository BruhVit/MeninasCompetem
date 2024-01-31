from flask import Flask, render_template, request, redirect, url_for
import sqlite3
import pandas as pd

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

#pesquisa por filtro de categoria e nivel
def filtragem(categorias, niveis):
    with sqlite3.connect(DATABASE) as con:
        placeholders_categoria = ",".join(["?"] * len(categorias))
        placeholders_nivel = ",".join(["?"] * len(niveis))
        query = f"SELECT * FROM usuarios WHERE categoria IN ({placeholders_categoria}) AND nivel IN ({placeholders_nivel})"
        params = tuple(categorias + niveis)  # Convert lists to tuples
        df = pd.read_sql(query, con, params=params)
    return df

#pesquisa por palavra chave
def pesquisa(termo):
    with sqlite3.connect(DATABASE) as con:
        query = "SELECT * FROM usuarios WHERE nome LIKE ? OR descricao LIKE ?"
        params = ('%' + termo + '%', '%' + termo + '%')  # Pass termo for both placeholders
        df = pd.read_sql(query, con, params=params)
    return df


@app.route('/pagina_dois.html', methods=['GET', 'POST'])
def display_results():
    if request.method == 'POST':
        if 'filter_action' in request.form:
            categorias = request.form.getlist('categoria[]')
            niveis = request.form.getlist('nivel[]')
            if not categorias:
                categorias = ['']
            if not niveis:
                niveis = ['']
            print("Categorias:", categorias)
            print("Niveis:", niveis)
            dataframe = filtragem(categorias, niveis)
            print("Filtered Dataframe:")
            print(dataframe)  # Print the dataframe for debugging
        elif 'search_action' in request.form:
            search_term = request.form['search_term']
            print("Search Term:", search_term)
            dataframe = pesquisa(search_term)
            print("Searched Dataframe:")
            print(dataframe)  # Print the dataframe for debugging
    else:
        dataframe = pd.DataFrame() 
    return render_template('pagina_dois.html', dataframe=dataframe)

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
    
    