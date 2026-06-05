from flask import render_template, session
from database import app
from models import Trabalho

@app.route("/dashboard-aluno")
def dashboard_aluno():

    print("DASHBOARD ALUNO FOI CHAMADO")

    if "usuario_id" not in session:
        return "Acesso negado"

    user_id = session["usuario_id"]
    print("USER ID:", user_id)

    trabalhos = Trabalho.query.filter_by(aluno_id=user_id).all()

    return render_template(
        "dashboard_aluno.html",
        trabalhos=trabalhos
    )