from flask import request, session
from werkzeug.security import generate_password_hash

from database import app, db
from models import Usuario


# =========================
# LISTAR USUÁRIOS
# =========================
@app.route("/usuarios", methods=["GET"])
def listar_usuarios():

    tipo = request.args.get("tipo")

    if tipo:
        usuarios = Usuario.query.filter_by(tipo_usuario=tipo).all()
    else:
        usuarios = Usuario.query.all()

    resultado = []

    for usuario in usuarios:
        resultado.append({
            "id": usuario.id,
            "nome": usuario.nome,
            "email": usuario.email,
            "tipo_usuario": usuario.tipo_usuario,
            "ativo": usuario.ativo
        })

    return {"usuarios": resultado}


# =========================
# CRIAR USUÁRIO
# =========================
@app.route("/usuarios/criar", methods=["POST"])
def criar_usuario():

    nome = request.form.get("nome")
    email = request.form.get("email")
    senha = request.form.get("senha")
    tipo_usuario = request.form.get("tipo_usuario")
    matricula = request.form.get("matricula")

    senha_hash = generate_password_hash(senha)

    novo_usuario = Usuario(
        nome=nome,
        email=email,
        senha=senha_hash,
        tipo_usuario=tipo_usuario,
        matricula=matricula
    )

    db.session.add(novo_usuario)
    db.session.commit()

    return {"mensagem": "Usuário criado com sucesso"}


# =========================
# EDITAR USUÁRIO
# =========================
@app.route("/usuarios/<usuario_id>/editar", methods=["PUT"])
def editar_usuario(usuario_id):

    usuario = Usuario.query.get(usuario_id)

    if not usuario:
        return {"erro": "Usuário não encontrado"}

    usuario.nome = request.form.get("nome", usuario.nome)
    usuario.email = request.form.get("email", usuario.email)
    usuario.matricula = request.form.get("matricula", usuario.matricula)

    db.session.commit()

    return {"mensagem": "Usuário atualizado com sucesso"}


# =========================
# ALTERAR PERFIL
# =========================
@app.route("/usuarios/<usuario_id>/perfil", methods=["PUT"])
def alterar_perfil(usuario_id):

    usuario = Usuario.query.get(usuario_id)

    if not usuario:
        return {"erro": "Usuário não encontrado"}

    usuario.tipo_usuario = request.form.get(
        "tipo_usuario",
        usuario.tipo_usuario
    )

    db.session.commit()

    return {"mensagem": "Perfil alterado com sucesso"}


# =========================
# ATIVAR/DESATIVAR USUÁRIO
# =========================
@app.route("/usuarios/<usuario_id>/status", methods=["PUT"])
def alterar_status(usuario_id):

    usuario = Usuario.query.get(usuario_id)

    if not usuario:
        return {"erro": "Usuário não encontrado"}

    usuario.ativo = not usuario.ativo

    db.session.commit()

    return {
        "mensagem": "Status atualizado com sucesso",
        "ativo": usuario.ativo
    }