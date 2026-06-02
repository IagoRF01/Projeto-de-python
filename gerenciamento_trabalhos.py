from flask import request

from database import app
from models import Trabalho


# =========================
# LISTAR TRABALHOS
# =========================
@app.route("/trabalhos", methods=["GET"])
def listar_trabalhos():

    status = request.args.get("status")

    if status:
        trabalhos = Trabalho.query.filter_by(status=status).all()
    else:
        trabalhos = Trabalho.query.all()

    resultado = []

    for trabalho in trabalhos:
        resultado.append({
            "id": trabalho.id,
            "titulo": trabalho.titulo,
            "status": trabalho.status,
            "aluno_id": trabalho.aluno_id,
            "avaliador_id": trabalho.avaliador_id
        })

    return {"trabalhos": resultado}


# =========================
# DETALHES DO TRABALHO
# =========================
@app.route("/trabalhos/<trabalho_id>", methods=["GET"])
def visualizar_trabalho(trabalho_id):

    trabalho = Trabalho.query.get(trabalho_id)

    if not trabalho:
        return {"erro": "Trabalho não encontrado"}

    return {
        "id": trabalho.id,
        "titulo": trabalho.titulo,
        "resumo": trabalho.resumo,
        "palavras_chave": trabalho.palavras_chave,
        "arquivo_url": trabalho.arquivo_url,
        "status": trabalho.status,
        "aluno_id": trabalho.aluno_id,
        "avaliador_id": trabalho.avaliador_id
    }


# =========================
# ALTERAR STATUS
# =========================
@app.route("/trabalhos/<trabalho_id>/status", methods=["PUT"])
def alterar_status(trabalho_id):

    trabalho = Trabalho.query.get(trabalho_id)

    if not trabalho:
        return {"erro": "Trabalho não encontrado"}

    novo_status = request.form.get("status")

    trabalho.status = novo_status

    from database import db
    db.session.commit()

    return {"mensagem": "Status atualizado com sucesso"}


# =========================
# VISUALIZAR ARQUIVO
# =========================
@app.route("/trabalhos/<trabalho_id>/arquivo", methods=["GET"])
def visualizar_arquivo(trabalho_id):

    trabalho = Trabalho.query.get(trabalho_id)

    if not trabalho:
        return {"erro": "Trabalho não encontrado"}

    return {
        "arquivo_url": trabalho.arquivo_url
    }


# =========================
# VISUALIZAR AVALIAÇÕES
# =========================
@app.route("/trabalhos/<trabalho_id>/avaliacoes", methods=["GET"])
def visualizar_avaliacoes(trabalho_id):

    return {
        "mensagem": "Funcionalidade preparada para exibir avaliações relacionadas ao trabalho."
    }