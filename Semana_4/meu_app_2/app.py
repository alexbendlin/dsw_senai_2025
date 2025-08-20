from flask import Flask

# --- Configuração da Aplicação Flask ---
app = Flask(__name__)


# --- Rotas da Aplicação ---

@app.route("/")
def index():
    return "<h1>Começando a aprender Flask-WTF!</h1>"


# --- Execução da Aplicação ---
if __name__ == '__main__':
    app.run(debug=True)
