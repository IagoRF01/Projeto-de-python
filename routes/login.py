from flask import render_template, request, redirect, url_for, session
from database import app
from models import Usuario
from werkzeug.security import check_password_hash


@app.route("/login/<perfil>")
def login_page(perfil):
    return render_template("login.html", perfil=perfil)


@app.route("/login", methods=["POST"])
def login():

    email = request.form.get("email")
    senha = request.form.get("senha")

    usuario = Usuario.query.filter_by(email=email).first()

    if not usuario:
        return "Usuário não encontrado"

    if not check_password_hash(usuario.senha, senha):
        return "Senha inválida"

    session["usuario_id"] = usuario.id
    session["tipo"] = usuario.tipo_usuario

    if usuario.tipo_usuario == "aluno":
        return redirect(url_for("dashboard_aluno"))

    if usuario.tipo_usuario == "avaliador":
        return redirect(url_for("dashboard_avaliador"))

    if usuario.tipo_usuario == "admin":
        return redirect(url_for("dashboard_indicadores"))

    return "Tipo inválido"