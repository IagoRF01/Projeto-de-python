from flask import render_template, session
from database import app
from models import Usuario, Trabalho
from routes.auth import login_required


@app.route("/dashboard-avaliador")
@login_required(perfil="avaliador")
def dashboard_avaliador():
    usuario = Usuario.query.get(session["usuario_id"])

    # Trabalhos pendentes — aluno submeteu mas ainda não foi para avaliação
    trabalhos_pendentes = Trabalho.query.filter_by(
        avaliador_id=session["usuario_id"],
        status="pendente"
    ).all()

    # Trabalhos em avaliação — já designados para este avaliador
    trabalhos_em_avaliacao = Trabalho.query.filter_by(
        avaliador_id=session["usuario_id"],
        status="em_avaliacao"
    ).all()

    # Todos os trabalhos deste avaliador (visão geral)
    todos_trabalhos = Trabalho.query.filter_by(
        avaliador_id=session["usuario_id"]
    ).order_by(Trabalho.criado_em.desc()).all()

    # Busca o nome do aluno para cada trabalho
    # (necessário pois o modelo não tem FK com join automático)
    alunos = {}
    for t in todos_trabalhos:
        if t.aluno_id and t.aluno_id not in alunos:
            aluno = Usuario.query.get(t.aluno_id)
            alunos[t.aluno_id] = aluno.nome if aluno else "—"

    return render_template(
        "dashboard_avaliador.html",
        usuario=usuario,
        trabalhos_pendentes=trabalhos_pendentes,
        trabalhos_em_avaliacao=trabalhos_em_avaliacao,
        todos_trabalhos=todos_trabalhos,
        alunos=alunos,
    )