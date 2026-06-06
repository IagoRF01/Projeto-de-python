from flask import render_template, request, redirect, url_for, flash, session
from database import app, db
from models import Trabalho, Avaliacao, Usuario
from routes.auth import login_required
import uuid


@app.route("/avaliar/<trabalho_id>", methods=["GET", "POST"])
@login_required(perfil="avaliador")
def avaliar_trabalho(trabalho_id):
    trabalho = Trabalho.query.get(trabalho_id)

    # Trabalho não existe ou não pertence a este avaliador
    if not trabalho or trabalho.avaliador_id != session["usuario_id"]:
        flash("Trabalho não encontrado.", "erro")
        return redirect(url_for("dashboard_avaliador"))

    # Busca avaliação existente (se já avaliou antes)
    avaliacao = Avaliacao.query.filter_by(
        trabalho_id=trabalho_id,
        avaliador_id=session["usuario_id"]
    ).first()

    # Nome do aluno (anonimato: só mostra se admin, aqui é avaliador então esconde)
    aluno = Usuario.query.get(trabalho.aluno_id)
    nome_aluno = "Autor Anônimo"  # RF09 — anonimato

    if request.method == "POST":
        nota       = request.form.get("nota", "").strip()
        comentario = request.form.get("comentario", "").strip()
        acao       = request.form.get("acao", "salvar")  # 'salvar' ou 'finalizar'

        # ── Validações ─────────────────────────────────────────
        if not nota:
            flash("Informe a nota.", "erro")
            return redirect(url_for("avaliar_trabalho", trabalho_id=trabalho_id))

        try:
            nota_float = float(nota)
            if not (0 <= nota_float <= 10):
                raise ValueError
        except ValueError:
            flash("Nota deve ser um número entre 0 e 10.", "erro")
            return redirect(url_for("avaliar_trabalho", trabalho_id=trabalho_id))

        # ── Salva ou atualiza avaliação ────────────────────────
        if avaliacao:
            avaliacao.nota       = nota_float
            avaliacao.comentario = comentario
            avaliacao.status     = "Finalizado" if acao == "finalizar" else "Pendente"
        else:
            avaliacao = Avaliacao(
                id=str(uuid.uuid4()),
                trabalho_id=trabalho_id,
                avaliador_id=session["usuario_id"],
                nota=nota_float,
                comentario=comentario,
                status="Finalizado" if acao == "finalizar" else "Pendente",
            )
            db.session.add(avaliacao)

        # ── Atualiza status do trabalho ────────────────────────
        if acao == "finalizar":
            trabalho.status = "aprovado" if nota_float >= 5 else "rejeitado"
            flash("Avaliação finalizada com sucesso!", "sucesso")
        else:
            flash("Avaliação salva como rascunho.", "sucesso")

        db.session.commit()
        return redirect(url_for("dashboard_avaliador"))

    return render_template(
        "avaliar_trabalho.html",
        trabalho=trabalho,
        avaliacao=avaliacao,
        nome_aluno=nome_aluno,
    )