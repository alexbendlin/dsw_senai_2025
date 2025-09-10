import os
from flask import Flask, render_template_string, request, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, SelectField, TextAreaField, SelectMultipleField
from wtforms.validators import DataRequired

# --- Configuração da Aplicação ---
app = Flask(__name__)

# Configura o caminho do banco de dados SQLite e a chave secreta para os formulários
basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'relacionamentos.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'uma-chave-secreta-super-segura-para-csrf'

db = SQLAlchemy(app)


# --- Modelos (Estrutura do Banco de Dados) ---

# Tabela de associação para a relação Muitos-para-Muitos
estudante_turma_association = db.Table('estudante_turma',
    db.Column('estudante_id', db.Integer, db.ForeignKey('estudante.id'), primary_key=True),
    db.Column('turma_id', db.Integer, db.ForeignKey('turma.id'), primary_key=True)
)

# 1. Relação Um-para-Um: Usuario e Perfil
class Usuario(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100), unique=True, nullable=False)
    # 'uselist=False' define a relação como um-para-um
    perfil = db.relationship('Perfil', backref='usuario', uselist=False, cascade="all, delete-orphan")

    def __repr__(self):
        return f'<Usuario {self.nome}>'

class Perfil(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    bio = db.Column(db.String(200))
    usuario_id = db.Column(db.Integer, db.ForeignKey('usuario.id'), nullable=False)

    def __repr__(self):
        return f'<Perfil de {self.usuario.nome}>'

# 2. Relação Um-para-Muitos: Autor e Livro
class Autor(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100), unique=True, nullable=False)
    # Um autor pode ter vários livros
    livros = db.relationship('Livro', backref='autor', lazy=True, cascade="all, delete-orphan")

    def __repr__(self):
        return f'<Autor {self.nome}>'

class Livro(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    titulo = db.Column(db.String(100), nullable=False)
    autor_id = db.Column(db.Integer, db.ForeignKey('autor.id'), nullable=False)

    def __repr__(self):
        return f'<Livro {self.titulo}>'

# 3. Relação Muitos-para-Muitos: Estudante e Turma
class Estudante(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100), unique=True, nullable=False)

    def __repr__(self):
        return f'<Estudante {self.nome}>'

class Turma(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100), unique=True, nullable=False)
    # Uma turma pode ter vários estudantes, e um estudante pode estar em várias turmas
    estudantes = db.relationship('Estudante', secondary=estudante_turma_association, backref='turmas', lazy='dynamic')

    def __repr__(self):
        return f'<Turma {self.nome}>'


# --- Formulários (WTForms) ---
class UsuarioPerfilForm(FlaskForm):
    nome_usuario = StringField('Nome do Usuário', validators=[DataRequired()])
    bio_perfil = TextAreaField('Biografia do Perfil')
    submit = SubmitField('Adicionar Usuário e Perfil')

class AutorForm(FlaskForm):
    nome = StringField('Nome do Autor', validators=[DataRequired()])
    submit = SubmitField('Adicionar Autor')

class LivroForm(FlaskForm):
    titulo = StringField('Título do Livro', validators=[DataRequired()])
    autor = SelectField('Autor', coerce=int, validators=[DataRequired()])
    submit = SubmitField('Adicionar Livro')

class EstudanteForm(FlaskForm):
    nome = StringField('Nome do Estudante', validators=[DataRequired()])
    submit = SubmitField('Adicionar Estudante')

class TurmaForm(FlaskForm):
    nome = StringField('Nome da Turma', validators=[DataRequired()])
    submit = SubmitField('Adicionar Turma')
    
class AssociarEstudanteTurmaForm(FlaskForm):
    turma = SelectField('Selecione a Turma', coerce=int, validators=[DataRequired()])
    estudantes = SelectMultipleField('Selecione os Estudantes', coerce=int, validators=[DataRequired()])
    submit = SubmitField('Associar')


# --- Templates HTML (embutidos como strings) ---

# Template base com estilos CSS para uma aparência mais limpa
HTML_BASE_TEMPLATE = """
<!DOCTYPE html>
<html lang="pt-BR">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Exemplo de Relacionamentos com Flask-SQLAlchemy</title>
    <style>
        body { font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, "Helvetica Neue", Arial, sans-serif; line-height: 1.6; color: #333; background-color: #f4f4f4; margin: 0; padding: 20px; }
        .container { max-width: 1000px; margin: auto; background: #fff; padding: 20px; border-radius: 8px; box-shadow: 0 2px 10px rgba(0,0,0,0.1); }
        h1, h2 { color: #0056b3; }
        h1 { text-align: center; }
        h2 { border-bottom: 2px solid #0056b3; padding-bottom: 10px; margin-top: 40px; }
        ul { list-style-type: none; padding: 0; }
        li { background: #e9ecef; margin-bottom: 8px; padding: 10px; border-radius: 4px; display: flex; justify-content: space-between; align-items: center; }
        .actions { display: flex; gap: 10px; }
        a.button, button, input[type=submit] { background-color: #007bff; color: white; padding: 10px 15px; border: none; border-radius: 4px; text-decoration: none; cursor: pointer; font-size: 1em; }
        a.button.add { background-color: #28a745; }
        a.button:hover, button:hover, input[type=submit]:hover { opacity: 0.9; }
        form { margin-top: 20px; background-color: #fdfdfd; padding: 20px; border-radius: 5px; border: 1px solid #ddd; }
        label { display: block; margin-bottom: 5px; font-weight: bold; }
        input[type=text], textarea, select { width: 100%; padding: 8px; margin-bottom: 10px; border-radius: 4px; border: 1px solid #ccc; box-sizing: border-box; }
        .flash { padding: 15px; margin-bottom: 20px; border: 1px solid transparent; border-radius: 4px; text-align: center; }
        .flash.success { color: #155724; background-color: #d4edda; border-color: #c3e6cb; }
        .grid { display: grid; grid-template-columns: repeat(auto-fit, minmax(300px, 1fr)); gap: 20px; }
        .card { padding: 15px; border: 1px solid #ddd; border-radius: 5px; }
    </style>
</head>
<body>
    <div class="container">
        {% with messages = get_flashed_messages(with_categories=true) %}
            {% if messages %}
                {% for category, message in messages %}
                    <div class="flash {{ category }}">{{ message }}</div>
                {% endfor %}
            {% endif %}
        {% endwith %}
        {% block content %}{% endblock %}
    </div>
</body>
</html>
"""

# Conteúdo da página principal a ser injetado no template base
INDEX_CONTENT = """
    <h1>Gerenciador de Relacionamentos</h1>
    
    <!-- Seção 1: Um-para-Um -->
    <section>
        <h2>1. Um-para-Um (Usuário & Perfil)</h2>
        <a href="{{ url_for('add_usuario_perfil') }}" class="button add">Adicionar Usuário</a>
        <ul>
            {% for usuario in usuarios %}
                <li>
                    <span><strong>Usuário:</strong> {{ usuario.nome }} &rarr; <strong>Bio:</strong> {{ usuario.perfil.bio or 'N/A' }}</span>
                </li>
            {% else %}
                <li>Nenhum usuário cadastrado.</li>
            {% endfor %}
        </ul>
    </section>

    <!-- Seção 2: Um-para-Muitos -->
    <section>
        <h2>2. Um-para-Muitos (Autor & Livros)</h2>
        <div class="actions">
            <a href="{{ url_for('add_autor') }}" class="button add">Adicionar Autor</a>
            <a href="{{ url_for('add_livro') }}" class="button add">Adicionar Livro</a>
        </div>
        <ul>
            {% for autor in autores %}
                <li>
                   <span><strong>Autor:</strong> {{ autor.nome }}<br>
                    <small><strong>Livros:</strong> {{ autor.livros|map(attribute='titulo')|join(', ') or 'Nenhum livro cadastrado' }}</small>
                   </span>
                </li>
            {% else %}
                <li>Nenhum autor cadastrado.</li>
            {% endfor %}
        </ul>
    </section>

    <!-- Seção 3: Muitos-para-Muitos -->
    <section>
        <h2>3. Muitos-para-Muitos (Estudante & Turmas)</h2>
        <div class="actions">
            <a href="{{ url_for('add_estudante') }}" class="button add">Adicionar Estudante</a>
            <a href="{{ url_for('add_turma') }}" class="button add">Adicionar Turma</a>
            <a href="{{ url_for('associar_estudante_turma') }}" class="button">Associar Estudante a Turma</a>
        </div>
        <div class="grid">
             <div class="card">
                <h3>Turmas e seus Estudantes</h3>
                <ul>
                {% for turma in turmas %}
                    <li><span><strong>Turma:</strong> {{ turma.nome }}<br>
                        <small><strong>Estudantes:</strong> {{ turma.estudantes.all()|map(attribute='nome')|join(', ') or 'Nenhum estudante na turma' }}</small>
                    </span></li>
                {% else %}
                    <li>Nenhuma turma cadastrada.</li>
                {% endfor %}
                </ul>
            </div>
            <div class="card">
                <h3>Estudantes e suas Turmas</h3>
                <ul>
                {% for estudante in estudantes %}
                     <li><span><strong>Estudante:</strong> {{ estudante.nome }}<br>
                        <small><strong>Turmas:</strong> {{ estudante.turmas|map(attribute='nome')|join(', ') or 'Não está em nenhuma turma' }}</small>
                    </span></li>
                {% else %}
                    <li>Nenhum estudante cadastrado.</li>
                {% endfor %}
                </ul>
            </div>
        </div>
    </section>
"""

# Conteúdo genérico para formulários a ser injetado no template base
FORM_CONTENT = """
    <h2>{{ title }}</h2>
    <form method="POST" action="">
        {{ form.hidden_tag() }}
        
        {% for field in form if field.widget.input_type != 'hidden' and field.type != 'SubmitField' %}
            <div>
                {{ field.label }}<br>
                {{ field() }}
                {% if field.errors %}
                    <ul class="errors">
                        {% for error in field.errors %}
                            <li>{{ error }}</li>
                        {% endfor %}
                    </ul>
                {% endif %}
            </div>
        {% endfor %}
        
        <div>
            {{ form.submit() }}
        </div>
    </form>
    <br>
    <a href="{{ url_for('index') }}" class="button">Voltar</a>
"""

# --- Rotas e Views (Lógica da Aplicação) ---

@app.route('/')
def index():
    """Página principal que exibe todos os dados."""
    usuarios = Usuario.query.all()
    autores = Autor.query.all()
    estudantes = Estudante.query.all()
    turmas = Turma.query.all()
    full_template = HTML_BASE_TEMPLATE.replace('{% block content %}{% endblock %}', INDEX_CONTENT)
    return render_template_string(
        full_template,
        usuarios=usuarios,
        autores=autores,
        estudantes=estudantes,
        turmas=turmas
    )

@app.route('/add/usuario', methods=['GET', 'POST'])
def add_usuario_perfil():
    """Adiciona um novo usuário e seu perfil (Um-para-Um)."""
    form = UsuarioPerfilForm()
    if form.validate_on_submit():
        novo_usuario = Usuario(nome=form.nome_usuario.data)
        novo_perfil = Perfil(bio=form.bio_perfil.data, usuario=novo_usuario)
        db.session.add(novo_usuario)
        db.session.add(novo_perfil)
        db.session.commit()
        flash('Usuário e Perfil adicionados com sucesso!', 'success')
        return redirect(url_for('index'))
    full_template = HTML_BASE_TEMPLATE.replace('{% block content %}{% endblock %}', FORM_CONTENT)
    return render_template_string(
        full_template,
        title="Adicionar Novo Usuário e Perfil",
        form=form
    )
    
@app.route('/add/autor', methods=['GET', 'POST'])
def add_autor():
    """Adiciona um novo autor."""
    form = AutorForm()
    if form.validate_on_submit():
        novo_autor = Autor(nome=form.nome.data)
        db.session.add(novo_autor)
        db.session.commit()
        flash('Autor adicionado com sucesso!', 'success')
        return redirect(url_for('index'))
    full_template = HTML_BASE_TEMPLATE.replace('{% block content %}{% endblock %}', FORM_CONTENT)
    return render_template_string(
        full_template,
        title="Adicionar Novo Autor",
        form=form
    )

@app.route('/add/livro', methods=['GET', 'POST'])
def add_livro():
    """Adiciona um novo livro e o associa a um autor (Um-para-Muitos)."""
    form = LivroForm()
    # Popula o campo de seleção com os autores existentes
    form.autor.choices = [(a.id, a.nome) for a in Autor.query.order_by('nome').all()]
    if form.validate_on_submit():
        novo_livro = Livro(titulo=form.titulo.data, autor_id=form.autor.data)
        db.session.add(novo_livro)
        db.session.commit()
        flash('Livro adicionado com sucesso!', 'success')
        return redirect(url_for('index'))
    full_template = HTML_BASE_TEMPLATE.replace('{% block content %}{% endblock %}', FORM_CONTENT)
    return render_template_string(
        full_template,
        title="Adicionar Novo Livro",
        form=form
    )
    
@app.route('/add/estudante', methods=['GET', 'POST'])
def add_estudante():
    """Adiciona um novo estudante."""
    form = EstudanteForm()
    if form.validate_on_submit():
        novo_estudante = Estudante(nome=form.nome.data)
        db.session.add(novo_estudante)
        db.session.commit()
        flash('Estudante adicionado com sucesso!', 'success')
        return redirect(url_for('index'))
    full_template = HTML_BASE_TEMPLATE.replace('{% block content %}{% endblock %}', FORM_CONTENT)
    return render_template_string(
        full_template,
        title="Adicionar Novo Estudante",
        form=form
    )
    
@app.route('/add/turma', methods=['GET', 'POST'])
def add_turma():
    """Adiciona uma nova turma."""
    form = TurmaForm()
    if form.validate_on_submit():
        nova_turma = Turma(nome=form.nome.data)
        db.session.add(nova_turma)
        db.session.commit()
        flash('Turma adicionada com sucesso!', 'success')
        return redirect(url_for('index'))
    full_template = HTML_BASE_TEMPLATE.replace('{% block content %}{% endblock %}', FORM_CONTENT)
    return render_template_string(
        full_template,
        title="Adicionar Nova Turma",
        form=form
    )
    
@app.route('/associar', methods=['GET', 'POST'])
def associar_estudante_turma():
    """Associa estudantes a uma turma (Muitos-para-Muitos)."""
    form = AssociarEstudanteTurmaForm()
    form.turma.choices = [(t.id, t.nome) for t in Turma.query.order_by('nome').all()]
    form.estudantes.choices = [(e.id, e.nome) for e in Estudante.query.order_by('nome').all()]
    
    if form.validate_on_submit():
        turma = Turma.query.get(form.turma.data)
        # Limpa associações existentes para esta turma para evitar duplicatas
        turma.estudantes = []
        for estudante_id in form.estudantes.data:
            estudante = Estudante.query.get(estudante_id)
            turma.estudantes.append(estudante)
        db.session.commit()
        flash(f'Estudantes associados à turma {turma.nome} com sucesso!', 'success')
        return redirect(url_for('index'))

    full_template = HTML_BASE_TEMPLATE.replace('{% block content %}{% endblock %}', FORM_CONTENT)
    return render_template_string(
        full_template,
        title="Associar Estudantes a uma Turma",
        form=form
    )

# --- Execução da Aplicação ---
if __name__ == '__main__':
    # O 'with app.app_context()' garante que a aplicação esteja
    # configurada antes de interagir com o banco de dados.
    with app.app_context():
        # Cria todas as tabelas definidas nos modelos.
        # Isso só precisa ser executado uma vez, mas é seguro executar sempre.
        db.create_all()
        print("Banco de dados e tabelas verificados/criados.")

    # Inicia o servidor de desenvolvimento do Flask
    app.run(debug=True)
