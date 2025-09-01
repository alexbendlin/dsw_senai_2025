# -*- coding: utf-8 -*-

# Passo 1: Importações e Configuração
from flask import Flask, render_template, request, redirect, url_for

# Inicializa a aplicação Flask
app = Flask(__name__)

# --- Rotas da Aplicação ---

# Rota principal que exibe o formulário e a lista de usuários
@app.route('/')
def index():
    return "Olá Galera!"


# Passo 3: Criando o Banco de Dados Físico
if __name__ == '__main__':
    # Inicia o servidor de desenvolvimento do Flask
    app.run(host='0.0.0.0', port=5000, debug=True)
