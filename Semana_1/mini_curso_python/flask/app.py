# Exemplo de uma aplicação Flask simples

# 1. Importa a classe Flask, que é a peça central da nossa aplicação.
from flask import Flask, request

# 2. Cria uma instância da aplicação.
# A variável __name__ informa ao Flask onde procurar por outros arquivos do projeto.
app = Flask(__name__)

# 3. Define a "rota" principal do site usando um "decorator".
# Isso significa: "Quando alguém acessar o endereço '/', execute a função logo abaixo."
@app.route('/')
def ola_mundo():
    # 4. A função retorna o conteúdo (em HTML) que será exibido no navegador.
    return "<h1>Olá galera!!!</h1>"

# Rota estática para exibir uma mensagem sobre a aplicação
# 5. Define outra rota que será acessada quando o usuário visitar '/sobre'.
@app.route('/sobre')
def sobre():
    return "<h1>Está é a página sobre!</h1>"

# Rota dinâmica para exibir o perfil de um usuário
# 6. Define uma rota que aceita um parâmetro dinâmico na URL.
# O parâmetro 'usuario' será capturado e passado para a função.
# Por exemplo, se o usuário acessar '/perfil/joao', 'usuario' será 'joao'.
@app.route('/perfil/<usuario>')
def perfil(usuario):
    return f'<h1>Exibindo o perfil de: {usuario}</h1>'

# Rota dinâmica para exibir dados de um produto
# 7. Define uma rota que aceita um parâmetro inteiro na URL.
# O parâmetro 'id_produto' será capturado e passado para a função.
# Por exemplo, se o usuário acessar '/produto/42', 'id_produto' será 42.
@app.route('/produto/<int:id_produto>')
def consultar_produto(id_produto):
    return f"<h1>Exibindo dados do produto com ID: {id_produto}</h1>"

# Rota para exibir um formulário de login
# 8. Define uma rota que aceita métodos GET e POST.
# Se o método for POST, exibe o usuário digitado; se for GET, exibe um formulário.
# Isso permite que o usuário envie dados através de um formulário HTML.
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        usuario = request.form['usuario']
        return f'<h1>Usuário: {usuario}'
    else:
        return '''
          <form method="post">
            <input type="text" name="usuario">
            <input type="submit" value="Login">
          </form>    
        '''

# Rota para consultar um produto com tratamento de erro
# 8.1 Define uma rota que aceita um parâmetro dinâmico na URL.
# Se o parâmetro não for um número inteiro válido, retorna um erro 404.
# Isso é útil para evitar erros quando o usuário tenta acessar um produto com um ID inválido
@app.route('/produto_v2/<id_produto>')
def consultar_produto_v2(id_produto):
    try:
        # Tenta converter o id_produto para um inteiro
        id_produto_int = int(id_produto)
        # Se a conversão for bem-sucedida, você pode usar o id_produto_int
        return f"<h1>Exibindo dados do produto com ID: {id_produto_int}</h1>"
    except ValueError:
        # Se a conversão falhar (por exemplo, se id_produto for 'xx')
        # você pode retornar um erro 404 ou 400 (Bad Request)
        # abort(404) é uma função do Flask que dispara a página de erro 404
        return f"<h1>Erro: O ID do produto '{id_produto}' não é um número inteiro válido.</h1>", 400

# 9. Define um manipulador de erros para o código de status 404 (Página não encontrada).
# Isso será chamado quando o usuário tentar acessar uma URL que não existe.
# Você pode personalizar a mensagem de erro ou renderizar um template HTML.
@app.errorhandler(404)
def pagina_nao_encontrada(error):
    # Aqui você pode renderizar um template HTML personalizado
    # ou apenas retornar uma string
    return "<h1>Página não encontrada!</h1><p>A URL que você tentou acessar não existe ou o ID do produto não é um número inteiro válido.</p>", 404

# 10. Inicia o servidor Flask.
# O servidor ficará escutando na porta 5000 por padrão.
# O parâmetro debug=True permite que o servidor reinicie automaticamente ao detectar mudanças no código.
# O parâmetro host='0.0.0.0' permite que o servidor seja acessado de outras máquinas na rede.
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)

# Exemplo de uso Flask
# Para rodar o servidor, execute: python app.py
# Acesse o servidor em http://localhost:5000
# A rota raiz (/) exibe uma mensagem de boas-vindas
# A rota /sobre exibe uma mensagem sobre a aplicação
# A rota /perfil/<usuario> exibe o perfil do usuário especificado na URL
# A rota /produto/<int:id_produto> exibe os dados do produto com o ID especificado
# A rota /login permite que o usuário faça login, exibindo um formulário
# Se o método for POST, exibe o usuário digitado
# Se o método for GET, exibe um formulário para o usuário digitar seu nome
# O servidor Flask roda na porta 5000 por padrão, mas pode ser alterado
# O parâmetro debug=True permite que o servidor reinicie automaticamente ao detectar mudanças no código
# O parâmetro host='0.0.0.0' permite que o servidor seja acessado de outras máquinas na rede
# Flask é um microframework para Python que facilita a criação de aplicações web
# Ele permite definir rotas, manipular requisições e respostas, e renderizar templates
# Flask é leve e fácil de usar, ideal para projetos pequenos e médios
# Para instalar o Flask, use o comando: pip install Flask
# A documentação oficial do Flask pode ser encontrada em https://flask.palletsprojects.com
# Flask suporta a criação de APIs RESTful, permitindo a construção de serviços web
# É possível integrar o Flask com bancos de dados, autenticação, e outras funcionalidades
# Flask é amplamente utilizado para prototipagem rápida e desenvolvimento ágil de aplicações web
# É possível criar extensões para adicionar funcionalidades extras ao Flask
# Exemplo de extensão: Flask-SQLAlchemy para integração com bancos de dados
# Exemplo de extensão: Flask-WTF para formulários e validação
# Exemplo de extensão: Flask-Login para autenticação de usuários
