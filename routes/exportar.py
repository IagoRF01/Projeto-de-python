from flask import send_file, session, redirect, url_for, flash
from database import app
from models import Trabalho, Usuario, Avaliacao
from routes.auth import login_required
from reportlab.lib.pagesizes import A4, landscape
from reportlab.lib import colors
from reportlab.lib.units import cm
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_CENTER
import io
import csv
from datetime import datetime


# ── Exportar PDF ───────────────────────────────────────────────
@app.route("/exportar/pdf")
@login_required(perfil="avaliador")
def exportar_pdf():
    avaliador   = Usuario.query.get(session["usuario_id"])
    trabalhos   = Trabalho.query.filter_by(avaliador_id=session["usuario_id"]).all()

    buffer = io.BytesIO()
    doc    = SimpleDocTemplate(buffer, pagesize=landscape(A4),
                               leftMargin=2*cm, rightMargin=2*cm,
                               topMargin=2*cm, bottomMargin=2*cm)

    styles  = getSampleStyleSheet()
    titulo  = ParagraphStyle("t", parent=styles["Normal"], fontSize=16,
                             fontName="Helvetica-Bold", alignment=TA_CENTER,
                             textColor=colors.HexColor("#1a1a2e"), spaceAfter=4)
    sub     = ParagraphStyle("s", parent=styles["Normal"], fontSize=10,
                             fontName="Helvetica", alignment=TA_CENTER,
                             textColor=colors.HexColor("#6b7280"), spaceAfter=16)

    el = []
    el.append(Paragraph("Relatório de Trabalhos Acadêmicos", titulo))
    el.append(Paragraph(
        f"Gerado em: {datetime.now().strftime('%d/%m/%Y')}  ·  "
        f"Professor: {avaliador.nome if avaliador else '—'}", sub))

    # Cabeçalho da tabela
    dados = [["Título do Trabalho", "Aluno", "Data Submissão", "Nota Final", "Status"]]

    for t in trabalhos:
        aluno     = Usuario.query.get(t.aluno_id)
        avaliacao = Avaliacao.query.filter_by(trabalho_id=t.id).first()
        dados.append([
            t.titulo,
            aluno.nome if aluno else "—",
            t.criado_em.strftime("%d/%m/%Y") if t.criado_em else "—",
            f"{float(avaliacao.nota):.1f}" if avaliacao and avaliacao.nota else "—",
            t.status.replace("_", " ").title(),
        ])

    tabela = Table(dados, colWidths=[8*cm, 5*cm, 3.5*cm, 3*cm, 3.5*cm])
    tabela.setStyle(TableStyle([
        ("BACKGROUND",  (0, 0), (-1, 0),  colors.HexColor("#3b5bdb")),
        ("TEXTCOLOR",   (0, 0), (-1, 0),  colors.white),
        ("FONTNAME",    (0, 0), (-1, 0),  "Helvetica-Bold"),
        ("FONTSIZE",    (0, 0), (-1, 0),  10),
        ("ALIGN",       (0, 0), (-1, -1), "LEFT"),
        ("VALIGN",      (0, 0), (-1, -1), "MIDDLE"),
        ("ROWBACKGROUNDS", (0, 1), (-1, -1), [colors.white, colors.HexColor("#f9fafb")]),
        ("FONTNAME",    (0, 1), (-1, -1), "Helvetica"),
        ("FONTSIZE",    (0, 1), (-1, -1), 9),
        ("GRID",        (0, 0), (-1, -1), 0.5, colors.HexColor("#e5e7eb")),
        ("TOPPADDING",  (0, 0), (-1, -1), 8),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 8),
        ("LEFTPADDING", (0, 0), (-1, -1), 8),
    ]))

    el.append(tabela)
    doc.build(el)
    buffer.seek(0)

    return send_file(buffer, mimetype="application/pdf", as_attachment=True,
                     download_name=f"relatorio_{datetime.now().strftime('%Y-%m-%d')}.pdf")


# ── Exportar Excel (CSV) ───────────────────────────────────────
@app.route("/exportar/excel")
@login_required(perfil="avaliador")
def exportar_excel():
    avaliador = Usuario.query.get(session["usuario_id"])
    trabalhos = Trabalho.query.filter_by(avaliador_id=session["usuario_id"]).all()

    buffer = io.StringIO()
    writer = csv.writer(buffer)

    # Cabeçalho
    writer.writerow([
        "Título", "Aluno", "Data Submissão",
        "Relevância", "Metodologia", "Clareza", "Originalidade",
        "Nota Final", "Status"
    ])

    for t in trabalhos:
        aluno     = Usuario.query.get(t.aluno_id)
        avaliacao = Avaliacao.query.filter_by(trabalho_id=t.id).first()
        writer.writerow([
            t.titulo,
            aluno.nome if aluno else "—",
            t.criado_em.strftime("%d/%m/%Y") if t.criado_em else "—",
            float(avaliacao.relevancia)    if avaliacao and avaliacao.relevancia    else "—",
            float(avaliacao.metodologia)   if avaliacao and avaliacao.metodologia   else "—",
            float(avaliacao.clareza)       if avaliacao and avaliacao.clareza       else "—",
            float(avaliacao.originalidade) if avaliacao and avaliacao.originalidade else "—",
            float(avaliacao.nota)          if avaliacao and avaliacao.nota          else "—",
            t.status.replace("_", " ").title(),
        ])

    buffer.seek(0)
    bytes_buffer = io.BytesIO(buffer.getvalue().encode("utf-8-sig"))

    return send_file(bytes_buffer, mimetype="text/csv", as_attachment=True,
                     download_name=f"relatorio_{datetime.now().strftime('%Y-%m-%d')}.csv")