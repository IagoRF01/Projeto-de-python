from flask import request, redirect, url_for, flash, session
from database import app, db
from models import Trabalho, Usuario
from routes.auth import login_required
from datetime import datetime
from zoneinfo import ZoneInfo
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

    # ── Prazo com ajuste de Fuso Horário ───────────────────────
    prazo = None
    if prazo_envio:
        try:
            # 1. Faz o parse da string enviada pelo formulário html
            prazo_local = datetime.strptime(prazo_envio, "%Y-%m-%dT%H:%M")
            
            # 2. Define que esse horário pertence ao fuso de Brasília/São Paulo
            fuso_local = ZoneInfo("America/Sao_Paulo")
            prazo_com_fuso = prazo_local.replace(tzinfo=fuso_local)
            
            # 3. Converte para UTC antes de salvar no banco de dados
            prazo = prazo_com_fuso.astimezone(ZoneInfo("UTC"))
            
        except ValueError:
            flash("Formato de prazo inválido.", "erro")
            return redirect(url_for("dashboard_avaliador"))

    # ── Envio para todos os alunos ────────────────────────────
    if aluno_id == "TODOS":

        alunos = Usuario.query.filter_by(
            tipo_usuario="aluno"
        ).all()

        if not alunos:
            flash("Nenhum aluno encontrado.", "erro")
            return redirect(url_for("dashboard_avaliador"))

        for aluno in alunos:

            trabalho = Trabalho(
                id=str(uuid.uuid4()),
                titulo=f"[ANONIMO] {titulo}",
                resumo=resumo,
                status="pendente",
                aluno_id=aluno.id,
                avaliador_id=session["usuario_id"],
                prazo_envio=prazo,
            )

            db.session.add(trabalho)

        db.session.commit()

        flash(
            f"Trabalho '{titulo}' enviado para todos os alunos!",
            "sucesso"
        )

        return redirect(url_for("dashboard_avaliador"))

    # ── Validação do aluno individual ─────────────────────────
    aluno = Usuario.query.filter_by(
        id=aluno_id,
        tipo_usuario="aluno"
    ).first()

    if not aluno:
        flash("Estudante inválido.", "erro")
        return redirect(url_for("dashboard_avaliador"))

    # ── Cria o trabalho individual ────────────────────────────
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

    flash(
        f"Trabalho '{titulo}' criado e enviado para {aluno.nome}!",
        "sucesso"
    )

    return redirect(url_for("dashboard_avaliador"))
