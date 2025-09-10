import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy

# Inicializa a aplicação Flask
app = Flask(__name__)

# Configurações do banco de dados (SQLite para simplicidade)
basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'meubanco.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Inicializa a extensão SQLAlchemy
db = SQLAlchemy(app)

# Definição do Modelo (Tabela) de Usuário
class Usuario(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)

    def __repr__(self):
        return f'<Usuario {self.nome}>'

@app.route('/')
def index():
    return "Aplicação Flask com SQLAlchemy!"

if __name__ == '__main__':
    app.run(debug=True, port=5002)
