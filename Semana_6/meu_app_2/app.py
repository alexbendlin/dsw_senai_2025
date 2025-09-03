# -*- coding: utf-8 -*-

# Passo 1: Importações e Configuração
from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy

# Inicializa a aplicação Flask
app = Flask(__name__)

# Chave secreta para segurança das sessões e formulários
app.config['SECRET_KEY'] = 'sua-chave-secreta-pode-ser-qualquer-coisa'

# Configuração do Banco de Dados SQLite
# Isso cria um arquivo 'meuapp.db' no diretório do seu projeto
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///meuapp.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False  # Opcional, mas remove um aviso de performance

# Inicializa a extensão do banco de dados com a aplicação
db = SQLAlchemy(app)


# Passo 2: Criando o Modelo (a "planta" da nossa tabela)
class Usuario(db.Model):
    """
    Define a estrutura da tabela 'usuario' no banco de dados.
    Cada atributo da classe representa uma coluna na tabela.
    """
    id = db.Column(db.Integer, primary_key=True)  # ID único para cada usuário
    nome = db.Column(db.String(80), unique=True, nullable=False)  # Nome do usuário, não pode repetir e não pode ser nulo
    email = db.Column(db.String(120), unique=True, nullable=False) # Email do usuário, também único e obrigatório

    def __repr__(self):
        """
        Representação em string do objeto, útil para debug.
        Corrigido de self.username para self.nome para corresponder ao modelo.
        """
        return f'<Usuário {self.nome}>'

class Postagem(db.Model):
    id = db.Column(db.Integer, primary_key=True)  # ID único para cada postagem
    titulo = db.Column(db.String(80), unique=True, nullable=False)  # Título da postagem, não pode repetir e não pode ser nulo
    descricao = db.Column(db.String(120), unique=True, nullable=False) # Descrição da postagem, também única e obrigatória

    def __repr__(self):
        return f'<Postagem {self.titulo}>'

# --- Rotas da Aplicação ---

# Rota principal que exibe o formulário e a lista de usuários
@app.route('/')
def index():
    usuarios = Usuario.query.all()
    # Agora renderiza o arquivo 'index.html' da pasta 'templates'
    return render_template('index.html', usuarios=usuarios)

# Rota para processar o formulário de adição de usuário
@app.route('/adicionar', methods=['POST'])
def adicionar_usuario():
    nome = request.form['nome']
    email = request.form['email']
    novo_usuario = Usuario(nome=nome, email=email)
    db.session.add(novo_usuario)
    db.session.commit()
    return redirect(url_for('index'))

@app.route('/postagens')
def postagens():
    postagens = Postagem.query.all()
    # Agora renderiza o arquivo 'postagens.html' da pasta 'templates'
    return render_template('postagens.html', postagens=postagens)

@app.route('/adicionar_postagem', methods=['POST'])
def adicionar_postagem():
    titulo = request.form['titulo']
    descricao = request.form['descricao']
    nova_postagem = Postagem(titulo=titulo, descricao=descricao)
    db.session.add(nova_postagem)
    db.session.commit()
    return redirect(url_for('postagens'))

# Passo 3: Criando o Banco de Dados Físico
if __name__ == '__main__':
    # O 'app_context' é necessário para que o Flask-SQLAlchemy saiba qual aplicação está usando.
    with app.app_context():
        print("Apagando o banco de dados antigo (se existir)...")
        db.drop_all()  # Apaga todas as tabelas (cuidado em produção!)
        print("Criando todas as tabelas do zero...")
        db.create_all() # Cria as tabelas com base nos modelos definidos (class Usuario)
        print("Banco de dados e tabelas criados com sucesso!")

    # Inicia o servidor de desenvolvimento do Flask
    app.run(host='0.0.0.0', port=5001, debug=True)
