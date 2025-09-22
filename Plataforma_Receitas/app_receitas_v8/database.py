from flask_sqlalchemy import SQLAlchemy

# Cria a instância do SQLAlchemy sem associá-la a uma aplicação ainda.
# Isso evita a importação circular.
db = SQLAlchemy()