from io import BytesIO

from flask import (
    send_file,
    session
)

from reportlab.platypus import (
    SimpleDocTemplate,
    Paragraph,
    Spacer
)

from reportlab.lib.styles import (
    getSampleStyleSheet
)

from database import app

from models import (
    Trabalho,
    Usuario,
    Avaliacao
)


@app.route(
    '/relatorio-pdf/<trabalho_id>'
)
def relatorio_pdf(
    trabalho_id
):

    if 'usuario_id' not in session:
        return "Acesso negado!"

    trabalho = (
        Trabalho.query
        .get_or_404(trabalho_id)
    )

    aluno = (
        Usuario.query
        .get(trabalho.aluno_id)
    )

    avaliacoes = (
        Avaliacao.query
        .filter_by(
            trabalho_id=trabalho.id
        )
        .all()
    )

    buffer = BytesIO()

    pdf = SimpleDocTemplate(
        buffer
    )

    estilos = (
        getSampleStyleSheet()
    )

    elementos = []

    elementos.append(
        Paragraph(
            "Relatório Final do Trabalho",
            estilos['Title']
        )
    )

    elementos.append(
        Spacer(1, 20)
    )

    # ======================
    # DADOS DO ALUNO
    # ======================

    elementos.append(
        Paragraph(
            f"<b>Aluno:</b> {aluno.nome}",
            estilos['Normal']
        )
    )

    elementos.append(
        Paragraph(
            f"<b>Email:</b> {aluno.email}",
            estilos['Normal']
        )
    )

    elementos.append(
        Paragraph(
            f"<b>Matrícula:</b> {aluno.matricula}",
            estilos['Normal']
        )
    )

    elementos.append(
        Spacer(1, 15)
    )

    # ======================
    # TRABALHO
    # ======================

    elementos.append(
        Paragraph(
            f"<b>Título:</b> {trabalho.titulo}",
            estilos['Normal']
        )
    )

    elementos.append(
        Paragraph(
            f"<b>Resumo:</b> {trabalho.resumo}",
            estilos['Normal']
        )
    )

    elementos.append(
        Paragraph(
            f"<b>Status:</b> {trabalho.status}",
            estilos['Normal']
        )
    )

    elementos.append(
        Paragraph(
            f"<b>Média Final:</b> {trabalho.media_final}",
            estilos['Normal']
        )
    )

    elementos.append(
        Spacer(1, 15)
    )

    # ======================
    # AVALIAÇÕES
    # ======================

    for avaliacao in avaliacoes:

        elementos.append(
            Paragraph(
                "<b>Avaliação</b>",
                estilos['Heading2']
            )
        )

        elementos.append(
            Paragraph(
                f"Originalidade: {avaliacao.originalidade}",
                estilos['Normal']
            )
        )

        elementos.append(
            Paragraph(
                f"Clareza: {avaliacao.clareza}",
                estilos['Normal']
            )
        )

        elementos.append(
            Paragraph(
                f"Metodologia: {avaliacao.metodologia}",
                estilos['Normal']
            )
        )

        elementos.append(
            Paragraph(
                f"Relevância: {avaliacao.relevancia}",
                estilos['Normal']
            )
        )

        elementos.append(
            Paragraph(
                f"Organização: {avaliacao.organizacao}",
                estilos['Normal']
            )
        )

        elementos.append(
            Paragraph(
                f"Comentário: {avaliacao.comentario}",
                estilos['Normal']
            )
        )

        elementos.append(
            Spacer(1, 10)
        )

    pdf.build(
        elementos
    )

    buffer.seek(0)

    return send_file(
        buffer,
        as_attachment=True,
        download_name=
        f"relatorio_{trabalho.id}.pdf",
        mimetype=
        "application/pdf"
    )