from flask import render_template, request, redirect, url_for, session, flash
from database import app
from models import Usuario
from werkzeug.security import check_password_hash

PERFIS_VALIDOS = {"aluno", "avaliador", "admin"}

PERFIL_LABELS = {
    "aluno":     "Aluno",
    "avaliador": "Avaliador",
    "admin":     "Administrador",
}


# ── Página de login por perfil ─────────────────────────────────
@app.route("/login/<perfil>")
def login_page(perfil):
    if perfil not in PERFIS_VALIDOS:
        return redirect(url_for("home"))

    # Se já está logado, manda para o dashboard correto
    if "usuario_id" in session:
        tipo = session.get("tipo")
        if tipo == "aluno":
            return redirect(url_for("dashboard_aluno"))
        if tipo == "avaliador":
            return redirect(url_for("dashboard_avaliador"))
        if tipo == "admin":
            return redirect(url_for("dashboard_admin"))

    return render_template(
        "login.html",
        perfil=perfil,
        perfil_label=PERFIL_LABELS[perfil]
    )


# ── Processar login ────────────────────────────────────────────
@app.route("/login/<perfil>", methods=["POST"])
def login(perfil):
    if perfil not in PERFIS_VALIDOS:
        return redirect(url_for("home"))

    email = request.form.get("email", "").strip().lower()
    senha = request.form.get("senha", "")

    # Campos vazios
    if not email or not senha:
        flash("Preencha e-mail e senha.", "erro")
        return redirect(url_for("login_page", perfil=perfil))

    # Busca usuário pelo e-mail E pelo tipo (impede aluno logar como avaliador)
    usuario = Usuario.query.filter_by(
        email=email,
        tipo_usuario=perfil
    ).first()

    if not usuario or not check_password_hash(usuario.senha, senha):
        flash("E-mail ou senha inválidos.", "erro")
        return redirect(url_for("login_page", perfil=perfil))

    # Salva na sessão
    session.clear()
    session["usuario_id"] = usuario.id
    session["usuario_nome"] = usuario.nome
    session["tipo"] = usuario.tipo_usuario

    # Redireciona para o dashboard do perfil
    if usuario.tipo_usuario == "aluno":
        return redirect(url_for("dashboard_aluno"))
    if usuario.tipo_usuario == "avaliador":
        return redirect(url_for("dashboard_avaliador"))
    if usuario.tipo_usuario == "admin":
        return redirect(url_for("dashboard_admin"))

    return redirect(url_for("home"))


# ── Logout ─────────────────────────────────────────────────────
@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("home"))