from flask import Flask, render_template, request, redirect, url_for
from flask_login import LoginManager, UserMixin, login_user, logout_user, login_required, current_user

# 1. Configuração Inicial
app = Flask(__name__)
# Chave secreta para proteger a sessão. Em um app real, use um valor complexo e secreto.
app.config['SECRET_KEY'] = 'sua-chave-secreta-muito-dificil'

# 2. Configuração do Flask-Login
login_manager = LoginManager()
login_manager.init_app(app)
# Se um usuário não logado tentar acessar uma página protegida,
# o Flask-Login o redirecionará para a rota 'login'.
login_manager.login_view = 'login'

# 3. Modelo de Usuário (Simulado)
# Em uma aplicação real, isso viria de um banco de dados.
# A classe User precisa herdar de UserMixin para ter os métodos que o Flask-Login espera
# (is_authenticated, is_active, is_anonymous, get_id()).
class User(UserMixin):
    def __init__(self, id, username, password):
        self.id = id
        self.username = username
        self.password = password

# "Banco de dados" de usuários em memória (um dicionário simples).
# A chave é o ID do usuário.
users_db = {
    '1': User('1', 'aluno', 'senha123'),
    '2': User('2', 'prof', 'senha456')
}

# 4. A função "user_loader"
# Esta é a função mais importante. O Flask-Login a usa para recarregar o objeto
# do usuário a partir do ID do usuário que é armazenado na sessão.
@login_manager.user_loader
def load_user(user_id):
    return users_db.get(user_id)

# 5. Definição das Rotas (Views)

@app.route('/')
def index():
    # A variável 'current_user' está sempre disponível nos templates
    # graças ao Flask-Login.
    return render_template('index.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        # Procura o usuário no nosso "banco de dados"
        user = None
        for u in users_db.values():
            if u.username == username:
                user = u
                break
        
        # Verifica se o usuário existe e se a senha está correta
        if user and user.password == password:
            # Se tudo estiver correto, "loga" o usuário com a função do Flask-Login.
            # É aqui que a "pulseira VIP" é colocada.
            login_user(user)
            # Redireciona para a página protegida após o login.
            return redirect(url_for('protegido'))
        else:
            # Caso contrário, exibe uma mensagem de erro (em um app real, use flash messages)
            return 'Usuário ou senha inválidos!'

    return render_template('login.html')

@app.route('/protegido')
@login_required # <-- A MÁGICA ACONTECE AQUI!
def protegido():
    # Este decorator garante que apenas usuários logados podem acessar esta rota.
    # 'current_user' contém o objeto do usuário que está logado.
    return render_template('protegido.html')

@app.route('/logout')
@login_required # É uma boa prática garantir que só usuários logados possam deslogar
def logout():
    # Remove a "pulseira VIP" do usuário.
    logout_user()
    return redirect(url_for('index'))

# Roda a aplicação
if __name__ == '__main__':
    app.run(debug=True)