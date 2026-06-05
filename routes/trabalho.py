from flask import render_template, request, redirect, session
from database import app, db
from models import Trabalho

@app.route("/novo-trabalho", methods=["GET", "POST"])
def novo_trabalho():

    if "usuario_id" not in session:
        return "Acesso negado"

    if request.method == "POST":

        trabalho = Trabalho(
            titulo=request.form.get("titulo"),
            resumo=request.form.get("resumo"),
            status="pendente",
            aluno_id=session["usuario_id"]
        )

        db.session.add(trabalho)
        db.session.commit()

        return redirect("/dashboard-aluno")

    return render_template("novo_trabalho.html")