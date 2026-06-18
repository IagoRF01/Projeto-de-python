import os
import uuid
from datetime import datetime
from flask import render_template, request, redirect, url_for, session, flash
from database import app, db
from models import Trabalho
from routes.auth import login_required
from supabase import create_client

# ── Cliente Supabase ───────────────────────────────────────────
SUPABASE_URL = os.environ.get("SUPABASE_URL", "https://zppeatcebobyddjpbmsv.supabase.co")
SUPABASE_KEY = os.environ.get("SUPABASE_KEY", "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InpwcGVhdGNlYm9ieWRkanBibXN2Iiwicm9sZSI6ImFub24iLCJpYXQiOjE3ODAwMTA3MjIsImV4cCI6MjA5NTU4NjcyMn0.PsugX-IJpHAvuYfpiDRiGqeypuTR0FOZjEB5o7k6lVw")

supabase = create_client(SUPABASE_URL, SUPABASE_KEY)

BUCKET               = "trabalhos"
EXTENSOES_PERMITIDAS = {"pdf", "docx"}
TAMANHO_MAXIMO       = 15 * 1024 * 1024  # 15 MB


def extensao_permitida(nome):
    return "." in nome and nome.rsplit(".", 1)[1].lower() in EXTENSOES_PERMITIDAS


def prazo_expirado(trabalho):
    """Retorna True se o prazo do trabalho já passou."""
    if not trabalho.prazo_envio:
        return False
    return datetime.utcnow() > trabalho.prazo_envio


# ── Criar novo trabalho (aluno cria do zero) ───────────────────
@app.route("/novo-trabalho", methods=["GET", "POST"])
@login_required(perfil="aluno")
def novo_trabalho():
    if request.method == "POST":
        titulo         = request.form.get("titulo", "").strip()
        resumo         = request.form.get("resumo", "").strip()
        palavras_chave = request.form.get("palavras_chave", "").strip()
        arquivo        = request.files.get("arquivo")

        if not titulo or not resumo:
            flash("Título e resumo são obrigatórios.", "erro")
            return redirect(url_for("novo_trabalho"))

        if not arquivo or arquivo.filename == "":
            flash("Selecione um arquivo PDF ou DOCX.", "erro")
            return redirect(url_for("novo_trabalho"))

        if not extensao_permitida(arquivo.filename):
            flash("Formato inválido. Envie apenas PDF ou DOCX.", "erro")
            return redirect(url_for("novo_trabalho"))

        conteudo = arquivo.read()
        if len(conteudo) > TAMANHO_MAXIMO:
            flash("Arquivo muito grande. O limite é 15 MB.", "erro")
            return redirect(url_for("novo_trabalho"))

        extensao   = arquivo.filename.rsplit(".", 1)[1].lower()
        nome_unico = f"{uuid.uuid4()}.{extensao}"
        caminho    = f"{session['usuario_id']}/{nome_unico}"

        try:
            supabase.storage.from_(BUCKET).upload(
                path=caminho,
                file=conteudo,
                file_options={"content-type": arquivo.content_type}
            )
            arquivo_url = supabase.storage.from_(BUCKET).get_public_url(caminho)
        except Exception as e:
            print("ERRO UPLOAD:", repr(e))
            flash(f"Erro: {str(e)}", "erro")
            return redirect(url_for("dashboard_aluno"))

        trabalho = Trabalho(
            titulo=titulo,
            resumo=resumo,
            palavras_chave=palavras_chave,
            arquivo_url=arquivo_url,
            status="em_avaliacao",
            aluno_id=session["usuario_id"]
        )
        db.session.add(trabalho)
        db.session.commit()

        flash("Trabalho enviado com sucesso!", "sucesso")
        return redirect(url_for("dashboard_aluno"))

    return render_template("novo_trabalho.html")


# ── Enviar arquivo em trabalho já existente (criado pelo avaliador) ──
@app.route("/enviar-arquivo/<trabalho_id>", methods=["POST"])
@login_required(perfil="aluno")
def enviar_arquivo(trabalho_id):
    trabalho = Trabalho.query.get(trabalho_id)

    # Segurança: só o aluno dono pode enviar
    if not trabalho or trabalho.aluno_id != session["usuario_id"]:
        flash("Trabalho não encontrado.", "erro")
        return redirect(url_for("dashboard_aluno"))

    if trabalho.status != "pendente":
        flash("Este trabalho já foi enviado.", "erro")
        return redirect(url_for("dashboard_aluno"))

    # ── Validação de prazo (data E hora) ──────────────────────
    if prazo_expirado(trabalho):
        prazo_fmt = trabalho.prazo_envio.strftime('%d/%m/%Y às %H:%M')
        flash(f"O prazo de entrega já passou! O prazo era {prazo_fmt}.", "erro")
        return redirect(url_for("dashboard_aluno"))

    arquivo = request.files.get("arquivo")

    if not arquivo or arquivo.filename == "":
        flash("Selecione um arquivo.", "erro")
        return redirect(url_for("dashboard_aluno"))

    if not extensao_permitida(arquivo.filename):
        flash("Formato inválido. Envie apenas PDF ou DOCX.", "erro")
        return redirect(url_for("dashboard_aluno"))

    conteudo = arquivo.read()
    if len(conteudo) > TAMANHO_MAXIMO:
        flash("Arquivo muito grande. O limite é 15 MB.", "erro")
        return redirect(url_for("dashboard_aluno"))

    extensao   = arquivo.filename.rsplit(".", 1)[1].lower()
    nome_unico = f"{uuid.uuid4()}.{extensao}"
    caminho    = f"{session['usuario_id']}/{nome_unico}"

    try:
        supabase.storage.from_(BUCKET).upload(
            path=caminho,
            file=conteudo,
            file_options={"content-type": arquivo.content_type}
        )
        arquivo_url = supabase.storage.from_(BUCKET).get_public_url(caminho)
    except Exception as e:
        flash("Erro ao enviar o arquivo. Tente novamente.", "erro")
        app.logger.error(f"Erro upload: {e}")
        return redirect(url_for("dashboard_aluno"))

    trabalho.arquivo_url = arquivo_url
    trabalho.status      = "em_avaliacao"
    db.session.commit()

    flash("Arquivo enviado com sucesso! Aguardando avaliação.", "sucesso")
    return redirect(url_for("dashboard_aluno"))