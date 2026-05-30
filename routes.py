from flask import render_template, redirect, request
from database import app, db
from models import Trabalho
import uuid


@app.route("/")
def dashboard():
    trabalhos = Trabalho.query.all()
    return render_template("dashboard.html", trabalhos=trabalhos)


@app.route("/trabalho/<id>")
def visualizar_trabalho(id):
    trabalho = Trabalho.query.get(id)
    return render_template("trabalho.html", trabalho=trabalho)


@app.route("/criar_trabalho", methods=["GET", "POST"])
def criar_trabalho():
    if request.method == "POST":

        titulo = request.form["titulo"]
        resumo = request.form["resumo"]

        novo = Trabalho(
            id=str(uuid.uuid4()),
            titulo=titulo,
            resumo=resumo,
            status="Enviado",
            aluno_id="11111111-1111-1111-1111-111111111111"
        )

        db.session.add(novo)
        db.session.commit()

        return redirect("/")

    return render_template("criar_trabalho.html")