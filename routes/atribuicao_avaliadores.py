from flask import render_template, request, redirect, session

from database import app, db
from models import Trabalho, Usuario


# =========================
# TELA DE ATRIBUIÇÃO
# =========================
@app.route('/atribuicao-avaliadores')
def atribuicao_avaliadores():

    if 'usuario_id' not in session:
        return "Acesso negado!"

    if session['tipo'] != 'admin':
        return "Somente administradores podem acessar esta página!"

    trabalhos = Trabalho.query.all()

    avaliadores = Usuario.query.filter_by(
        tipo_usuario='avaliador'
    ).all()

    avaliadores_dict = {
        avaliador.id: avaliador.nome
        for avaliador in avaliadores
    }

    return render_template(
        'atribuicao_avaliadores.html',
        trabalhos=trabalhos,
        avaliadores=avaliadores,
        avaliadores_dict=avaliadores_dict
    )


# =========================
# SALVAR ATRIBUIÇÃO
# =========================
@app.route(
    '/atribuir-avaliador/<trabalho_id>',
    methods=['POST']
)
def atribuir_avaliador(trabalho_id):

    if 'usuario_id' not in session:
        return "Acesso negado!"

    if session['tipo'] != 'admin':
        return "Somente administradores podem atribuir avaliadores!"

    trabalho = Trabalho.query.get_or_404(trabalho_id)

    avaliador_id = request.form.get('avaliador_id')

    if not avaliador_id:
        return "Selecione um avaliador."

    trabalho.avaliador_id = avaliador_id

    trabalho.status = 'em_avaliacao'

    db.session.commit()

    return redirect('/atribuicao-avaliadores')