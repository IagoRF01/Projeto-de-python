from flask import request, session
from werkzeug.security import generate_password_hash, check_password_hash

from database import app, db
from models import Usuario

# =========================
# CADASTRO
# =========================
@app.route('/cadastro', methods=['POST'])
def cadastro():

    nome = request.form.get('nome')
    email = request.form.get('email')
    senha = request.form.get('senha')
    tipo_usuario = request.form.get('tipo_usuario')

    if not nome or not email or not senha or not tipo_usuario:
        return "Preencha todos os campos!"

    usuario_existente = Usuario.query.filter_by(email=email).first()
    if usuario_existente:
        return "E-mail já cadastrado!"

    senha_hash = generate_password_hash(senha)

    novo_usuario = Usuario(
        nome=nome,
        email=email,
        senha=senha_hash,
        tipo_usuario=tipo_usuario
    )

    db.session.add(novo_usuario)
    db.session.commit()

    return "Usuário cadastrado com sucesso!"


# =========================
# LOGIN
# =========================
@app.route('/login', methods=['POST'])
def login():

    email = request.form.get('email')
    senha = request.form.get('senha')

    usuario = Usuario.query.filter_by(email=email).first()

    if not usuario:
        return "Usuário não encontrado!"

    if not check_password_hash(usuario.senha, senha):
        return "Senha inválida!"

    session['usuario_id'] = usuario.id
    session['tipo'] = usuario.tipo_usuario

    return f"Login realizado como {usuario.tipo_usuario}"


# =========================
# LOGOUT
# =========================
@app.route('/logout')
def logout():
    session.clear()
    return "Logout realizado!"


# =========================
# ÁREA PROTEGIDA
# =========================
@app.route('/painel')
def painel():

    if 'usuario_id' not in session:
        return "Acesso negado!"

    if session['tipo'] == 'admin':
        return "Painel do Administrador"
    elif session['tipo'] == 'aluno':
        return "Painel do Aluno"
    elif session['tipo'] == 'avaliador':
        return "Painel do Avaliador"
    else:
        return "Tipo desconhecido"


# =========================
# RODAR APP
# =========================
if __name__ == '__main__':
    app.run(debug=True)