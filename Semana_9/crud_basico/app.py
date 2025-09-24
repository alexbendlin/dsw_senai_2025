import os
from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy

# Encontra o caminho absoluto do diretório do arquivo atual
basedir = os.path.abspath(os.path.dirname(__file__))

# Inicialização do App Flask
app = Flask(__name__)

# Configuração do Banco de Dados SQLAlchemy
# Define o caminho do banco de dados SQLite dentro do diretório do projeto
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'database.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False  # Desativa o rastreamento de modificações do SQLAlchemy

# Inicialização do SQLAlchemy com o app Flask
db = SQLAlchemy(app)

# --- MODELO DO BANCO DE DADOS ---
# O modelo define a estrutura da nossa tabela no banco de dados.
class Usuario(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)

    def __repr__(self):
        return f'<Usuario {self.nome}>'

# --- ROTAS DA APLICAÇÃO ---

# Rota READ (Ler): Página inicial que lista todos os usuários.
@app.route('/')
def index():
    # Busca todos os usuários no banco de dados
    usuarios = Usuario.query.all()
    # Renderiza o template 'index.html' passando a lista de usuários
    return render_template('index.html', usuarios=usuarios)

# Rota CREATE (Criar): Página para adicionar um novo usuário.
@app.route('/adicionar', methods=['GET', 'POST'])
def adicionar():
    # Se o método da requisição for POST, o formulário foi enviado.
    if request.method == 'POST':
        # Pega os dados do formulário
        nome = request.form['nome']
        email = request.form['email']

        # Cria um novo objeto Usuario com os dados recebidos
        novo_usuario = Usuario(nome=nome, email=email)

        # Adiciona o novo usuário à sessão do banco de dados e salva (commit)
        try:
            db.session.add(novo_usuario)
            db.session.commit()
            # Redireciona o usuário para a página inicial
            return redirect(url_for('index'))
        except:
            return "Ocorreu um erro ao adicionar o usuário."

    # Se o método for GET, apenas exibe a página com o formulário.
    return render_template('adicionar.html')

# Rota UPDATE (Atualizar): Página para editar um usuário existente.
@app.route('/editar/<int:id>', methods=['GET', 'POST'])
def editar(id):
    # Busca o usuário pelo ID. Se não encontrar, retorna erro 404.
    usuario = Usuario.query.get_or_404(id)

    # Se o formulário for enviado (POST)
    if request.method == 'POST':
        usuario.nome = request.form['nome']
        usuario.email = request.form['email']
        try:
            db.session.commit()
            return redirect(url_for('index'))
        except:
            return "Ocorreu um erro ao editar o usuário."
    else:
        # Se for GET, apenas exibe o formulário preenchido com os dados do usuário.
        return render_template('editar.html', usuario=usuario)

# Rota DELETE (Deletar): Rota para deletar um usuário.
# Usamos o método POST para mais segurança.
@app.route('/deletar/<int:id>', methods=['POST'])
def deletar(id):
    # Busca o usuário pelo ID.
    usuario = Usuario.query.get_or_404(id)
    try:
        db.session.delete(usuario)
        db.session.commit()
        return redirect(url_for('index'))
    except:
        return "Ocorreu um erro ao deletar o usuário."

# Bloco principal para rodar a aplicação
if __name__ == '__main__':
    # Cria o banco de dados e as tabelas (se não existirem) antes de rodar a app
    with app.app_context():
        db.create_all()
    app.run(debug=True)