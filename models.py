from database import db
import uuid
from datetime import datetime


class Usuario(db.Model):
    __tablename__ = "usuarios"

    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))

    nome = db.Column(db.String(255), nullable=False)
    email = db.Column(db.String(255), nullable=False, unique=True)
    senha = db.Column(db.Text, nullable=False)

    tipo_usuario = db.Column(db.String(50), nullable=False)
    matricula = db.Column(db.String(50))

    ativo = db.Column(db.Boolean, default=True)
    criado_em = db.Column(db.DateTime, default=datetime.utcnow)


class Trabalho(db.Model):
    __tablename__ = "trabalhos"

    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))

    titulo = db.Column(db.String(255), nullable=False)
    resumo = db.Column(db.Text, nullable=False)
    palavras_chave = db.Column(db.Text)

    arquivo_url = db.Column(db.Text)

    status = db.Column(db.String(50), default="pendente")

    aluno_id = db.Column(db.String(36))
    avaliador_id = db.Column(db.String(36))

    criado_em = db.Column(db.DateTime, default=datetime.utcnow)
    prazo_envio = db.Column(db.DateTime)

    media_final = db.Column(
        db.Float,
        default=0
    )

class HistoricoMovimentacao(db.Model):
    __tablename__ = "historico_movimentacoes"

    id = db.Column(
        db.String(36),
        primary_key=True,
        default=lambda: str(uuid.uuid4())
    )

    trabalho_id = db.Column(db.String(36), nullable=False)

    descricao = db.Column(db.Text, nullable=False)

    criado_em = db.Column(
        db.DateTime,
        default=datetime.utcnow
    )