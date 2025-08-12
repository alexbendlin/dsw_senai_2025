from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

# Lista que armazena as tarefas
tarefas = []

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        nome_tarefa = request.form.get("tarefa")
        data_limite = request.form.get("data")
        tarefas.append({"tarefa": nome_tarefa, "data": data_limite})
        return redirect(url_for("sucesso", tarefa=nome_tarefa))
    return render_template("index.html", tarefas=tarefas)

@app.route("/sucesso")
def sucesso():
    tarefa = request.args.get("tarefa")
    return render_template("sucesso.html", tarefa=tarefa)

if __name__ == "__main__":
    app.run(debug=True)
