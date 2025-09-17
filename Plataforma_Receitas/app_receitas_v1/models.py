from app import db

# 1. O "Association Object" para a relação M:M
class ReceitaIngrediente(db.Model):
    __tablename__ = 'receita_ingredientes'
    receita_id = db.Column(db.Integer, db.ForeignKey('receita.id'),
                           primary_key=True)
    ingrediente_id = db.Column(db.Integer, db.ForeignKey('ingrediente.id'),
                               primary_key=True)
    quantidade = db.Column(db.String(50), nullable=False)

    # Relações de volta para Receita e Ingrediente
    ingrediente = db.relationship("Ingrediente",
                                  back_populates="receitas_associadas")
    receita = db.relationship("Receita",
                              back_populates="ingredientes_associados")

# 2. Modelo Chef (O "Um" de One-to-One e One-to-Many)
class Chef(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100), nullable=False)
    
    # Relação 1:1 com PerfilChef
    perfil = db.relationship('PerfilChef', back_populates='chef',
                             uselist=False, cascade="all, delete-orphan")
    
    # Relação 1:M com Receita
    receitas = db.relationship('Receita', back_populates='chef')

# 3. Modelo PerfilChef (O outro "Um" de One-to-One)
class PerfilChef(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    especialidade = db.Column(db.String(100))
    anos_experiencia = db.Column(db.Integer)
    chef_id = db.Column(db.Integer, db.ForeignKey('chef.id'), 
                        nullable=False, unique=True)
    
    chef = db.relationship('Chef', back_populates='perfil')

# 4. Modelo Receita (O "Muitos" de One-to-Many e parte do M:M)
class Receita(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    titulo = db.Column(db.String(200), nullable=False)
    instrucoes = db.Column(db.Text, nullable=False)
    chef_id = db.Column(db.Integer, db.ForeignKey('chef.id'), nullable=False)

    chef = db.relationship('Chef', back_populates='receitas')

    # Relação com o "Association Object"
    ingredientes_associados = \
        db.relationship('ReceitaIngrediente', 
                        back_populates='receita', cascade="all, delete-orphan")

# 5. Modelo Ingrediente (A outra parte do M:M)
class Ingrediente(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100), nullable=False, unique=True)

    receitas_associadas = \
        db.relationship('ReceitaIngrediente',
                        back_populates='ingrediente', cascade="all, delete-orphan")
