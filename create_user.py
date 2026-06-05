from database import app, db
from models import Usuario
from werkzeug.security import generate_password_hash

with app.app_context():

    user = Usuario(
        nome="Teste",
        email="teste@gmail.com",
        senha=generate_password_hash("123"),
        tipo_usuario="aluno"
    )

    db.session.add(user)
    db.session.commit()

    print("Usuário criado com sucesso")