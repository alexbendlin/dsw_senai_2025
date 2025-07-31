from flask import Flask, request

app = Flask(__name__)

@app.route('/')
def ola_mundo():
    return "<h1>Olá galera!!!</h1>"

@app.route('/sobre')
def sobre():
    return "Está é a página sobre!"

@app.route('/perfil/<usuario>')
def perfil(usuario):
    return f'<h1>Exibindo o perfil de: {usuario}</h1>'

@app.route('/produto/<int:id_produto>')
def consultar_produto(id_produto):
    return f"<h1>Exibindo dados do produto com ID: {id_produto}</h1>"

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        usuario = request.form['usuario']
        return f'<h1>Usuário: {usuario}'
    else:
        return '''
          <form method="post">
            <input type="text" name="usuario">
            <input type="submit" value="Login">
          </form>    
        '''

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
