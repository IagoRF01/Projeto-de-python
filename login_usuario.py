from flask import Flask, request, redirect, session
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)

# chave da sessão (obrigatório para login)
app.secret_key = "chave_super_secreta"

# banco de dados
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)


# =========================
# MODELO USUÁRIO
# =========================
class Usuario(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), nullable=False, unique=True)
    senha = db.Column(db.String(255), nullable=False)
    tipo_usuario = db.Column(db.String(50), nullable=False)


with app.app_context():
    db.create_all()


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