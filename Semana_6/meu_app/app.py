# -*- coding: utf-8 -*-

# Passo 1: Importações e Configuração
from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy

# Inicializa a aplicação Flask
app = Flask(__name__)
app.config['SECRET_KEY'] = 'Sua-Segurança-Mora-Aqui'

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///meuapp.db'

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

app.config['SECRET_KEY'] = 'sua-chave-secreta-pode-ser-qualquer-coisa'

class Usuario(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)

    def __repr__(self):
        return f'<Usuário: {self.nome}>'

class Postagem(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    titulo = db.Column(db.String(80), unique=True, nullable=False)
    descricao = db.Column(db.String(200), unique=True, nullable=False)

    def __repr__(self):
        return f'<Título: {self.titulo}>'


# --- Rotas da Aplicação ---

# Rota principal que exibe o formulário e a lista de usuários
@app.route('/')
def index():
    usuarios = Usuario.query.all()
    return render_template('index.html', usuarios=usuarios)

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
    postagens = Postagem().query.all()
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
    with app.app_context():
        # db.drop_all()
        db.create_all()
 
    # Inicia o servidor de desenvolvimento do Flask
    app.run(host='0.0.0.0', port=5001, debug=True)
