from flask import session

from database import app
from models import Usuario

@app.route('/dashboard/admin')
def dashboard_admin():

    if 'usuario_id' not in session:
        return "Acesso negado!"

    if session['tipo'] != 'admin':
        return "Apenas administradores podem acessar este painel"

    total_usuarios = Usuario.query.count()
    total_alunos = Usuario.query.filter_by(tipo_usuario='aluno').count()
    total_avaliadores = Usuario.query.filter_by(tipo_usuario='avaliador').count()

    # ainda não existem tabelas de trabalho/avaliação no seu sistema
    total_trabalhos = 0
    trabalhos_em_avaliacao = 0
    trabalhos_avaliados = 0
    avaliacoes_pendentes = 0

    return f"""
    ===== DASHBOARD ADMIN =====

    USUÁRIOS:
    Total de usuários: {total_usuarios}
    Alunos: {total_alunos}
    Avaliadores: {total_avaliadores}

    TRABALHOS:
    Total enviados: {total_trabalhos}
    Em avaliação: {trabalhos_em_avaliacao}
    Avaliados: {trabalhos_avaliados}

    AVALIAÇÕES:
    Pendentes: {avaliacoes_pendentes}
    """