from database import db

class Usuario(db.Model):
    __tablename__ = "usuarios"

    id = db.Column(db.String(36), primary_key=True)

    nome = db.Column(db.String(255), nullable=False)

    email = db.Column(db.String(255), nullable=False, unique=True)

    senha = db.Column(db.Text, nullable=False)

    tipo_usuario = db.Column(db.String(50), nullable=False)

    matricula = db.Column(db.String(50))

    ativo = db.Column(db.Boolean, default=True)

    criado_em = db.Column(db.DateTime)

class Trabalho(db.Model):
    __tablename__ = "trabalhos"

    id = db.Column(db.String(36), primary_key=True)
    titulo = db.Column(db.String(255))
    resumo = db.Column(db.Text)
    palavras_chave = db.Column(db.Text)
    arquivo_url = db.Column(db.Text)
    status = db.Column(db.String(50))
    aluno_id = db.Column(db.String(36))
    avaliador_id = db.Column(db.String(36))
    criado_em = db.Column(db.DateTime)
    prazo_envio = db.Column(db.DateTime)