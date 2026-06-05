from flask import (
    request,
    session,
    redirect
)

from database import app, db

from models import (
    Trabalho,
    Avaliacao
)


@app.route(
    '/avaliacao/<trabalho_id>',
    methods=['POST']
)
def salvar_avaliacao(
    trabalho_id
):

    # =====================
    # VALIDA LOGIN
    # =====================

    if 'usuario_id' not in session:
        return "Acesso negado!"

    if session['tipo'] != 'avaliador':
        return (
            "Apenas avaliadores "
            "podem avaliar trabalhos."
        )

    # =====================
    # RECEBE DADOS
    # =====================

    originalidade = request.form.get(
        'originalidade'
    )

    clareza = request.form.get(
        'clareza'
    )

    metodologia = request.form.get(
        'metodologia'
    )

    relevancia = request.form.get(
        'relevancia'
    )

    organizacao = request.form.get(
        'organizacao'
    )

    comentario = request.form.get(
        'comentario'
    )

    # =====================
    # VALIDA CAMPOS
    # =====================

    if not all([
        originalidade,
        clareza,
        metodologia,
        relevancia,
        organizacao
    ]):
        return (
            "Preencha todas "
            "as notas."
        )

    trabalho = (
        Trabalho.query
        .get_or_404(trabalho_id)
    )

    # =====================
    # CRIA AVALIAÇÃO
    # =====================

    avaliacao = Avaliacao(

        trabalho_id=
        trabalho.id,

        avaliador_id=
        session['usuario_id'],

        originalidade=
        float(originalidade),

        clareza=
        float(clareza),

        metodologia=
        float(metodologia),

        relevancia=
        float(relevancia),

        organizacao=
        float(organizacao),

        comentario=
        comentario
    )

    db.session.add(
        avaliacao
    )

    # =====================
    # ATUALIZA STATUS
    # =====================

    trabalho.status = (
        'avaliado'
    )

    db.session.commit()

    return redirect(
        '/painel'
    )