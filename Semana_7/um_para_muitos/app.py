# -*- coding: utf-8 -*-

import os
from flask import Flask, request, redirect, url_for, render_template, flash
from flask_sqlalchemy import SQLAlchemy

# -----------------------------------------------------------------------------
# CONFIGURAÇÃO DA APLICAÇÃO FLASK E DO BANCO DE DADOS
# -----------------------------------------------------------------------------

# Cria uma instância da aplicação Flask
app = Flask(__name__)

# Configurações da aplicação
# Chave secreta para proteger a sessão e outras funcionalidades de segurança
app.config['SECRET_KEY'] = 'uma-chave-secreta-bem-segura'

# Define o caminho para o arquivo de banco de dados SQLite
# Ele será criado no mesmo diretório deste script
basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'database.db')

# Desativa o rastreamento de modificações do SQLAlchemy para economizar recursos
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Inicializa a extensão SQLAlchemy para interagir com o banco de dados
db = SQLAlchemy(app)


# -----------------------------------------------------------------------------
# DEFINIÇÃO DOS MODELOS (TABELAS DO BANCO DE DADOS)
# -----------------------------------------------------------------------------

# --- Modelo Usuario (Usuário) ---
# Representa a tabela 'usuario'. É o lado "um" do relacionamento.
class Usuario(db.Model):
    __tablename__ = 'usuario'
    id = db.Column(db.Integer, primary_key=True)
    usuario_nome = db.Column(db.String(80), unique=True, nullable=False)

    # --- A MÁGICA DO RELACIONAMENTO 1-PARA-MUITOS ---
    # O relacionamento agora representa uma coleção de objetos 'Publicacao'.
    # 1. 'Publicacao': A classe do modelo "filho".
    # 2. back_populates='autor': Cria uma referência de volta no modelo 'Publicacao',
    #    permitindo acessar o autor de uma publicação (ex: minha_publicacao.autor).
    # 3. cascade='all, delete-orphan': Garante que, se um usuário for deletado,
    #    TODAS as suas publicações também serão deletadas.
    # OBS: O parâmetro 'uselist=False' foi removido. Por padrão, um relationship
    # é uma lista (um-para-muitos).
    publicacoes = db.relationship('Publicacao', back_populates='autor', cascade='all, delete-orphan')

    def __repr__(self):
        return f'<Usuário {self.usuario_nome}>'


# --- Modelo Publicacao (Publicação) ---
# Representa a tabela 'publicacao'. É o lado "muitos" do relacionamento.
class Publicacao(db.Model):
    __tablename__ = 'publicacao'
    id = db.Column(db.Integer, primary_key=True)
    titulo = db.Column(db.String(120), nullable=False)
    conteudo = db.Column(db.Text, nullable=True)

    # --- CHAVE ESTRANGEIRA ---
    # A segunda parte fundamental do relacionamento.
    # 1. db.ForeignKey('usuario.id'): Cria a ligação. A coluna 'usuario_id' nesta tabela
    #    irá armazenar o 'id' de um registro da tabela 'usuario'.
    # 2. OBS: A restrição 'unique=True' FOI REMOVIDA. Isso é CRÍTICO.
    #    Agora, um mesmo 'usuario_id' pode aparecer várias vezes na tabela 'publicacao',
    #    permitindo que um usuário tenha múltiplos publicações.
    usuario_id = db.Column(db.Integer, db.ForeignKey('usuario.id'), nullable=False)

    # Relação de volta para o modelo Usuario, conforme definido em `back_populates` acima.
    autor = db.relationship('Usuario', back_populates='publicacoes')

    def __repr__(self):
        return f'<Publicação {self.titulo}>'


# -----------------------------------------------------------------------------
# DEFINIÇÃO DAS ROTAS E LÓGICA DA APLICAÇÃO
# -----------------------------------------------------------------------------

# --- Rota Principal (/) ---
# Exibe os usuários, suas publicações e os formulários para adicionar novos dados.
@app.route('/')
def index():
    # Busca todos os usuários e suas publicações associadas (graças ao 'relationship')
    usuarios = Usuario.query.all()
    
    # O HTML é renderizado a partir de uma string para manter tudo em um único arquivo
    return render_template('index.html', usuarios=usuarios)


# --- Rota para Adicionar Usuário ---
@app.route('/adicionar_usuario', methods=['POST'])
def adicionar_usuario():
    usuario_nome = request.form.get('usuario_nome')
    if usuario_nome:
        # Verifica se o usuário já existe
        usuario_existente = Usuario.query.filter_by(usuario_nome=usuario_nome).first()
        if not usuario_existente:
            novo_usuario = Usuario(usuario_nome=usuario_nome)
            db.session.add(novo_usuario)
            db.session.commit()
            flash(f'Usuário "{usuario_nome}" adicionado com sucesso!', 'success')
        else:
            flash(f'Usuário "{usuario_nome}" já existe.', 'danger')
    return redirect(url_for('index'))


# --- Rota para Adicionar Publicação ---
@app.route('/adicionar_perfil', methods=['POST'])
def adicionar_perfil():
    usuario_id = request.form.get('usuario_id')
    titulo = request.form.get('titulo')
    conteudo = request.form.get('conteudo')

    if usuario_id and titulo:
        usuario = Usuario.query.get(usuario_id)
        if usuario:
            novo_perfil = Publicacao(titulo=titulo, conteudo=conteudo, autor=usuario)
            db.session.add(novo_perfil)
            db.session.commit()
            flash(f'Publicação "{titulo}" adicionada para {usuario.usuario_nome}!', 'success')
        else:
            flash(f'Usuário não encontrado.', 'danger')

    return redirect(url_for('index'))

# --- Rota para Deletar Usuário (e suas publicações, via cascade) ---
@app.route('/excluir_usuario/<int:usuario_id>', methods=['POST'])
def excluir_usuario(usuario_id):
    usuario_para_excluir = Usuario.query.get_or_404(usuario_id)
    usuario_nome = usuario_para_excluir.usuario_nome
    db.session.delete(usuario_para_excluir)
    db.session.commit()
    flash(f'Usuário "{usuario_nome}" e todas as suas publicações foram deletados.', 'info')
    return redirect(url_for('index'))

# -----------------------------------------------------------------------------
# INICIALIZAÇÃO DA APLICAÇÃO
# -----------------------------------------------------------------------------
if __name__ == '__main__':
    # Cria as tabelas no banco de dados, se não existirem
    with app.app_context():
        # Antes de rodar, para garantir que as tabelas antigas sejam removidas
        # e as novas sejam criadas, você pode deletar o arquivo 'database.db'
        # que está na mesma pasta deste script.
        db.create_all()
    # Roda a aplicação em modo de debug
    app.run(debug=True,port=5002)
