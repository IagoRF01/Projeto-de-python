from flask import request, session

from database import app

@app.route('/avaliacao', methods=['POST'])
def avaliacao():

    if 'usuario_id' not in session:
        return "Acesso negado!"

    if session['tipo'] != 'avaliador':
        return "Apenas avaliadores podem registrar avaliações"

    originalidade = request.form.get('originalidade')
    clareza = request.form.get('clareza')
    metodologia = request.form.get('metodologia')
    relevancia = request.form.get('relevancia')
    organizacao = request.form.get('organizacao')
    comentario = request.form.get('comentario')

    if not all([originalidade, clareza, metodologia, relevancia, organizacao]):
        return "Preencha todas as notas!"

    # aqui ainda não tem banco de Avaliação, então só simula
    return f"""
    Avaliação registrada com sucesso!

    Originalidade: {originalidade}
    Clareza: {clareza}
    Metodologia: {metodologia}
    Relevância: {relevancia}
    Organização: {organizacao}
    Comentário: {comentario}
    """