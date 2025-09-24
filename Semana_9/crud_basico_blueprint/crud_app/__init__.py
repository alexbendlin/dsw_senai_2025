import os
from flask import Flask
from .models import db

def create_app():
    # Cria a instância da aplicação Flask
    app = Flask(__name__)

    # --- CONFIGURAÇÕES ---
    basedir = os.path.abspath(os.path.dirname(__file__))
    # Aponta para o diretório raiz do projeto
    project_root = os.path.dirname(basedir)
    
    # Configura a chave secreta e o banco de dados
    app.config['SECRET_KEY'] = 'uma_chave_secreta_muito_segura'
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(project_root, 'database.db')
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    # Inicializa o banco de dados com a aplicação
    db.init_app(app)

    # --- REGISTRO DO BLUEPRINT ---
    # Importa o blueprint de rotas
    from .routes import main as main_blueprint
    # Registra o blueprint na aplicação
    app.register_blueprint(main_blueprint)
    
    # Cria o banco de dados se ele não existir
    with app.app_context():
        db.create_all()

    return app