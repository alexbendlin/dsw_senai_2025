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
app.config['SECRET_KEY'] = 'uma-chave-secreta-bem-segura'
basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'database.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Inicializa a extensão SQLAlchemy
db = SQLAlchemy(app)


# -----------------------------------------------------------------------------
# DEFINIÇÃO DOS MODELOS (TABELAS DO BANCO DE DADOS)
# -----------------------------------------------------------------------------

# --- TABELA DE ASSOCIAÇÃO (Helper Table) ---
# Esta é a peça central do relacionamento Muitos-para-Muitos.
# Não é uma classe de modelo, mas uma tabela auxiliar que o SQLAlchemy usará.
# Ela contém apenas as chaves estrangeiras para as tabelas que está conectando.
publicacoes_etiquetas = db.Table('publicacoes_etiquetas',
    db.Column('publicacao_id', db.Integer, db.ForeignKey('publicacao.id'), primary_key=True),
    db.Column('etiqueta_id', db.Integer, db.ForeignKey('etiqueta.id'), primary_key=True)
)

# --- Modelo Usuario (Usuário) ---
class Usuario(db.Model):
    __tablename__ = 'usuario'
    id = db.Column(db.Integer, primary_key=True)
    usuario_nome = db.Column(db.String(80), unique=True, nullable=False)
    publicacoes = db.relationship('Publicacao', back_populates='autor', cascade='all, delete-orphan')

    def __repr__(self):
        return f'<Usuário {self.usuario_nome}>'

# --- Modelo Publicacao (Publicação) ---
class Publicacao(db.Model):
    __tablename__ = 'publicacao'
    id = db.Column(db.Integer, primary_key=True)
    titulo = db.Column(db.String(120), nullable=False)
    conteudo = db.Column(db.Text, nullable=True)
    usuario_id = db.Column(db.Integer, db.ForeignKey('usuario.id'), nullable=False)
    autor = db.relationship('Usuario', back_populates='publicacoes')
    
    # --- RELACIONAMENTO MUITOS-PARA-MUITOS com Etiqueta ---
    # 1. 'Etiqueta': A classe do modelo com a qual se relaciona.
    # 2. secondary=publicacoes_etiquetas: Este é o parâmetro CRÍTICO. Ele diz ao SQLAlchemy
    #    para usar nossa tabela de associação 'publicacoes_etiquetas' para gerenciar este relacionamento.
    # 3. back_populates='publicacoes': Cria a referência de volta no modelo 'Etiqueta'.
    etiquetas = db.relationship('Etiqueta', secondary=publicacoes_etiquetas, back_populates='publicacoes', lazy='dynamic')

    def __repr__(self):
        return f'<Publicação {self.titulo}>'

# --- Modelo Etiqueta ---
class Etiqueta(db.Model):
    __tablename__ = 'etiqueta'
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(50), unique=True, nullable=False)
    
    # Relação de volta para o modelo Publicacao
    publicacoes = db.relationship('Publicacao', secondary=publicacoes_etiquetas, back_populates='etiquetas', lazy='dynamic')

    def __repr__(self):
        return f'<Etiqueta {self.nome}>'

# -----------------------------------------------------------------------------
# DEFINIÇÃO DAS ROTAS E LÓGICA DA APLICAÇÃO
# -----------------------------------------------------------------------------

@app.route('/')
def index():
    usuarios = Usuario.query.all()
    etiquetas = Etiqueta.query.all()
    return render_template('index.html', usuarios=usuarios, etiquetas=etiquetas)

@app.route('/adicionar_usuario', methods=['POST'])
def adicionar_usuario():
    usuario_nome = request.form.get('usuario_nome')
    if usuario_nome:
        usuario_existente = Usuario.query.filter_by(usuario_nome=usuario_nome).first()
        if not usuario_existente:
            novo_usuario = Usuario(usuario_nome=usuario_nome)
            db.session.add(novo_usuario)
            db.session.commit()
            flash(f'Usuário "{usuario_nome}" adicionado com sucesso!', 'success')
        else:
            flash(f'Usuário "{usuario_nome}" já existe.', 'danger')
    return redirect(url_for('index'))

@app.route('/adicionar_perfil', methods=['POST'])
def adicionar_perfil():
    usuario_id = request.form.get('usuario_id')
    titulo = request.form.get('titulo')
    conteudo = request.form.get('conteudo')
    sequencia_etiquetas = request.form.get('etiquetas')

    if usuario_id and titulo:
        usuario = Usuario.query.get(usuario_id)
        if usuario:
            nova_publicacao = Publicacao(titulo=titulo, conteudo=conteudo, autor=usuario)
            
            # Lógica para processar as etiquetas
            if sequencia_etiquetas:
                nomes_etiquetas = [nome.strip() for nome in sequencia_etiquetas.split(',') if nome.strip()]
                for etiqueta_nome in nomes_etiquetas:
                    # Verifica se a etiqueta já existe
                    etiqueta = Etiqueta.query.filter_by(nome=etiqueta_nome).first()
                    if not etiqueta:
                        # Se não existir, cria uma nova
                        etiqueta = Etiqueta(nome=etiqueta_nome)
                        db.session.add(etiqueta)
                    # Associa a etiqueta à publicação
                    nova_publicacao.etiquetas.append(etiqueta)

            db.session.add(nova_publicacao)
            db.session.commit()
            flash(f'Publicação "{titulo}" adicionada para {usuario.usuario_nome}!', 'success')
        else:
            flash(f'Usuário não encontrado.', 'danger')
    return redirect(url_for('index'))

@app.route('/excluir_usuario/<int:usuario_id>', methods=['POST'])
def excluir_usuario(usuario_id):
    usuario_para_excluir = Usuario.query.get_or_44(usuario_id)
    usuario_nome = usuario_para_excluir.usuario_nome
    db.session.delete(usuario_para_excluir)
    db.session.commit()
    flash(f'Usuário "{usuario_nome}" e todas as suas publicações foram deletados.', 'info')
    return redirect(url_for('index'))


# -----------------------------------------------------------------------------
# INICIALIZAÇÃO DA APLICAÇÃO
# -----------------------------------------------------------------------------
if __name__ == '__main__':
    with app.app_context():
        # Antes de rodar, para garantir que as tabelas antigas sejam removidas
        # e as novas sejam criadas, você pode deletar o arquivo 'database.db'
        db.create_all()
    app.run(debug=True,port=5002)
