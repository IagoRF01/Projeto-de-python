from flask import render_template, session, redirect, url_for, flash
from database import app, db
from models import Usuario, Trabalho
from routes.auth import login_required


@app.route("/dashboard-admin")
@login_required(perfil="admin")
def dashboard_admin():
    usuario = Usuario.query.get(session["usuario_id"])

    # ── Usuários ───────────────────────────────────────────────
    alunos      = Usuario.query.filter_by(tipo_usuario="aluno").all()
    avaliadores = Usuario.query.filter_by(tipo_usuario="avaliador").all()

    # ── Trabalhos ──────────────────────────────────────────────
    todos_trabalhos = Trabalho.query.order_by(Trabalho.criado_em.desc()).all()

    pendentes     = [t for t in todos_trabalhos if t.status == "pendente"]
    em_avaliacao  = [t for t in todos_trabalhos if t.status == "em_avaliacao"]
    avaliados     = [t for t in todos_trabalhos if t.status in ("aprovado", "rejeitado")]

    # ── Mapa de nomes (aluno_id e avaliador_id → nome) ────────
    todos_usuarios = Usuario.query.all()
    nomes = {u.id: u.nome for u in todos_usuarios}

    return render_template(
        "dashboard_admin.html",
        usuario=usuario,
        alunos=alunos,
        avaliadores=avaliadores,
        todos_trabalhos=todos_trabalhos,
        total_avaliacoes=len(avaliados),
        total_pendentes=len(pendentes),
        total_em_avaliacao=len(em_avaliacao),
        nomes=nomes,
    ) 
@app.route("/remover-usuario/<usuario_id>", methods=["POST"])
@login_required(perfil="admin")
def remover_usuario(usuario_id):

    usuario = Usuario.query.get(usuario_id)

    if not usuario:
        flash("Usuário não encontrado.", "erro")
        return redirect(url_for("dashboard_admin"))

    db.session.delete(usuario)
    db.session.commit()

    flash("Usuário removido com sucesso!", "sucesso")
    return redirect(url_for("dashboard_admin"))
