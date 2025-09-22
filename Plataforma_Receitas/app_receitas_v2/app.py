import os
from flask import Flask, render_template, request, redirect, url_for
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
from flask_bcrypt import Bcrypt
from database import db

# Cria a instância da aplicação Flask
app = Flask(__name__)

# --- Configurações da Aplicação ---
basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SECRET_KEY'] = 'uma-chave-secreta-muito-dificil-de-adivinhar'
app.config['SQLALCHEMY_DATABASE_URI'] = \
    'sqlite:///' + os.path.join(basedir, 'instance', 'receitas.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Cria a pasta 'instance' se ela não existir
instance_path = os.path.join(basedir, 'instance')
if not os.path.exists(instance_path):
    os.makedirs(instance_path)

# --- Inicialização das Extensões ---
db.init_app(app)
bcrypt = Bcrypt(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login' # Redireciona para a rota 'login' se o acesso for negado
login_manager.login_message = "Por favor, faça login para acessar esta página."
login_manager.login_message_category = "info"

# --- Importações Pós-Inicialização ---
# Importa modelos e formulários DEPOIS da configuração para evitar importação circular
from models import Usuario, Chef, Receita, Ingrediente, ReceitaIngrediente
from forms import RegistrationForm, LoginForm

# --- Configuração do Flask-Login ---
@login_manager.user_loader
def load_user(user_id):
    return Usuario.query.get(int(user_id))

# --- Rotas ---

@app.route('/')
def index():
    receitas = Receita.query.all()
    return render_template('index.html', receitas=receitas)

@app.route("/cadastro", methods=['GET', 'POST'])
def cadastro():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        
        # 1. Cria o objeto Usuario
        novo_usuario = Usuario(email=form.email.data, password_hash=hashed_password)
        
        # 2. Cria o objeto Chef e o associa ao novo usuário
        novo_chef = Chef(
            nome=form.nome.data, 
            especialidade=form.especialidade.data, 
            usuario=novo_usuario
        )
        
        db.session.add(novo_usuario)
        db.session.add(novo_chef)
        db.session.commit()
        
        return redirect(url_for('login'))
    return render_template('cadastro.html', title='Cadastro', form=form)

@app.route("/login", methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = LoginForm()
    if form.validate_on_submit():
        user = Usuario.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password_hash, form.password.data):
            login_user(user)
            return redirect(url_for('index'))
    return render_template('login.html', title='Login', form=form)

@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('index'))

@app.route('/receita/nova', methods=['GET', 'POST'])
@login_required # Protege a rota!
def criar_receita():
    if not current_user.chef:
        return "Apenas usuários com perfil de chef podem criar receitas.", 403

    if request.method == 'POST':
        titulo = request.form['titulo']
        instrucoes = request.form['instrucoes']
        # O autor da receita é o chef associado ao usuário logado
        nova_receita = Receita(titulo=titulo, instrucoes=instrucoes, chef_id=current_user.chef.id)
        db.session.add(nova_receita)
        
        ingredientes_str = request.form['ingredientes']
        pares_ingredientes = [par.strip() for par in ingredientes_str.split(',') if par.strip()]
        for par in pares_ingredientes:
            if ':' in par:
                nome, qtd = par.split(':', 1)
                nome_ingrediente = nome.strip().lower()
                quantidade = qtd.strip()
                ingrediente = Ingrediente.query.filter_by(nome=nome_ingrediente).first()
                if not ingrediente:
                    ingrediente = Ingrediente(nome=nome_ingrediente)
                    db.session.add(ingrediente)
                associacao = ReceitaIngrediente(receita=nova_receita, ingrediente=ingrediente, quantidade=quantidade)
                db.session.add(associacao)

        db.session.commit()
        return redirect(url_for('index'))
    
    return render_template('criar_receita.html')

@app.route('/chef/<int:chef_id>')
def detalhes_chef(chef_id):
    chef = Chef.query.get_or_404(chef_id)
    return render_template('detalhes_chef.html', chef=chef)


# --- Comandos CLI ---
@app.cli.command('init-db')
def init_db_command():
    """Cria as tabelas e popula com dados de exemplo."""
    with app.app_context():
        db.drop_all()
        db.create_all()

        # Criar Usuário 1
        hashed_pass1 = bcrypt.generate_password_hash('senha123').decode('utf-8')
        user1 = Usuario(email='ana@example.com', password_hash=hashed_pass1)
        
        # Criar Chef 1 e associar ao Usuário 1
        chef1 = Chef(nome='Ana Maria', especialidade='Culinária Brasileira', usuario=user1)
        
        db.session.add(user1)
        db.session.add(chef1)
        db.session.commit() # Commit para garantir que o chef1 tenha um ID
        
        # Criar Ingredientes
        ingredientes = {
            'tomate': Ingrediente(nome='tomate'), 'cebola': Ingrediente(nome='cebola')
        }
        db.session.add_all(list(ingredientes.values()))
        db.session.commit()

        # Criar Receita
        receita1 = Receita(titulo='Molho de Tomate Clássico', instrucoes='Refogue tudo.', chef_id=chef1.id)
        db.session.add(receita1)
        db.session.commit()

        # Criar Associações
        assoc1 = ReceitaIngrediente(receita_id=receita1.id, ingrediente_id=ingredientes['tomate'].id, quantidade='5 unidades')
        db.session.add(assoc1)

        db.session.commit()
        print('Banco de dados com sistema de usuários inicializado!')

if __name__ == '__main__':
    app.run(debug=True, port=5002)
