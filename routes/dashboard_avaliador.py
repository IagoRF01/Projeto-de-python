from flask import render_template, session
from database import app
from models import Usuario, Trabalho
from routes.auth import login_required


@app.route("/dashboard-avaliador")
@login_required(perfil="avaliador")
def dashboard_avaliador():
    usuario = Usuario.query.get(session["usuario_id"])

    # Todos os alunos (para o select do modal)
    alunos = Usuario.query.filter_by(tipo_usuario="aluno").all()

    # Trabalhos deste avaliador
    todos_trabalhos = Trabalho.query.filter_by(
        avaliador_id=session["usuario_id"]
    ).order_by(Trabalho.criado_em.desc()).all()

    # Mapa aluno_id → nome
    todos_usuarios = Usuario.query.all()
    nomes_alunos = {u.id: u.nome for u in todos_usuarios}

    return render_template(
        "dashboard_avaliador.html",
        usuario=usuario,
        alunos=alunos,
        todos_trabalhos=todos_trabalhos,
        trabalhos_pendentes=[t for t in todos_trabalhos if t.status == "pendente"],
        trabalhos_em_avaliacao=[t for t in todos_trabalhos if t.status == "em_avaliacao"],
        alunos_nomes=nomes_alunos,
    )