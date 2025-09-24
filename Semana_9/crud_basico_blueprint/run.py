from crud_app import create_app

# Cria a aplicação chamando a nossa factory
app = create_app()

if __name__ == '__main__':
    # Roda o servidor de desenvolvimento do Flask
    app.run(debug=True)