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
# Representa a tabela 'usuario' no banco de dados.
class Usuario(db.Model):
    __tablename__ = 'usuario'
    id = db.Column(db.Integer, primary_key=True)
    usuario_nome = db.Column(db.String(80), unique=True, nullable=False)

    # --- A MÁGICA DO RELACIONAMENTO 1-PARA-1 ---
    # O relacionamento é definido aqui, na tabela "pai".
    # 1. 'Perfil': A classe do modelo com a qual este modelo se relaciona.
    # 2. uselist=False: Este é o parâmetro CRÍTICO. Ele diz ao SQLAlchemy que este
    #    relacionamento se conectará a apenas UM registro (e não a uma lista de registros),
    #    transformando o padrão (um-para-muitos) em um-para-um.
    # 3. back_populates='usuario': Cria uma referência de volta no modelo 'Perfil'.
    #    Isso nos permite acessar o objeto Usuario a partir de um objeto Perfil (ex: meu_perfil.usuario).
    # 4. cascade='all, delete-orphan': Garante que, se um usuário for deletado,
    #    seu perfil associado também será deletado automaticamente.
    perfil = db.relationship('Perfil', uselist=False, back_populates='usuario', cascade='all, delete-orphan')

    def __repr__(self):
        return f'<Usuario {self.usuario_nome}>'


# --- Modelo Perfil (Perfil) ---
# Representa a tabela 'perfil'. Cada perfil pertencerá a um único usuário.
class Perfil(db.Model):
    __tablename__ = 'perfil'
    id = db.Column(db.Integer, primary_key=True)
    nome_completo = db.Column(db.String(120), nullable=False)
    bio = db.Column(db.Text, nullable=True)

    # --- CHAVE ESTRANGEIRA E RESTRIÇÃO DE UNICIDADE ---
    # A segunda parte fundamental da implementação do relacionamento 1-para-1.
    # 1. db.ForeignKey('usuario.id'): Cria a ligação. A coluna 'usuario_id' nesta tabela
    #    irá armazenar o 'id' de um registro da tabela 'usuario'.
    # 2. unique=True: Esta é a RESTRIÇÃO no nível do banco de dados. Ela garante que
    #    um 'usuario_id' só pode aparecer UMA VEZ na tabela 'perfil'. Isso impede
    #    fisicamente que um usuário tenha mais de um perfil.
    usuario_id = db.Column(db.Integer, db.ForeignKey('usuario.id'), unique=True, nullable=False)

    # Relação de volta para o modelo Usuario, conforme definido em `back_populates` acima.
    usuario = db.relationship('Usuario', back_populates='perfil')

    def __repr__(self):
        return f'<Perfil for {self.usuario.usuario_nome}>'


# -----------------------------------------------------------------------------
# DEFINIÇÃO DAS ROTAS E LÓGICA DA APLICAÇÃO
# -----------------------------------------------------------------------------

# --- Rota Principal (/) ---
# Exibe os usuários, seus perfis e os formulários para adicionar novos dados.
@app.route('/')
def index():
    # Busca todos os usuários e os perfis associados (graças ao 'relationship')
    usuarios = Usuario.query.all()
    # Busca usuários que ainda não têm um perfil para popular o formulário de criação de perfil
    usuarios_sem_perfil = Usuario.query.filter(Usuario.perfil == None).all()
    
    # O HTML é renderizado a partir de uma string para manter tudo em um único arquivo
    return render_template('index.html', usuarios=usuarios, usuarios_sem_perfil=usuarios_sem_perfil)


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


# --- Rota para Adicionar Perfil ---
@app.route('/adicionar_perfil', methods=['POST'])
def adicionar_perfil():
    usuario_id = request.form.get('usuario_id')
    nome_completo = request.form.get('nome_completo')
    bio = request.form.get('bio')

    if usuario_id and nome_completo:
        # A lógica do banco de dados (unique=True na coluna usuario_id) já impede
        # a criação de um segundo perfil, mas é uma boa prática verificar aqui também.
        usuario = Usuario.query.get(usuario_id)
        if usuario and not usuario.perfil:
            novo_perfil = Perfil(nome_completo=nome_completo, bio=bio, usuario_id=usuario.id)
            db.session.add(novo_perfil)
            db.session.commit()
            flash(f'Perfil para "{usuario.usuario_nome}" adicionado com sucesso!', 'success')
        else:
            flash(f'Este usuário já possui um perfil ou não existe.', 'danger')

    return redirect(url_for('index'))

# --- Rota para Deletar Usuário (e seu perfil, via cascade) ---
@app.route('/excluir_usuario/<int:usuario_id>', methods=['POST'])
def excluir_usuario(usuario_id):
    usuario_para_excluir = Usuario.query.get_or_404(usuario_id)
    usuario_nome = usuario_para_excluir.usuario_nome
    db.session.delete(usuario_para_excluir)
    db.session.commit()
    flash(f'Usuário "{usuario_nome}" e seu perfil foram deletados.', 'info')
    return redirect(url_for('index'))

# -----------------------------------------------------------------------------
# INICIALIZAÇÃO DA APLICAÇÃO
# -----------------------------------------------------------------------------
if __name__ == '__main__':
    # Cria as tabelas no banco de dados, se não existirem
    with app.app_context():
        db.create_all()
    # Roda a aplicação em modo de debug
    app.run(debug=True,port=5002)
