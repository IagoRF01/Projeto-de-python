from flask import send_file, session, redirect, url_for, flash
from database import app
from models import Trabalho, Usuario, Avaliacao
from routes.auth import login_required
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.lib.units import cm
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, HRFlowable
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_CENTER, TA_LEFT
import io
from datetime import datetime


def _estilos():
    styles = getSampleStyleSheet()
    titulo = ParagraphStyle("titulo", parent=styles["Normal"],
        fontSize=20, fontName="Helvetica-Bold",
        textColor=colors.HexColor("#1a1a2e"), alignment=TA_CENTER, spaceAfter=6)
    subtitulo = ParagraphStyle("subtitulo", parent=styles["Normal"],
        fontSize=12, fontName="Helvetica",
        textColor=colors.HexColor("#6b7280"), alignment=TA_CENTER, spaceAfter=4)
    label = ParagraphStyle("label", parent=styles["Normal"],
        fontSize=9, fontName="Helvetica",
        textColor=colors.HexColor("#6b7280"), alignment=TA_LEFT, spaceAfter=2)
    valor = ParagraphStyle("valor", parent=styles["Normal"],
        fontSize=11, fontName="Helvetica-Bold",
        textColor=colors.HexColor("#1a1a2e"), alignment=TA_LEFT, spaceAfter=12)
    rodape = ParagraphStyle("rodape", parent=styles["Normal"],
        fontSize=8, fontName="Helvetica",
        textColor=colors.HexColor("#9ca3af"), alignment=TA_CENTER)
    return titulo, subtitulo, label, valor, rodape


# ── Certificado do Aluno ───────────────────────────────────────
@app.route("/certificado/aluno/<trabalho_id>")
@login_required(perfil="aluno")
def certificado_aluno(trabalho_id):
    trabalho  = Trabalho.query.get(trabalho_id)
    avaliacao = Avaliacao.query.filter_by(trabalho_id=trabalho_id).first()

    if not trabalho or trabalho.aluno_id != session["usuario_id"]:
        flash("Trabalho não encontrado.", "erro")
        return redirect(url_for("dashboard_aluno"))

    if not avaliacao:
        flash("Este trabalho ainda não foi avaliado.", "erro")
        return redirect(url_for("dashboard_aluno"))

    aluno     = Usuario.query.get(trabalho.aluno_id)
    avaliador = Usuario.query.get(trabalho.avaliador_id)
    titulo, subtitulo, label, valor, rodape = _estilos()

    buffer = io.BytesIO()
    doc    = SimpleDocTemplate(buffer, pagesize=A4,
                               leftMargin=3*cm, rightMargin=3*cm,
                               topMargin=3*cm, bottomMargin=2*cm)
    el = []
    el.append(Spacer(1, 1*cm))
    el.append(Paragraph("CERTIFICADO DE PARTICIPAÇÃO", titulo))
    el.append(Paragraph("Plataforma de Submissão Acadêmica", subtitulo))
    el.append(Spacer(1, 0.5*cm))
    el.append(HRFlowable(width="100%", thickness=1, color=colors.HexColor("#3b5bdb")))
    el.append(Spacer(1, 0.8*cm))
    el.append(Paragraph("Certificamos que", label))
    el.append(Paragraph(aluno.nome if aluno else "—", valor))
    el.append(Paragraph("submeteu e teve avaliado o trabalho acadêmico", label))
    el.append(Paragraph(trabalho.titulo, valor))
    el.append(Paragraph("Avaliado por", label))
    el.append(Paragraph(avaliador.nome if avaliador else "—", valor))
    el.append(Paragraph("Nota Final", label))
    el.append(Paragraph(f"{float(avaliacao.nota):.1f} / 10" if avaliacao.nota else "—", valor))
    el.append(Paragraph("Data de Avaliação", label))
    el.append(Paragraph(avaliacao.criado_em.strftime("%d/%m/%Y") if avaliacao.criado_em else "—", valor))
    el.append(Spacer(1, 0.5*cm))
    el.append(HRFlowable(width="100%", thickness=1, color=colors.HexColor("#e5e7eb")))
    el.append(Spacer(1, 0.4*cm))
    el.append(Paragraph(f"Gerado em {datetime.now().strftime('%d/%m/%Y às %H:%M')} · Plataforma de Submissão Acadêmica", rodape))

    doc.build(el)
    buffer.seek(0)
    return send_file(buffer, mimetype="application/pdf", as_attachment=True,
                     download_name=f"certificado_{(aluno.nome if aluno else 'aluno').replace(' ','_')}.pdf")


# ── Certificado do Avaliador ───────────────────────────────────
@app.route("/certificado/avaliador/<trabalho_id>")
@login_required(perfil="avaliador")
def certificado_avaliador(trabalho_id):
    trabalho  = Trabalho.query.get(trabalho_id)
    avaliacao = Avaliacao.query.filter_by(
        trabalho_id=trabalho_id, avaliador_id=session["usuario_id"]).first()

    if not trabalho or trabalho.avaliador_id != session["usuario_id"]:
        flash("Trabalho não encontrado.", "erro")
        return redirect(url_for("dashboard_avaliador"))

    if not avaliacao:
        flash("Avaliação não encontrada.", "erro")
        return redirect(url_for("dashboard_avaliador"))

    avaliador = Usuario.query.get(session["usuario_id"])
    titulo, subtitulo, label, valor, rodape = _estilos()

    buffer = io.BytesIO()
    doc    = SimpleDocTemplate(buffer, pagesize=A4,
                               leftMargin=3*cm, rightMargin=3*cm,
                               topMargin=3*cm, bottomMargin=2*cm)
    el = []
    el.append(Spacer(1, 1*cm))
    el.append(Paragraph("CERTIFICADO DE PARTICIPAÇÃO COMO REVISOR", titulo))
    el.append(Paragraph("Plataforma de Submissão Acadêmica", subtitulo))
    el.append(Spacer(1, 0.5*cm))
    el.append(HRFlowable(width="100%", thickness=1, color=colors.HexColor("#16a34a")))
    el.append(Spacer(1, 0.8*cm))
    el.append(Paragraph("Certificamos que", label))
    el.append(Paragraph(avaliador.nome if avaliador else "—", valor))
    el.append(Paragraph("atuou como avaliador do trabalho acadêmico", label))
    el.append(Paragraph(trabalho.titulo, valor))
    el.append(Paragraph("Nota atribuída", label))
    el.append(Paragraph(f"{float(avaliacao.nota):.1f} / 10" if avaliacao.nota else "—", valor))

    criterios = []
    if avaliacao.relevancia    is not None: criterios.append(f"Relevância: {float(avaliacao.relevancia):.1f}")
    if avaliacao.metodologia   is not None: criterios.append(f"Metodologia: {float(avaliacao.metodologia):.1f}")
    if avaliacao.clareza       is not None: criterios.append(f"Clareza: {float(avaliacao.clareza):.1f}")
    if avaliacao.originalidade is not None: criterios.append(f"Originalidade: {float(avaliacao.originalidade):.1f}")

    el.append(Paragraph("Critérios avaliados", label))
    el.append(Paragraph("  ·  ".join(criterios) if criterios else "—", valor))
    el.append(Paragraph("Data da Avaliação", label))
    el.append(Paragraph(avaliacao.criado_em.strftime("%d/%m/%Y") if avaliacao.criado_em else "—", valor))
    el.append(Spacer(1, 0.5*cm))
    el.append(HRFlowable(width="100%", thickness=1, color=colors.HexColor("#e5e7eb")))
    el.append(Spacer(1, 0.4*cm))
    el.append(Paragraph(f"Gerado em {datetime.now().strftime('%d/%m/%Y às %H:%M')} · Plataforma de Submissão Acadêmica", rodape))

    doc.build(el)
    buffer.seek(0)
    return send_file(buffer, mimetype="application/pdf", as_attachment=True,
                     download_name=f"certificado_revisor_{(avaliador.nome if avaliador else 'avaliador').replace(' ','_')}.pdf")