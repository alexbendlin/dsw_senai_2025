import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy

# Define o caminho base do projeto
basedir = os.path.abspath(os.path.dirname(__file__))

# Cria a instância da aplicação Flask
app = Flask(__name__)

# Configurações da aplicação
# Define o caminho para o nosso banco de dados SQLite
app.config['SQLALCHEMY_DATABASE_URI'] = \
    'sqlite:///' + os.path.join(basedir, 'instance', 'receitas.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Cria a pasta 'instance' se ela não existir
instance_path = os.path.join(basedir, 'instance')
if not os.path.exists(instance_path):
    os.makedirs(instance_path)

# Inicializa a extensão SQLAlchemy
db = SQLAlchemy(app)

# Importa os modelos DEPOIS de inicializar 'db'
from flask import render_template, request, redirect, url_for
from models import Chef, PerfilChef, Receita, Ingrediente, ReceitaIngrediente

@app.route('/')
def index():
    receitas = Receita.query.all()
    return render_template('index.html', receitas=receitas)

@app.route('/receita/nova', methods=['GET', 'POST'])
def criar_receita():
    if request.method == 'POST':
        # 1. Pega os dados básicos
        titulo = request.form['titulo']
        instrucoes = request.form['instrucoes']
        chef_id = request.form['chef_id']

        # 2. Cria o objeto Receita
        nova_receita = Receita(titulo=titulo, instrucoes=instrucoes, chef_id=chef_id)
        db.session.add(nova_receita)

        # 3. Processa a string de ingredientes
        ingredientes_str = request.form['ingredientes']
        pares_ingredientes = [par.strip() for par in ingredientes_str.split(',') if par.strip()]
        
        for par in pares_ingredientes:
            if ':' in par:
                nome, qtd = par.split(':', 1)
                nome_ingrediente = nome.strip().lower()
                quantidade = qtd.strip()

                # Encontra ou cria o ingrediente
                ingrediente = Ingrediente.query.filter_by(nome=nome_ingrediente).first()
                if not ingrediente:
                    ingrediente = Ingrediente(nome=nome_ingrediente)
                    db.session.add(ingrediente)
                
                # Cria a associação com a quantidade
                associacao = ReceitaIngrediente(receita=nova_receita, ingrediente=ingrediente, quantidade=quantidade)
                db.session.add(associacao)
        
        db.session.commit()
        return redirect(url_for('index'))

    # Se for GET, apenas mostra o formulário
    chefs = Chef.query.all()
    return render_template('criar_receita.html', chefs=chefs)

@app.route('/chef/<int:chef_id>')
def detalhes_chef(chef_id):
    chef = Chef.query.get_or_404(chef_id)
    return render_template('detalhes_chef.html', chef=chef)

# Bloco para executar a aplicação
if __name__ == '__main__':
    app.run(debug=True)


# --- Comandos CLI ---

@app.cli.command('init-db')
def init_db_command():
    """Cria as tabelas e popula com dados de exemplo."""
    db.drop_all()
    db.create_all()

    # Criar Chefs e Perfis
    chef1 = Chef(nome='Ana Maria')
    perfil1 = PerfilChef(especialidade='Culinária Brasileira', anos_experiencia=25, chef=chef1)
    chef2 = Chef(nome='Érick Jacquin')
    perfil2 = PerfilChef(especialidade='Culinária Francesa', anos_experiencia=30, chef=chef2)

    # Criar Ingredientes
    ingredientes = {
        'tomate': Ingrediente(nome='tomate'), 'cebola': Ingrediente(nome='cebola'),
        'farinha': Ingrediente(nome='farinha'), 'ovo': Ingrediente(nome='ovo'),
        'manteiga': Ingrediente(nome='manteiga')
    }
    
    db.session.add_all([chef1, chef2] + list(ingredientes.values()))

    # Criar Receitas
    receita1 = Receita(titulo='Molho de Tomate Clássico', instrucoes='...', chef=chef1)
    receita2 = Receita(titulo='Bolo Simples', instrucoes='...', chef=chef1)
    receita3 = Receita(titulo='Petit Gâteau', instrucoes='...', chef=chef2)
    db.session.add_all([receita1, receita2, receita3])

    # Criar Associações com Quantidade
    db.session.add_all([
        ReceitaIngrediente(receita=receita1, ingrediente=ingredientes['tomate'], quantidade='5 unidades'),
        ReceitaIngrediente(receita=receita1, ingrediente=ingredientes['cebola'], quantidade='1 unidade'),
        ReceitaIngrediente(receita=receita2, ingrediente=ingredientes['farinha'], quantidade='2 xícaras'),
        ReceitaIngrediente(receita=receita2, ingrediente=ingredientes['ovo'], quantidade='3 unidades'),
        ReceitaIngrediente(receita=receita3, ingrediente=ingredientes['manteiga'], quantidade='150g')
    ])
    
    db.session.commit()
    print('Banco de dados inicializado com sucesso!')