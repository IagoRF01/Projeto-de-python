from flask import render_template, session, redirect, url_for
from database import app
from models import Usuario, Trabalho
from routes.auth import login_required


@app.route("/dashboard-aluno")
@login_required(perfil="aluno")
def dashboard_aluno():
    usuario = Usuario.query.get(session["usuario_id"])

    trabalhos = Trabalho.query.filter_by(aluno_id=session["usuario_id"]).all()

    return render_template(
        "dashboard_aluno.html",
        usuario=usuario,
        trabalhos=trabalhos
    )