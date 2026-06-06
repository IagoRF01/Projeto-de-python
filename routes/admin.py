from flask import render_template, request, redirect, url_for, flash, session
from database import app, db
from models import Usuario
from routes.auth import login_required
from werkzeug.security import generate_password_hash
import uuid


PERFIS_VALIDOS = {"aluno", "avaliador"}


@app.route("/criar-usuario", methods=["GET", "POST"])
@login_required(perfil="admin")
def criar_usuario():

    if request.method == "POST":
        nome         = request.form.get("nome", "").strip()
        email        = request.form.get("email", "").strip().lower()
        senha        = request.form.get("senha", "")
        tipo_usuario = request.form.get("tipo_usuario", "")

        # ── Validações ─────────────────────────────────────────
        if not nome or not email or not senha or not tipo_usuario:
            flash("Preencha todos os campos.", "erro")
            return redirect(url_for("criar_usuario"))

        if tipo_usuario not in PERFIS_VALIDOS:
            flash("Tipo de usuário inválido.", "erro")
            return redirect(url_for("criar_usuario"))

        if len(senha) < 6:
            flash("A senha deve ter pelo menos 6 caracteres.", "erro")
            return redirect(url_for("criar_usuario"))

        # Verifica se email já existe
        if Usuario.query.filter_by(email=email).first():
            flash("Este e-mail já está cadastrado.", "erro")
            return redirect(url_for("criar_usuario"))

        # ── Cria o usuário ─────────────────────────────────────
        novo = Usuario(
            id=str(uuid.uuid4()),
            nome=nome,
            email=email,
            senha=generate_password_hash(senha),
            tipo_usuario=tipo_usuario,
        )

        db.session.add(novo)
        db.session.commit()

        flash(f"Usuário {nome} criado com sucesso!", "sucesso")
        return redirect(url_for("dashboard_admin"))

    return render_template("criar_usuario.html")