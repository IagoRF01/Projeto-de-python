from flask import render_template, session

from database import app, db
from models import (
    Trabalho,
    HistoricoMovimentacao
)


# ==================================
# REGISTRAR MOVIMENTAÇÃO
# ==================================
def registrar_movimentacao(
    trabalho_id,
    descricao
):

    movimentacao = (
        HistoricoMovimentacao(
            trabalho_id=trabalho_id,
            descricao=descricao
        )
    )

    db.session.add(
        movimentacao
    )

    db.session.commit()


# ==================================
# VISUALIZAR HISTÓRICO
# ==================================
@app.route(
    '/historico/<trabalho_id>'
)
def visualizar_historico(
    trabalho_id
):

    if 'usuario_id' not in session:
        return "Acesso negado!"

    trabalho = (
        Trabalho.query
        .get_or_404(trabalho_id)
    )

    historicos = (
        HistoricoMovimentacao.query
        .filter_by(
            trabalho_id=trabalho_id
        )
        .order_by(
            HistoricoMovimentacao.criado_em.desc()
        )
        .all()
    )

    return render_template(
        'historico_movimentacoes.html',
        trabalho=trabalho,
        historicos=historicos
    )