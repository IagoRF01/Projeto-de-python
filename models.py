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