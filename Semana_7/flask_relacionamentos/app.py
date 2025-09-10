import os
from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from models import db, Usuario, Perfil, Autor, Livro, Aluno, Curso, associacao_de_cursos_alunos

# --- CONFIGURAÇÃO DA APLICAÇÃO ---
app = Flask(__name__)

# Configuração do caminho do banco de dados
# __file__ é o caminho para o arquivo atual (app.py)
# os.path.abspath() obtém o caminho absoluto
# os.path.dirname() obtém o diretório do arquivo
# Isso garante que o banco de dados será criado na pasta 'instance' dentro do diretório do projeto
basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'instance', 'project.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Inicializa a extensão SQLAlchemy com a aplicação Flask
db.init_app(app)

# --- COMANDO PARA INICIALIZAR O BANCO DE DADOS ---
@app.cli.command('init-db')
def init_db_command():
    """Cria as tabelas do banco de dados e as popula com dados iniciais."""
    with app.app_context():
        # Garante que a pasta 'instance' exista
        if not os.path.exists(os.path.join(basedir, 'instance')):
            os.makedirs(os.path.join(basedir, 'instance'))

        db.drop_all()  # Apaga tudo para um começo limpo
        db.create_all()  # Cria as tabelas baseadas nos modelos

        # --- DADOS INICIAIS (SEED) ---
        print("Populando o banco de dados com dados iniciais...")

        # 1:1 - Usuários e Perfis
        usuario1 = Usuario(nome_usuario='ana.silva')
        perfil1 = Perfil(bio='Desenvolvedora Python e entusiasta de Flask.', usuario=usuario1)
        usuario2 = Usuario(nome_usuario='carlos.souza')
        perfil2 = Perfil(bio='Gerente de projetos ágeis.', usuario=usuario2)
        db.session.add_all([usuario1, perfil1, usuario2, perfil2])
        
        # 1:M - Autores e Livros
        autor1 = Autor(nome='J.K. Rowling')
        autor2 = Autor(nome='J.R.R. Tolkien')
        livro1 = Livro(titulo='Harry Potter e a Pedra Filosofal', autor=autor1)
        livro2 = Livro(titulo='O Hobbit', autor=autor2)
        livro3 = Livro(titulo='O Senhor dos Anéis: A Sociedade do Anel', autor=autor2)
        db.session.add_all([autor1, autor2, livro1, livro2, livro3])

        # M:M - Alunos e Cursos
        aluno1 = Aluno(nome='Mariana')
        aluno2 = Aluno(nome='Lucas')
        aluno3 = Aluno(nome='Beatriz')
        curso1 = Curso(nome='Introdução à Programação')
        curso2 = Curso(nome='Estrutura de Dados')
        curso3 = Curso(nome='Desenvolvimento Web com Flask')
        
        # Associando alunos aos cursos
        curso1.alunos.append(aluno1)
        curso1.alunos.append(aluno2)
        curso2.alunos.append(aluno2)
        curso2.alunos.append(aluno3)
        curso3.alunos.append(aluno1)
        curso3.alunos.append(aluno3)

        db.session.add_all([aluno1, aluno2, aluno3, curso1, curso2, curso3])

        db.session.commit()
        print("Banco de dados inicializado e populado com sucesso!")


# --- ROTAS DA APLICAÇÃO ---

@app.route('/')
def index():
    """Página inicial."""
    return render_template('index.html')

# --- ROTAS PARA UM-PARA-UM ---
@app.route('/um-para-um', methods=['GET', 'POST'])
def um_para_um():
    """Página para demonstrar o relacionamento Um-para-Um."""
    if request.method == 'POST':
        nome_usuario = request.form['nome_usuario']
        bio = request.form['bio']
        
        # Cria um novo usuário e seu perfil associado
        novo_usuario = Usuario(nome_usuario=nome_usuario)
        novo_perfil = Perfil(bio=bio, usuario=novo_usuario)
        
        db.session.add(novo_usuario)
        db.session.add(novo_perfil)
        db.session.commit()
        
        return redirect(url_for('um_para_um'))

    usuarios = Usuario.query.all()
    return render_template('um_para_um.html', usuarios=usuarios)

# --- ROTAS PARA UM-PARA-MUITOS ---
@app.route('/um-para-muitos', methods=['GET', 'POST'])
def um_para_muitos():
    """Página para demonstrar o relacionamento Um-para-Muitos."""
    if request.method == 'POST':
        titulo = request.form['titulo']
        autor_id = request.form['autor_id']
        
        autor = Autor.query.get(autor_id)
        if autor:
            novo_livro = Livro(titulo=titulo, autor=autor)
            db.session.add(novo_livro)
            db.session.commit()

        return redirect(url_for('um_para_muitos'))

    autores = Autor.query.all()
    return render_template('um_para_muitos.html', autores=autores)

@app.route('/add-autor', methods=['POST'])
def add_autor():
    """Rota para adicionar um novo autor."""
    nome = request.form['nome']
    if nome:
        novo_autor = Autor(nome=nome)
        db.session.add(novo_autor)
        db.session.commit()
    return redirect(url_for('um_para_muitos'))


# --- ROTAS PARA MUITOS-PARA-MUITOS ---
@app.route('/muitos-para-muitos', methods=['GET', 'POST'])
def muitos_para_muitos():
    """Página para demonstrar o relacionamento Muitos-para-Muitos."""
    if request.method == 'POST':
        aluno_id = request.form['aluno_id']
        curso_id = request.form['curso_id']

        aluno = Aluno.query.get(aluno_id)
        curso = Curso.query.get(curso_id)

        if aluno and curso:
            # A mágica do SQLAlchemy: basta adicionar o objeto à lista
            # e a tabela de associação é atualizada automaticamente.
            if aluno not in curso.alunos:
                curso.alunos.append(aluno)
                db.session.commit()
        
        return redirect(url_for('muitos_para_muitos'))

    alunos = Aluno.query.all()
    cursos = Curso.query.all()
    return render_template('muitos_para_muitos.html', alunos=alunos, cursos=cursos)

# --- ROTA PRINCIPAL PARA EXECUÇÃO ---
if __name__ == '__main__':
    app.run(debug=True)
