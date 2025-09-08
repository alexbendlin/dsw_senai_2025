# Importa as classes e funções necessárias do Flask.
from flask import Flask, render_template, request, redirect, url_for, flash
# Importa o formulário que acabamos de criar.
from forms import ContactForm

# Cria uma instância da aplicação.
app = Flask(__name__)
# Configura uma chave secreta para usar com flash messages e Flask-WTF (obrigatório).
app.config['SECRET_KEY'] = 'uma-chave-secreta-para-revisao-com-wtf'

# ---- Conteúdo da Revisão (dados para os templates) ----

# Dados para a Semana 2 (templates e laços de repetição).
conteudo_semana_2 = {
    'titulo': 'Semana 2: Templates com Jinja2',
    'conceitos': [
        'Separação de Lógica e Apresentação (Python vs. HTML)',
        'O que é um Template Engine (Jinja2)',
        'Sintaxe de Expressões ({{ }}): Exibir variáveis',
        'Sintaxe de Estruturas de Controle ({% %}): Laços (for), Condicionais (if)',
        'Herança de Templates (extends, block): O princípio DRY'
    ],
    'desafio': 'Crie um template que herde de base.html e exiba uma lista de hobbies com um laço for.'
}

# Dados para a Semana 3 (arquivos estáticos e formulários).
conteudo_semana_3 = {
    'titulo': 'Semana 3: Conteúdo Estático e Formulários',
    'conceitos': [
        'Servindo Arquivos Estáticos (a pasta "static")',
        "A função url_for('static', filename='...')",
        'Fundamentos de Formulários HTML (<form>, <input>, <label>)',
        'Métodos HTTP: GET vs. POST (visível vs. invisível)',
        'Recebendo dados no Flask (o objeto request)'
    ],
    'desafio': 'Crie um formulário de feedback que envie os dados usando o método POST para uma nova rota.'
}

# Dados para a Semana 4 (validação de formulários).
conteudo_semana_4 = {
    'titulo': 'Semana 4: Validação de Formulários',
    'conceitos': [
        'A necessidade de validação no lado do servidor',
        'Uso de Flask-WTF (simplifica a criação e validação)',
        'Validações básicas (dados obrigatórios, formatos, etc.)',
        'Tratamento de erros e exibição de mensagens ao usuário (flash)'
    ],
    'desafio': 'Adicione validação para que os campos de um formulário de contato não fiquem em branco.'
}

# ---- Rotas (URLs) da Aplicação ----

# Rota para a página inicial
@app.route('/')
def index():
    """Renderiza a página inicial com links para as revisões."""
    return render_template('index.html')

# Rota genérica para as páginas de revisão.
# Recebe o nome da semana como um parâmetro de rota.
@app.route('/revisao/<semana_id>')
def revisao(semana_id):
    """
    Renderiza a página de revisão para a semana especificada.
    Trata dinamicamente o conteúdo de cada semana.
    """
    if semana_id == 'semana1':
        titulo = 'Semana 1: Introdução ao Desenvolvimento Web e Flask'
        conceitos = [
            'O Modelo Cliente-Servidor (HTTP)',
            'O que é um Framework Web (Flask)',
            'Ambientes Virtuais (venv)',
            'Criação de Rotas com @app.route()'
        ]
        desafio = 'Adicione novas rotas para suas páginas favoritas.'
        return render_template('revisao.html', titulo=titulo, conceitos=conceitos, desafio=desafio)
    
    elif semana_id == 'semana2':
        return render_template('revisao.html', **conteudo_semana_2)

    elif semana_id == 'semana3':
        return render_template('revisao.html', **conteudo_semana_3)

    elif semana_id == 'semana4':
        return render_template('revisao.html', **conteudo_semana_4)

    # Redireciona para a página inicial caso a semana não exista.
    return redirect(url_for('index'))

# Rota para o formulário de contato (versão HTML tradicional).
@app.route('/contato', methods=['GET', 'POST'])
def contato():
    """
    Exibe um formulário de contato e processa o envio dos dados.
    Esta é a versão com HTML puro.
    """
    if request.method == 'POST':
        # Obtém os dados do formulário.
        nome = request.form['nome']
        email = request.form['email']
        mensagem = request.form['mensagem']
        
        # Simples validação de campos obrigatórios.
        if not nome or not email or not mensagem:
            flash('Por favor, preencha todos os campos!', 'danger')
            return render_template('contato.html')
        
        print(f"Novo contato recebido de {nome} ({email}): {mensagem}")
        
        flash('Sua mensagem foi enviada com sucesso!', 'success')
        return redirect(url_for('contato'))
    
    return render_template('contato.html')

# Nova rota para o formulário de contato (versão Flask-WTF).
@app.route('/contato-wtf', methods=['GET', 'POST'])
def contato_wtf():
    """
    Exibe um formulário de contato e processa o envio dos dados.
    Agora usa a classe de formulário Flask-WTF.
    """
    form = ContactForm()
    # Verifica se a requisição é POST e se o formulário é válido.
    if form.validate_on_submit():
        # Obtém os dados do formulário a partir do objeto 'form'.
        nome = form.nome.data
        email = form.email.data
        mensagem = form.mensagem.data
        
        print(f"Novo contato recebido de {nome} ({email}): {mensagem}")
        
        flash('Sua mensagem foi enviada com sucesso!', 'success')
        # Redireciona para evitar reenvio do formulário.
        return redirect(url_for('contato_wtf'))
    
    # Se a requisição for GET ou se a validação falhar,
    # renderiza o template com o formulário.
    return render_template('contato-wtf.html', form=form)


# ---- Executa a aplicação ----
if __name__ == '__main__':
    # Roda a aplicação no modo de depuração.
    app.run(debug=True)
