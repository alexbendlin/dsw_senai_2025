# -*- coding: utf-8 -*-

import os
from flask import Flask, request, redirect, url_for, render_template_string, flash
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

# --- Tabela de Associação (Muitos-para-Muitos) ---
post_tags = db.Table('post_tags',
    db.Column('post_id', db.Integer, db.ForeignKey('post.id'), primary_key=True),
    db.Column('tag_id', db.Integer, db.ForeignKey('tag.id'), primary_key=True)
)

# --- Modelo User (Usuário) ---
class User(db.Model):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    posts = db.relationship('Post', back_populates='author', cascade='all, delete-orphan')

    def __repr__(self):
        return f'<User {self.username}>'

# --- Modelo Post (Publicação) ---
class Post(db.Model):
    __tablename__ = 'post'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(120), nullable=False)
    content = db.Column(db.Text, nullable=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    author = db.relationship('User', back_populates='posts')
    tags = db.relationship('Tag', secondary=post_tags, back_populates='posts')

    def __repr__(self):
        return f'<Post {self.title}>'

# --- Modelo Tag ---
class Tag(db.Model):
    __tablename__ = 'tag'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), unique=True, nullable=False)
    posts = db.relationship('Post', secondary=post_tags, back_populates='tags')

    def __repr__(self):
        return f'<Tag {self.name}>'

# -----------------------------------------------------------------------------
# DEFINIÇÃO DAS ROTAS E LÓGICA DA APLICAÇÃO (CRUD)
# -----------------------------------------------------------------------------

# --- READ (Ler) ---
# A rota principal exibe todos os dados.
@app.route('/')
def index():
    users = User.query.all()
    tags = Tag.query.all()
    return render_template_string(HTML_TEMPLATE, users=users, tags=tags)

# --- CREATE (Criar) ---
@app.route('/add_user', methods=['POST'])
def add_user():
    username = request.form.get('username')
    if username:
        existing_user = User.query.filter_by(username=username).first()
        if not existing_user:
            new_user = User(username=username)
            db.session.add(new_user)
            db.session.commit()
            flash(f'Usuário "{username}" adicionado com sucesso!', 'success')
        else:
            flash(f'Usuário "{username}" já existe.', 'danger')
    return redirect(url_for('index'))

@app.route('/add_post', methods=['POST'])
def add_post():
    user_id = request.form.get('user_id')
    title = request.form.get('title')
    content = request.form.get('content')
    tags_string = request.form.get('tags')

    if user_id and title:
        user = User.query.get(user_id)
        if user:
            new_post = Post(title=title, content=content, author=user)
            if tags_string:
                tag_names = [name.strip() for name in tags_string.split(',') if name.strip()]
                for tag_name in tag_names:
                    tag = Tag.query.filter_by(name=tag_name).first()
                    if not tag:
                        tag = Tag(name=tag_name)
                        db.session.add(tag)
                    new_post.tags.append(tag)
            db.session.add(new_post)
            db.session.commit()
            flash(f'Publicação "{title}" adicionada para {user.username}!', 'success')
        else:
            flash(f'Usuário não encontrado.', 'danger')
    return redirect(url_for('index'))

# --- UPDATE (Atualizar) ---
@app.route('/edit_post/<int:post_id>', methods=['GET', 'POST'])
def edit_post(post_id):
    post_to_edit = Post.query.get_or_404(post_id)

    if request.method == 'POST':
        # Pega os dados do formulário de edição
        post_to_edit.title = request.form['title']
        post_to_edit.content = request.form['content']
        tags_string = request.form.get('tags')

        # Lógica para atualizar as tags
        post_to_edit.tags.clear() # Remove as associações antigas
        if tags_string:
            tag_names = [name.strip() for name in tags_string.split(',') if name.strip()]
            for tag_name in tag_names:
                tag = Tag.query.filter_by(name=tag_name).first()
                if not tag:
                    tag = Tag(name=tag_name)
                    db.session.add(tag)
                post_to_edit.tags.append(tag)
        
        db.session.commit()
        flash('Publicação atualizada com sucesso!', 'success')
        return redirect(url_for('index'))

    # Se for GET, exibe a página de edição com os dados atuais
    current_tags = ', '.join([tag.name for tag in post_to_edit.tags])
    return render_template_string(EDIT_TEMPLATE, post=post_to_edit, current_tags=current_tags)

# --- DELETE (Deletar) ---
@app.route('/delete_user/<int:user_id>', methods=['POST'])
def delete_user(user_id):
    user_to_delete = User.query.get_or_404(user_id)
    username = user_to_delete.username
    db.session.delete(user_to_delete)
    db.session.commit()
    flash(f'Usuário "{username}" e todas as suas publicações foram deletados.', 'info')
    return redirect(url_for('index'))

@app.route('/delete_post/<int:post_id>', methods=['POST'])
def delete_post(post_id):
    post_to_delete = Post.query.get_or_404(post_id)
    title = post_to_delete.title
    db.session.delete(post_to_delete)
    db.session.commit()
    flash(f'Publicação "{title}" foi deletada.', 'info')
    return redirect(url_for('index'))

# -----------------------------------------------------------------------------
# TEMPLATES HTML
# -----------------------------------------------------------------------------
HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="pt-br">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>CRUD Completo: Flask & SQLAlchemy</title>
    <script src="https://cdn.tailwindcss.com"></script>
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0-beta3/css/all.min.css">
    <style> body { font-family: 'Inter', sans-serif; } @import url('https://rsms.me/inter/inter.css'); </style>
</head>
<body class="bg-slate-100 text-slate-800">
    <div class="container mx-auto p-4 md:p-8">
        
        <header class="text-center mb-10">
            <h1 class="text-4xl font-bold text-slate-900">Aplicação CRUD Completa</h1>
            <p class="text-lg text-slate-600 mt-2">Demonstração de Create, Read, Update e Delete com Flask</p>
        </header>

        <div class="bg-white p-6 rounded-xl shadow-md mb-8 border border-slate-200">
            <h2 class="text-2xl font-semibold mb-4 text-slate-800"><i class="fas fa-tasks text-sky-500 mr-3"></i> Operações CRUD</h2>
            <div class="space-y-2 text-slate-700">
                <p><strong>CREATE:</strong> Use os formulários na coluna da esquerda para criar novos Usuários e Publicações.</p>
                <p><strong>READ:</strong> Os dados de todos os usuários e suas publicações são exibidos na coluna da direita.</p>
                <p><strong>UPDATE:</strong> Clique no botão <i class="fas fa-edit text-yellow-500"></i> "Editar" em qualquer publicação para modificar seus dados.</p>
                <p><strong>DELETE:</strong> Clique no botão <i class="fas fa-trash-alt text-red-500"></i> "Deletar" para remover uma publicação ou um usuário (com suas publicações).</p>
            </div>
        </div>

        <div class="grid grid-cols-1 lg:grid-cols-3 gap-8">
            <div class="lg:col-span-1 space-y-8">
                <div class="bg-white p-6 rounded-xl shadow-md border border-slate-200">
                    <h3 class="text-xl font-semibold mb-4 border-b pb-2">1. Adicionar Usuário</h3>
                    <form action="{{ url_for('add_user') }}" method="POST">
                        <div class="mb-4">
                            <label for="username" class="block text-sm font-medium text-slate-600 mb-1">Nome de Usuário</label>
                            <input type="text" name="username" id="username" required class="w-full px-3 py-2 border border-slate-300 rounded-md focus:outline-none focus:ring-2 focus:ring-sky-500">
                        </div>
                        <button type="submit" class="w-full bg-sky-500 text-white font-bold py-2 px-4 rounded-md hover:bg-sky-600 transition duration-200"><i class="fas fa-plus mr-2"></i> Criar Usuário</button>
                    </form>
                </div>
                <div class="bg-white p-6 rounded-xl shadow-md border border-slate-200">
                    <h3 class="text-xl font-semibold mb-4 border-b pb-2">2. Adicionar Publicação</h3>
                    {% if users %}
                    <form action="{{ url_for('add_post') }}" method="POST">
                        <div class="mb-4">
                            <label for="user_id" class="block text-sm font-medium text-slate-600 mb-1">Autor</label>
                            <select name="user_id" id="user_id" class="w-full px-3 py-2 border border-slate-300 rounded-md focus:outline-none focus:ring-2 focus:ring-sky-500">
                                {% for user in users %}<option value="{{ user.id }}">{{ user.username }}</option>{% endfor %}
                            </select>
                        </div>
                        <div class="mb-4">
                            <label for="title" class="block text-sm font-medium text-slate-600 mb-1">Título</label>
                            <input type="text" name="title" id="title" required class="w-full px-3 py-2 border border-slate-300 rounded-md focus:outline-none focus:ring-2 focus:ring-sky-500">
                        </div>
                         <div class="mb-4">
                            <label for="tags" class="block text-sm font-medium text-slate-600 mb-1">Tags (separadas por vírgula)</label>
                            <input type="text" name="tags" id="tags" placeholder="ex: python, flask, sql" class="w-full px-3 py-2 border border-slate-300 rounded-md focus:outline-none focus:ring-2 focus:ring-sky-500">
                        </div>
                        <div class="mb-4">
                            <label for="content" class="block text-sm font-medium text-slate-600 mb-1">Conteúdo</label>
                            <textarea name="content" id="content" rows="3" class="w-full px-3 py-2 border border-slate-300 rounded-md focus:outline-none focus:ring-2 focus:ring-sky-500"></textarea>
                        </div>
                        <button type="submit" class="w-full bg-emerald-500 text-white font-bold py-2 px-4 rounded-md hover:bg-emerald-600 transition duration-200"><i class="fas fa-plus mr-2"></i>Criar Publicação</button>
                    </form>
                    {% else %}
                    <p class="text-center text-slate-500 italic p-4 bg-slate-50 rounded-md">Crie um usuário primeiro.</p>
                    {% endif %}
                </div>
            </div>
            <div class="lg:col-span-2">
                <div class="bg-white p-6 rounded-xl shadow-md border border-slate-200">
                    <h3 class="text-xl font-semibold mb-4 border-b pb-2 flex items-center"><i class="fas fa-database mr-3 text-slate-500"></i> Dados Atuais</h3>
                    {% with messages = get_flashed_messages(with_categories=true) %}
                      {% if messages %}
                        <div class="mb-4 space-y-2">
                        {% for category, message in messages %}
                          <div class="p-4 rounded-md text-sm {% if category == 'danger' %} bg-red-100 text-red-800 {% elif category == 'success' %} bg-green-100 text-green-800 {% else %} bg-blue-100 text-blue-800 {% endif %}">{{ message }}</div>
                        {% endfor %}
                        </div>
                      {% endif %}
                    {% endwith %}
                    <div class="space-y-6">
                        {% for user in users %}
                        <div class="border border-slate-200 rounded-lg p-4">
                            <div class="flex justify-between items-start">
                                <h4 class="font-bold text-lg text-sky-700"><i class="fas fa-user mr-2"></i>{{ user.username }}</h4>
                                <form action="{{ url_for('delete_user', user_id=user.id) }}" method="POST" onsubmit="return confirm('Tem certeza que deseja deletar este usuário e TODAS as suas publicações?');">
                                    <button type="submit" class="text-red-500 hover:text-red-700 transition duration-200 text-sm"><i class="fas fa-trash-alt mr-1"></i> Deletar Usuário</button>
                                </form>
                            </div>
                            <div class="mt-3 pl-4">
                                <h5 class="font-semibold text-emerald-700 mb-2"><i class="fas fa-newspaper mr-2"></i> Publicações</h5>
                                {% if user.posts %}
                                    <div class="space-y-3">
                                    {% for post in user.posts %}
                                        <div class="bg-slate-50 p-3 rounded-md border-l-4 border-emerald-500">
                                            <div class="flex justify-between items-start">
                                                <div>
                                                    <p class="text-slate-800 font-semibold">{{ post.title }}</p>
                                                    <p class="text-slate-600 italic text-sm">"{{ post.content if post.content else 'N/A' }}"</p>
                                                </div>
                                                <div class="flex items-center space-x-2 flex-shrink-0">
                                                    <a href="{{ url_for('edit_post', post_id=post.id) }}" class="text-yellow-500 hover:text-yellow-700 transition duration-200"><i class="fas fa-edit"></i></a>
                                                    <form action="{{ url_for('delete_post', post_id=post.id) }}" method="POST" onsubmit="return confirm('Deletar esta publicação?');">
                                                        <button type="submit" class="text-red-500 hover:text-red-700 transition duration-200"><i class="fas fa-trash-alt"></i></button>
                                                    </form>
                                                </div>
                                            </div>
                                            <div class="mt-2">
                                                {% for tag in post.tags %}
                                                    <span class="bg-purple-200 text-purple-800 text-xs font-semibold mr-2 px-2.5 py-0.5 rounded-full">{{ tag.name }}</span>
                                                {% endfor %}
                                            </div>
                                        </div>
                                    {% endfor %}
                                    </div>
                                {% else %}
                                    <p class="text-slate-500 italic text-sm"><i class="fas fa-exclamation-circle mr-2"></i> Nenhuma publicação.</p>
                                {% endif %}
                            </div>
                        </div>
                        {% else %}
                        <p class="text-center text-slate-500 italic p-4 bg-slate-50 rounded-md">Nenhum usuário cadastrado.</p>
                        {% endfor %}
                    </div>
                </div>
            </div>
        </div>
        <footer class="text-center mt-12 text-slate-500 text-sm"><p>SENAI - Desenvolvimento de sitemas web.</p></footer>
    </div>
</body>
</html>
"""

EDIT_TEMPLATE = """
<!DOCTYPE html>
<html lang="pt-br">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Editar Publicação</title>
    <script src="https://cdn.tailwindcss.com"></script>
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0-beta3/css/all.min.css">
    <style> body { font-family: 'Inter', sans-serif; } @import url('https://rsms.me/inter/inter.css'); </style>
</head>
<body class="bg-slate-100 text-slate-800">
    <div class="container mx-auto p-4 md:p-8 max-w-2xl">
        <header class="text-center mb-10">
            <h1 class="text-4xl font-bold text-slate-900">Editar Publicação</h1>
            <p class="text-lg text-slate-600 mt-2">Altere os dados da publicação abaixo.</p>
        </header>
        <div class="bg-white p-6 rounded-xl shadow-md border border-slate-200">
            <form action="{{ url_for('edit_post', post_id=post.id) }}" method="POST">
                <div class="mb-4">
                    <label for="title" class="block text-sm font-medium text-slate-600 mb-1">Título</label>
                    <input type="text" name="title" id="title" value="{{ post.title }}" required class="w-full px-3 py-2 border border-slate-300 rounded-md focus:outline-none focus:ring-2 focus:ring-yellow-500">
                </div>
                 <div class="mb-4">
                    <label for="tags" class="block text-sm font-medium text-slate-600 mb-1">Tags (separadas por vírgula)</label>
                    <input type="text" name="tags" id="tags" value="{{ current_tags }}" class="w-full px-3 py-2 border border-slate-300 rounded-md focus:outline-none focus:ring-2 focus:ring-yellow-500">
                </div>
                <div class="mb-4">
                    <label for="content" class="block text-sm font-medium text-slate-600 mb-1">Conteúdo</label>
                    <textarea name="content" id="content" rows="5" class="w-full px-3 py-2 border border-slate-300 rounded-md focus:outline-none focus:ring-2 focus:ring-yellow-500">{{ post.content }}</textarea>
                </div>
                <div class="flex items-center justify-end space-x-4">
                    <a href="{{ url_for('index') }}" class="bg-slate-200 text-slate-800 font-bold py-2 px-4 rounded-md hover:bg-slate-300 transition duration-200">Cancelar</a>
                    <button type="submit" class="bg-yellow-500 text-white font-bold py-2 px-4 rounded-md hover:bg-yellow-600 transition duration-200">
                        <i class="fas fa-save mr-2"></i>Salvar Alterações
                    </button>
                </div>
            </form>
        </div>
    </div>
</body>
</html>
"""

# -----------------------------------------------------------------------------
# INICIALIZAÇÃO DA APLICAÇÃO
# -----------------------------------------------------------------------------
if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)
