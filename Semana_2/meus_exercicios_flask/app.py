from flask import Flask, render_template

# Inicializa a aplicação Flask
app = Flask(__name__)

# --- Exercício 1: Exibindo uma Mensagem de Boas-Vindas ---
@app.route('/')
@app.route('/bemvindo')
def exercicio1():
    """
    Esta função responde à URL /bemvindo.
    Ela passa uma variável 'nome_usuario' para o template 'exercicio1.html'.
    """
    nome_usuario = "Maria"
    return render_template('exercicio1.html', nome_usuario=nome_usuario)

# --- Exercício 2: Listando Itens ---
@app.route('/cursos')
def exercicio2():
    """
    Esta função responde à URL /cursos.
    Ela passa uma lista de cursos para o template 'exercicio2.html'.
    """
    lista_de_cursos = [
        "Desenvolvimento Web com Flask",
        "Python para Análise de Dados",
        "Introdução a Machine Learning",
        "Banco de Dados SQL"
    ]
    return render_template('exercicio2.html', cursos=lista_de_cursos)

# --- Exercício 3: Usando Condicionais ---
@app.route('/perfil/<nome>')
@app.route('/perfil')
def exercicio3(nome=None):
    """
    Esta função responde a /perfil e /perfil/<nome>.
    Ela simula um status de login e passa para o template 'exercicio3.html'.
    """
    logado = nome is not None
    return render_template('exercicio3.html', usuario_logado=logado, nome_usuario=nome)

# --- Exercício 4: Herança de Templates ---
@app.route('/sobre')
def exercicio4():
    """
    Renderiza a página 'Sobre', que herda o layout base.
    """
    return render_template('sobre.html')


# --- Bloco para rodar a aplicação ---
if __name__ == '__main__':
    # O modo debug reinicia o servidor automaticamente a cada alteração no código.
    app.run(host='0.0.0.0', port=5000, debug=True)
