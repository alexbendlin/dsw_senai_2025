from flask import Flask, render_template

app = Flask(__name__)

@app.route('/')
def index():
    nome_usuario = 'Alunos'
    return render_template('index.html', usuario=nome_usuario)

@app.route("/produtos")
def produtos():
    lista_produtos = [
        {'nome': 'Produto 1', 'preco': 'R$ 1.500,00'},
        {'nome': 'Produto 2', 'preco': 'R$ 2.500,00'},
        {'nome': 'Produto 3', 'preco': 'R$ 4.800,00'}
    ]
    return render_template('produtos.html', produtos=lista_produtos)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
