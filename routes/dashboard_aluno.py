from flask import render_template, session
from database import app
from models import Usuario, Trabalho, Avaliacao
from routes.auth import login_required
from datetime import datetime


@app.route("/dashboard-aluno")
@login_required(perfil="aluno")
def dashboard_aluno():
    usuario   = Usuario.query.get(session["usuario_id"])
    trabalhos = Trabalho.query.filter_by(aluno_id=session["usuario_id"]).all()

    # Mapa avaliador_id → nome
    nomes_avaliadores = {}
    for t in trabalhos:
        if t.avaliador_id and t.avaliador_id not in nomes_avaliadores:
            av = Usuario.query.get(t.avaliador_id)
            nomes_avaliadores[t.avaliador_id] = av.nome if av else "—"

    # Tempo restante por trabalho
    agora = datetime.utcnow()
    tempo_restante = {}
    for t in trabalhos:
        if t.prazo_envio:
            delta = t.prazo_envio - agora
            if delta.total_seconds() > 0:
                tempo_restante[t.id] = f"{delta.days} dias e {delta.seconds // 3600} horas"
            else:
                tempo_restante[t.id] = "Prazo encerrado"
        else:
            tempo_restante[t.id] = None

    # Avaliações por trabalho_id
    avaliacoes = {}
    for t in trabalhos:
        av = Avaliacao.query.filter_by(trabalho_id=t.id).first()
        if av:
            avaliacoes[t.id] = av

    return render_template(
        "dashboard_aluno.html",
        usuario=usuario,
        trabalhos=trabalhos,
        nomes_avaliadores=nomes_avaliadores,
        tempo_restante=tempo_restante,
        avaliacoes=avaliacoes,
        now=datetime.utcnow(),
    )