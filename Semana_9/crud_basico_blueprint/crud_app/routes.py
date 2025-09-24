from flask import Blueprint, render_template, request, redirect, url_for
from .models import db, Usuario

# Criamos o Blueprint. 'main' é o nome do blueprint.
main = Blueprint('main', __name__)

@main.route('/')
def index():
    usuarios = Usuario.query.all()
    return render_template('index.html', usuarios=usuarios)

@main.route('/adicionar', methods=['GET', 'POST'])
def adicionar():
    if request.method == 'POST':
        nome = request.form['nome']
        email = request.form['email']
        novo_usuario = Usuario(nome=nome, email=email)
        try:
            db.session.add(novo_usuario)
            db.session.commit()
            # Note que o 'url_for' agora usa '.index' precedido pelo nome do blueprint
            return redirect(url_for('main.index'))
        except:
            return "Ocorreu um erro ao adicionar o usuário."

    return render_template('adicionar.html')

@main.route('/editar/<int:id>', methods=['GET', 'POST'])
def editar(id):
    usuario = Usuario.query.get_or_404(id)
    if request.method == 'POST':
        usuario.nome = request.form['nome']
        usuario.email = request.form['email']
        try:
            db.session.commit()
            return redirect(url_for('main.index'))
        except:
            return "Ocorreu um erro ao editar o usuário."
    else:
        return render_template('editar.html', usuario=usuario)

@main.route('/deletar/<int:id>', methods=['POST'])
def deletar(id):
    usuario = Usuario.query.get_or_404(id)
    try:
        db.session.delete(usuario)
        db.session.commit()
        return redirect(url_for('main.index'))
    except:
        return "Ocorreu um erro ao deletar o usuário."