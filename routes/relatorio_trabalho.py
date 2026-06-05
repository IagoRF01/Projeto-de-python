from flask import (
    render_template,
    session
)

from database import app

from models import (
    Trabalho,
    Usuario,
    Avaliacao
)


@app.route(
    '/relatorio/<trabalho_id>'
)
def relatorio_trabalho(
    trabalho_id
):

    if 'usuario_id' not in session:
        return "Acesso negado!"

    trabalho = (
        Trabalho.query
        .get_or_404(trabalho_id)
    )

    aluno = (
        Usuario.query
        .get(trabalho.aluno_id)
    )

    avaliacoes = (
        Avaliacao.query
        .filter_by(
            trabalho_id=trabalho.id
        )
        .all()
    )

    return render_template(
        'relatorio_trabalho.html',
        trabalho=trabalho,
        aluno=aluno,
        avaliacoes=avaliacoes
    )