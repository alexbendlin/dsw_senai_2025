from database import db
from flask_login import UserMixin

# Modelo de Associação para a relação M:M (não muda)
class ReceitaIngrediente(db.Model):
    __tablename__ = 'receita_ingredientes'
    receita_id = db.Column(db.Integer, db.ForeignKey('receita.id'), primary_key=True)
    ingrediente_id = db.Column(db.Integer, db.ForeignKey('ingrediente.id'), primary_key=True)
    quantidade = db.Column(db.String(50), nullable=False)

    ingrediente = db.relationship("Ingrediente", back_populates="receitas_associadas")
    receita = db.relationship("Receita", back_populates="ingredientes_associados")

# NOVO MODELO: Usuario (para autenticação)
class Usuario(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(128))

    # Relação 1:1 com Chef -> Um usuário pode ter um perfil de chef
    chef = db.relationship('Chef', back_populates='usuario', uselist=False, cascade="all, delete-orphan")

# MODELO AJUSTADO: Chef (agora é um perfil)
class Chef(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100), nullable=False)
    especialidade = db.Column(db.String(100))
    
    # Chave estrangeira para conectar ao usuário
    usuario_id = db.Column(db.Integer, db.ForeignKey('usuario.id'), nullable=False, unique=True)
    
    # Relação de volta para Usuario
    usuario = db.relationship('Usuario', back_populates='chef')
    
    # Relação 1:M com Receita (não muda)
    receitas = db.relationship('Receita', back_populates='chef')

# MODELO AJUSTADO: Receita
class Receita(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    titulo = db.Column(db.String(200), nullable=False)
    instrucoes = db.Column(db.Text, nullable=False)
    chef_id = db.Column(db.Integer, db.ForeignKey('chef.id'), nullable=False) # Continua apontando para Chef
    
    chef = db.relationship('Chef', back_populates='receitas')
    
    ingredientes_associados = db.relationship('ReceitaIngrediente', back_populates='receita', cascade="all, delete-orphan")

# Modelo Ingrediente (não muda)
class Ingrediente(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100), nullable=False, unique=True)
    
    receitas_associadas = db.relationship('ReceitaIngrediente', back_populates='ingrediente', cascade="all, delete-orphan")
