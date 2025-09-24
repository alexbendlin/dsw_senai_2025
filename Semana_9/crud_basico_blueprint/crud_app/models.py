from flask_sqlalchemy import SQLAlchemy

# Criamos a instância do SQLAlchemy fora da aplicação para evitar importações circulares
db = SQLAlchemy()

class Usuario(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)

    def __repr__(self):
        return f'<Usuario {self.nome}>'