import os
import pyotp
import qrcode
import base64
from io import BytesIO
from flask import Flask, render_template, request, redirect, url_for, session, flash
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
from flask_bcrypt import Bcrypt
from flask_mail import Mail, Message
from database import db
from sqlalchemy import or_

# Cria a instância da aplicação Flask
app = Flask(__name__)

# --- Configurações da Aplicação ---
basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SECRET_KEY'] = 'uma-chave-secreta-muito-dificil-de-adivinhar'
app.config['SQLALCHEMY_DATABASE_URI'] = \
    'sqlite:///' + os.path.join(basedir, 'instance', 'receitas.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Configurações do Flask-Mail (use variáveis de ambiente em produção!)
app.config['MAIL_SERVER'] = 'smtp.googlemail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = 'bendlin@gmail.com' # Coloque seu e-mail
app.config['MAIL_PASSWORD'] = 'udvgcbsxnefuliqe' # Use uma "Senha de App" do Google

mail = Mail(app)

instance_path = os.path.join(basedir, 'instance')
if not os.path.exists(instance_path):
    os.makedirs(instance_path)

# --- Inicialização das Extensões ---
db.init_app(app)
bcrypt = Bcrypt(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'
login_manager.login_message = "Por favor, faça login para acessar esta página."
login_manager.login_message_category = "info"

# --- Importações Pós-Inicialização ---
from models import Usuario, Chef, Receita, Ingrediente, ReceitaIngrediente, Categoria, receita_categorias
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
    # ... (código existente sem alterações)
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        novo_usuario = Usuario(email=form.email.data, password_hash=hashed_password)
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

# ROTA MODIFICADA: Login
@app.route("/login", methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = LoginForm()
    if form.validate_on_submit():
        user = Usuario.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password_hash, form.password.data):
            login_user(user)
            # A GRANDE MUDANÇA: Verifica se o 2FA está ativo
            if user.has_2fa_enabled:
                # Se estiver, redireciona para a página de verificação do 2FA
                return redirect(url_for('verify_2fa'))
            else:
                # Se não, o login está completo
                return redirect(url_for('index'))
        else:
            flash('Login inválido. Verifique seu e-mail e senha.', 'danger')
    return render_template('login.html', title='Login', form=form)

@app.route("/logout")
def logout():
    logout_user()
    session.pop('2fa_authenticated', None) # Limpa a flag do 2FA
    return redirect(url_for('index'))

# ROTA PROTEGIDA COM VERIFICAÇÃO 2FA
@app.route('/receita/nova', methods=['GET', 'POST'])
@login_required
def criar_receita():
    # Adicionamos uma verificação extra da sessão 2FA
    if current_user.has_2fa_enabled and not session.get('2fa_authenticated'):
        return redirect(url_for('verify_2fa'))
    
    if not current_user.chef:
        return "Apenas usuários com perfil de chef podem criar receitas.", 403

    if request.method == 'POST':
        # ... (código existente sem alterações)
        titulo = request.form['titulo']
        instrucoes = request.form['instrucoes']
        nova_receita = Receita(titulo=titulo, instrucoes=instrucoes, chef_id=current_user.chef.id)

        categorias_str = request.form['categorias_str']
        nomes_categorias = [nome.strip().capitalize() for nome in categorias_str.split(',') if nome.strip()]
        
        for nome_cat in nomes_categorias:
            categoria = Categoria.query.filter_by(nome=nome_cat).first()
            if not categoria:
                categoria = Categoria(nome=nome_cat)
                db.session.add(categoria)
            nova_receita.categorias.append(categoria)
        
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
    # ... (código existente sem alterações)
    chef = Chef.query.get_or_404(chef_id)
    return render_template('detalhes_chef.html', chef=chef)

# --- NOVAS ROTAS PARA 2FA ---

@app.route('/conta')
@login_required
def conta():
    # Adicionamos uma verificação extra da sessão 2FA
    if current_user.has_2fa_enabled and not session.get('2fa_authenticated'):
        return redirect(url_for('verify_2fa'))
    return render_template('conta.html')

@app.route('/2fa/setup')
@login_required
def setup_2fa():
    if not current_user.otp_secret:
        current_user.otp_secret = pyotp.random_base32()
        db.session.commit()

    uri = pyotp.totp.TOTP(current_user.otp_secret).provisioning_uri(
        name=current_user.email,
        issuer_name="Plataforma de Receitas"
    )
    
    img = qrcode.make(uri)
    buffered = BytesIO()
    img.save(buffered, format="PNG")
    qr_code_data = base64.b64encode(buffered.getvalue()).decode()

    return render_template('setup_2fa.html', secret=current_user.otp_secret, qr_code_data=qr_code_data)

# ROTA MODIFICADA: verify_2fa com feedback
@app.route('/2fa/verify', methods=['GET', 'POST'])
@login_required
def verify_2fa():
    if request.method == 'POST':
        token = request.form.get('token')
        totp = pyotp.TOTP(current_user.otp_secret)
        if totp.verify(token):
            # Se o token for válido e o 2FA não estiver habilitado, habilita-o agora
            if not current_user.has_2fa_enabled:
                current_user.has_2fa_enabled = True
                db.session.commit()
            
            # Marca na sessão que o 2FA foi verificado
            session['2fa_authenticated'] = True
            return redirect(url_for('index'))
        else:
            flash('Código inválido ou expirado. Por favor, tente novamente.', 'danger')
    
    return render_template('verify_2fa.html')

@app.route('/2fa/disable', methods=['POST'])
@login_required
def disable_2fa():
    current_user.has_2fa_enabled = False
    current_user.otp_secret = None
    session.pop('2fa_authenticated', None)
    db.session.commit()
    return redirect(url_for('conta'))


@app.route('/dashboard')
@login_required # Apenas usuários logados podem ver
def dashboard():
    # Proteção 2FA
    if current_user.has_2fa_enabled and not session.get('2fa_authenticated'):
        return redirect(url_for('verify_2fa'))

    # Consultas para estatísticas simples
    total_receitas = Receita.query.count()
    total_chefs = Chef.query.count()

    # Consulta para os dados do gráfico (Receitas por Chef)
    chefs_com_receitas = db.session.query(
        Chef.nome, 
        db.func.count(Receita.id).label('total')
    ).join(Receita).group_by(Chef.nome).order_by(db.desc('total')).all()
    
    # Prepara os dados para o JavaScript
    labels_grafico = [item[0] for item in chefs_com_receitas]
    dados_grafico = [item[1] for item in chefs_com_receitas]

    return render_template(
        'dashboard.html', 
        total_receitas=total_receitas,
        total_chefs=total_chefs,
        labels_grafico=labels_grafico,
        dados_grafico=dados_grafico
    )

@app.route('/receita/<int:receita_id>')
def detalhes_receita(receita_id):
    receita = Receita.query.get_or_404(receita_id)
    return render_template('detalhes_receita.html', receita=receita)

@app.route('/receita/<int:receita_id>/enviar', methods=['POST'])
@login_required
def enviar_receita(receita_id):
    receita = Receita.query.get_or_404(receita_id)
    destinatario = request.form['email_destinatario']

    if destinatario:
        try:
            msg = Message(
                subject=f"Receita: {receita.titulo}",
                sender=app.config['MAIL_USERNAME'],
                recipients=[destinatario]
            )
            msg.html = render_template('email_receita.html', receita=receita)
            mail.send(msg)
            flash('Receita enviada com sucesso!', 'info')
        except Exception as e:
            flash(f'Ocorreu um erro ao enviar o e-mail: {e}', 'danger')

    return redirect(url_for('detalhes_receita', receita_id=receita_id))

@app.route('/categoria/<int:categoria_id>')
def receitas_por_categoria(categoria_id):
    categoria = Categoria.query.get_or_404(categoria_id)
    # Acessamos as receitas através do backref que definimos no modelo
    receitas = categoria.receitas.all()
    return render_template('receitas_por_categoria.html', categoria=categoria, receitas=receitas)

@app.route('/busca')
def busca():
    query = request.args.get('q')
    resultados = []
    
    if query:
        # Prepara o termo de busca para usar com o operador LIKE
        search_term = f"%{query}%"
        
        # Busca por título da receita OU por nome do ingrediente
        resultados = Receita.query.filter(
            or_(
                Receita.titulo.ilike(search_term),
                Receita.ingredientes_associados.any(
                    ReceitaIngrediente.ingrediente.has(Ingrediente.nome.ilike(search_term))
                )
            )
        ).distinct().all()

    return render_template('busca.html', query=query, resultados=resultados)

@app.route('/receita/<int:receita_id>/editar', methods=['GET', 'POST'])
@login_required
def editar_receita(receita_id):
    receita = Receita.query.get_or_404(receita_id)

    # --- LÓGICA DE AUTORIZAÇÃO ---
    if receita.chef != current_user.chef:
        flash('Você não tem permissão para editar esta receita.', 'danger')
        return redirect(url_for('detalhes_receita', receita_id=receita.id))

    if request.method == 'POST':
        # Atualiza os campos básicos
        receita.titulo = request.form['titulo']
        receita.instrucoes = request.form['instrucoes']

        # Lógica para atualizar categorias (apaga as antigas e adiciona as novas)
        receita.categorias.clear()
        categorias_str = request.form['categorias_str']
        nomes_categorias = [nome.strip().capitalize() for nome in categorias_str.split(',') if nome.strip()]
        for nome_cat in nomes_categorias:
            categoria = Categoria.query.filter_by(nome=nome_cat).first()
            if not categoria:
                categoria = Categoria(nome=nome_cat)
                db.session.add(categoria)
            receita.categorias.append(categoria)
        
        # (Opcional) A edição de ingredientes pode ser complexa. Aqui, mantemos os originais.
        # Uma implementação completa poderia apagar e recriar as associações.
        
        db.session.commit()
        flash('Receita atualizada com sucesso!', 'success')
        return redirect(url_for('detalhes_receita', receita_id=receita.id))

    # Prepara os dados para exibir no formulário (método GET)
    categorias_atuais = ", ".join([cat.nome for cat in receita.categorias])
    return render_template('editar_receita.html', receita=receita, categorias_atuais=categorias_atuais)

@app.route('/receita/<int:receita_id>/excluir', methods=['POST'])
@login_required
def excluir_receita(receita_id):
    receita = Receita.query.get_or_404(receita_id)
    
    # A mesma lógica de autorização
    if receita.chef != current_user.chef:
        flash('Você não tem permissão para excluir esta receita.', 'danger')
        return redirect(url_for('detalhes_receita', receita_id=receita.id))
    
    db.session.delete(receita)
    db.session.commit()
    flash('Receita excluída com sucesso!', 'success')
    return redirect(url_for('index'))


# --- Comandos CLI ---
@app.cli.command('init-db')
def init_db_command():
    with app.app_context():
        db.drop_all()
        db.create_all()
        print('Banco de dados (vazio) inicializado!')

if __name__ == '__main__':
    app.run(debug=True)