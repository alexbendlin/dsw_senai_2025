# Importa as classes e funções necessárias
from flask import Flask, render_template, flash, redirect, url_for
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired, Email

# 1. CONFIGURAÇÃO DA APLICAÇÃO
app = Flask(__name__)

# A SECRET_KEY é crucial para a proteção CSRF. 
# Em um projeto real, isso deve ser uma string complexa e mantida em segredo.
app.config['SECRET_KEY'] = 'uma-chave-secreta-muito-dificil-de-adivinhar'

# 2. DEFINIÇÃO DA CLASSE DO FORMULÁRIO
# Esta classe herda de FlaskForm e define a estrutura e as regras do nosso formulário.
class MeuFormulario(FlaskForm):
    """
    Representa o formulário de contato com validação.
    """
    # StringField: Campo de texto.
    # O primeiro argumento é o 'label' que aparecerá para o usuário.
    # 'validators' é uma lista de regras. DataRequired garante que o campo não seja enviado vazio.
    nome = StringField('Nome Completo', validators=[DataRequired(message="Este campo é obrigatório.")])
    
    # O validor Email() checa se o texto inserido tem um formato de e-mail válido.
    email = StringField('Seu Melhor E-mail', validators=[
        DataRequired(message="Este campo é obrigatório."), 
        Email(message="Por favor, insira um e-mail válido.")
    ])
    
    # SubmitField: Representa o botão de envio do formulário.
    submit = SubmitField('Enviar Cadastro')

# 3. CRIAÇÃO DAS ROTAS (VIEWS)

# Rota original, com o formulário em branco
@app.route('/formulario', methods=['GET', 'POST'])
def formulario():
    """
    Renderiza o formulário e processa os dados enviados.
    """
    form = MeuFormulario()
    if form.validate_on_submit():
        nome_usuario = form.nome.data
        email_usuario = form.email.data
        flash(f'Cadastro recebido com sucesso para {nome_usuario} ({email_usuario})!', 'success')
        return redirect(url_for('formulario'))
        
    return render_template('formulario.html', form=form)

# --- EXEMPLOS DE PREENCHIMENTO ---

# Exemplo 1: Populando o formulário via argumentos diretos
@app.route('/formulario/preenchido-args', methods=['GET', 'POST'])
def formulario_com_argumentos():
    """
    Demonstra como popular o formulário passando os valores como argumentos
    na sua instanciação.
    """
    form = MeuFormulario(nome="Fulano de Tal", email="fulano@exemplo.com")
    
    if form.validate_on_submit():
        flash(f'Dados de "{form.nome.data}" atualizados com sucesso!', 'success')
        return redirect(url_for('formulario_com_argumentos'))
        
    return render_template('formulario.html', form=form)

# Exemplo 2: Populando o formulário com um objeto
@app.route('/formulario/preenchido-obj', methods=['GET', 'POST'])
def formulario_com_objeto():
    """
    Demonstra como popular o formulário a partir de um objeto,
    simulando dados vindos de um banco de dados.
    """
    class UsuarioMock:
        def __init__(self, nome, email):
            self.nome = nome
            self.email = email
            
    usuario_do_banco = UsuarioMock(nome="Ciclano da Silva", email="ciclano@banco.com")

    form = MeuFormulario(obj=usuario_do_banco)
    
    if form.validate_on_submit():
        flash(f'Dados de "{form.nome.data}" atualizados com sucesso!', 'success')
        return redirect(url_for('formulario_com_objeto'))
        
    return render_template('formulario.html', form=form)


# Rota principal agora renderiza um template HTML
@app.route('/')
def index():
    """
    Renderiza a página inicial a partir de um arquivo de template.
    """
    return render_template('index.html')

# Permite executar o app diretamente com 'python app.py'
if __name__ == '__main__':
    app.run(debug=True)
