from flask import render_template, session

from database import app
from models import Trabalho, Usuario


@app.route('/dashboard-indicadores')
def dashboard_indicadores():

    if 'usuario_id' not in session:
        return "Acesso negado!"

    total_trabalhos = Trabalho.query.count()

    trabalhos_em_avaliacao = (
        Trabalho.query.filter_by(
            status='em_avaliacao'
        ).count()
    )

    trabalhos_avaliados = (
        Trabalho.query.filter_by(
            status='avaliado'
        ).count()
    )

    avaliacoes_pendentes = (
        Trabalho.query.filter_by(
            status='em_avaliacao'
        ).count()
    )

    total_alunos = (
        Usuario.query.filter_by(
            tipo_usuario='aluno'
        ).count()
    )

    total_avaliadores = (
        Usuario.query.filter_by(
            tipo_usuario='avaliador'
        ).count()
    )

    total_admins = (
        Usuario.query.filter_by(
            tipo_usuario='admin'
        ).count()
    )

    media_geral = "N/D"

    return render_template(
        'dashboard_indicadores.html',

        total_trabalhos=total_trabalhos,

        trabalhos_em_avaliacao=
        trabalhos_em_avaliacao,

        trabalhos_avaliados=
        trabalhos_avaliados,

        avaliacoes_pendentes=
        avaliacoes_pendentes,

        media_geral=media_geral,

        total_alunos=total_alunos,

        total_avaliadores=
        total_avaliadores,

        total_admins=total_admins
    )