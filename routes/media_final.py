from database import db

from models import (
    Trabalho,
    Avaliacao
)


def calcular_media_final(
    trabalho_id
):

    avaliacoes = (
        Avaliacao.query
        .filter_by(
            trabalho_id=trabalho_id
        )
        .all()
    )

    if not avaliacoes:
        return 0

    medias_avaliadores = []

    for avaliacao in avaliacoes:

        media_avaliador = (

            avaliacao.originalidade +

            avaliacao.clareza +

            avaliacao.metodologia +

            avaliacao.relevancia +

            avaliacao.organizacao

        ) / 5

        medias_avaliadores.append(
            media_avaliador
        )

    media_geral = (
        sum(medias_avaliadores)
        /
        len(medias_avaliadores)
    )

    media_geral = round(
        media_geral,
        2
    )

    trabalho = (
        Trabalho.query
        .get(trabalho_id)
    )

    trabalho.media_final = (
        media_geral
    )

    db.session.commit()

    return media_geral