from flask import request, redirect, url_for, flash, session
from database import app, db
from models import Trabalho, Avaliacao, Usuario
from routes.auth import login_required
import uuid


@app.route("/avaliar/<trabalho_id>", methods=["GET", "POST"])
@login_required(perfil="avaliador")
def avaliar_trabalho(trabalho_id):
    trabalho  = Trabalho.query.get(trabalho_id)

    if not trabalho or trabalho.avaliador_id != session["usuario_id"]:
        flash("Trabalho não encontrado.", "erro")
        return redirect(url_for("dashboard_avaliador"))

    avaliacao = Avaliacao.query.filter_by(
        trabalho_id=trabalho_id,
        avaliador_id=session["usuario_id"]
    ).first()

    if request.method == "POST":
        # Lê os sliders
        try:
            relevancia    = float(request.form.get("relevancia", 7))
            metodologia   = float(request.form.get("metodologia", 7))
            clareza       = float(request.form.get("clareza", 7))
            originalidade = float(request.form.get("originalidade", 7))
        except ValueError:
            flash("Valores de critérios inválidos.", "erro")
            return redirect(url_for("dashboard_avaliador"))

        comentario = request.form.get("comentario", "").strip()

        # Média automática dos 4 critérios
        nota = round((relevancia + metodologia + clareza + originalidade) / 4, 2)

        if avaliacao:
            avaliacao.relevancia    = relevancia
            avaliacao.metodologia   = metodologia
            avaliacao.clareza       = clareza
            avaliacao.originalidade = originalidade
            avaliacao.nota          = nota
            avaliacao.comentario    = comentario
            avaliacao.status        = "Finalizado"
        else:
            avaliacao = Avaliacao(
                id=str(uuid.uuid4()),
                trabalho_id=trabalho_id,
                avaliador_id=session["usuario_id"],
                relevancia=relevancia,
                metodologia=metodologia,
                clareza=clareza,
                originalidade=originalidade,
                nota=nota,
                comentario=comentario,
                status="Finalizado",
            )
            db.session.add(avaliacao)

        # Atualiza status do trabalho com base na média
        trabalho.status = "aprovado" if nota >= 5 else "rejeitado"
        db.session.commit()

        flash(f"Avaliação enviada! Nota final: {nota}/10", "sucesso")
        return redirect(url_for("dashboard_avaliador"))

    # GET — renderiza o modal via redirect com parâmetro
    return redirect(url_for("dashboard_avaliador", avaliar=trabalho_id))