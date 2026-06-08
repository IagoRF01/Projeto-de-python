from flask import request, redirect, url_for, flash, session
from database import app, db
from models import Trabalho, Usuario
from routes.auth import login_required
from datetime import datetime
import uuid


@app.route("/criar-trabalho", methods=["POST"])
@login_required(perfil="avaliador")
def criar_trabalho():
    titulo      = request.form.get("titulo", "").strip()
    resumo      = request.form.get("resumo", "").strip()
    aluno_id    = request.form.get("aluno_id", "").strip()
    prazo_envio = request.form.get("prazo_envio", "").strip()

    # ── Validações ─────────────────────────────────────────────
    if not titulo or not resumo or not aluno_id:
        flash("Preencha título, descrição e selecione um estudante.", "erro")
        return redirect(url_for("dashboard_avaliador"))

    aluno = Usuario.query.filter_by(id=aluno_id, tipo_usuario="aluno").first()
    if not aluno:
        flash("Estudante inválido.", "erro")
        return redirect(url_for("dashboard_avaliador"))

    # ── Prazo (opcional) ───────────────────────────────────────
    prazo = None
    if prazo_envio:
        try:
            prazo = datetime.strptime(prazo_envio, "%Y-%m-%dT%H:%M")
        except ValueError:
            flash("Formato de prazo inválido.", "erro")
            return redirect(url_for("dashboard_avaliador"))

    # ── Cria o trabalho ────────────────────────────────────────
    trabalho = Trabalho(
        id=str(uuid.uuid4()),
        titulo=titulo,
        resumo=resumo,
        status="pendente",
        aluno_id=aluno_id,
        avaliador_id=session["usuario_id"],
        prazo_envio=prazo,
    )

    db.session.add(trabalho)
    db.session.commit()

    flash(f"Trabalho '{titulo}' criado e enviado para {aluno.nome}!", "sucesso")
    return redirect(url_for("dashboard_avaliador"))