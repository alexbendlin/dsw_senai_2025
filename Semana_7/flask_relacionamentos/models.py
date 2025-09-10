from flask_sqlalchemy import SQLAlchemy

# Cria uma instância do SQLAlchemy.
# Esta instância será vinculada à aplicação Flask no arquivo app.py
db = SQLAlchemy()

# ==============================================================================
# RELACIONAMENTO ONE-TO-ONE (Um-para-Um)
# Exemplo: Usuario <-> Perfil
# Um usuário tem um perfil, e um perfil pertence a um único usuário.
# ==============================================================================

class Usuario(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nome_usuario = db.Column(db.String(80), unique=True, nullable=False)
    
    # O relacionamento é definido aqui.
    # 'Perfil' é a classe com a qual estamos nos relacionando.
    # back_populates='usuario' cria um link de volta, permitindo que de um objeto Perfil,
    # possamos acessar o objeto Usuario correspondente através de `profile.usuario`.
    # cascade='all, delete-orphan' significa que se um usuário for deletado,
    # seu perfil associado também será.
    perfil = db.relationship('Perfil', back_populates='usuario', uselist=False, cascade='all, delete-orphan')

    def __repr__(self):
        return f'<Usuario {self.nome_usuario}>'

class Perfil(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    bio = db.Column(db.String(200), nullable=True)
    
    # A chave estrangeira (ForeignKey) é a coluna que armazena o ID do usuário,
    # estabelecendo a conexão entre as tabelas no nível do banco de dados.
    usuario_id = db.Column(db.Integer, db.ForeignKey('usuario.id'), unique=True, nullable=False)

    # Este é o outro lado do relacionamento definido em Usuario.
    usuario = db.relationship('Usuario', back_populates='perfil')

    def __repr__(self):
        return f'<Perfil for {self.usuario.nome_usuario}>'


# ==============================================================================
# RELACIONAMENTO ONE-TO-MANY (Um-para-Muitos)
# Exemplo: Autor -> Book
# Um autor pode ter escrito muitos livros, mas um livro pertence a um único autor.
# ==============================================================================

class Autor(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100), nullable=False)

    # 'livros' será uma lista de objetos Livro associados a este autor.
    # back_populates='autor' permite que de um objeto Livro, possamos acessar
    # o autor através de `livro.autor`.
    livros = db.relationship('Livro', back_populates='autor', cascade='all, delete-orphan')

    def __repr__(self):
        return f'<Autor {self.nome}>'

class Livro(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    titulo = db.Column(db.String(150), nullable=False)

    # A chave estrangeira aponta para o ID do autor na tabela 'autor'.
    autor_id = db.Column(db.Integer, db.ForeignKey('autor.id'), nullable=False)
    
    # O relacionamento de volta para o autor.
    autor = db.relationship('Autor', back_populates='livros')

    def __repr__(self):
        return f'<Livro {self.titulo}>'


# ==============================================================================
# RELACIONAMENTO MANY-TO-MANY (Muitos-para-Muitos)
# Exemplo: Aluno <-> Curso
# Um aluno pode estar em vários cursos, e um curso pode ter vários alunos.
# Isso requer uma tabela de associação (também chamada de tabela de junção).
# ==============================================================================

# A tabela de associação é definida usando a API do SQLAlchemy Core.
# Ela não precisa de uma classe de modelo própria.
associacao_de_cursos_alunos = db.Table('aluno_cursos',
    db.Column('aluno_id', db.Integer, db.ForeignKey('aluno.id'), primary_key=True),
    db.Column('curso_id', db.Integer, db.ForeignKey('curso.id'), primary_key=True)
)

class Aluno(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100), nullable=False)
    
    # O relacionamento é definido aqui.
    # 'secondary' aponta para a nossa tabela de associação.
    # 'back_populates' conecta com o relacionamento no modelo Curso.
    # Agora, `alunos.cursos` será uma lista de cursos em que o aluno está inscrito.
    cursos = db.relationship('Curso', secondary=associacao_de_cursos_alunos, back_populates='alunos')

    def __repr__(self):
        return f'<Aluno {self.nome}>'

class Curso(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100), nullable=False)
    
    # O outro lado do relacionamento Many-to-Many.
    # `curso.alunos` será uma lista de alunos inscritos neste curso.
    alunos = db.relationship('Aluno', secondary=associacao_de_cursos_alunos, back_populates='cursos')

    def __repr__(self):
        return f'<Curso {self.nome}>'
