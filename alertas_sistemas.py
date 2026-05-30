from flask import request, session
from werkzeug.security import generate_password_hash, check_password_hash

from database import app, db
from models import Usuario

# =========================
# MENSAGENS PADRÃO
# =========================
def mensagem(tipo, texto):
    return f"[{tipo.upper()}] {texto}"


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
        return mensagem("erro", "Preencha todos os campos!")

    if Usuario.query.filter_by(email=email).first():
        return mensagem("erro", "E-mail já cadastrado!")

    senha_hash = generate_password_hash(senha)

    novo = Usuario(
        nome=nome,
        email=email,
        senha=senha_hash,
        tipo_usuario=tipo_usuario
    )

    db.session.add(novo)
    db.session.commit()

    return mensagem("sucesso", "Usuário cadastrado com sucesso!")


# =========================
# LOGIN
# =========================
@app.route('/login', methods=['POST'])
def login():

    email = request.form.get('email')
    senha = request.form.get('senha')

    usuario = Usuario.query.filter_by(email=email).first()

    if not usuario:
        return mensagem("erro", "Usuário não encontrado!")

    if not check_password_hash(usuario.senha, senha):
        return mensagem("erro", "Senha inválida!")

    session['usuario_id'] = usuario.id
    session['tipo'] = usuario.tipo_usuario

    return mensagem("sucesso", f"Login realizado como {usuario.tipo_usuario}")


# =========================
# LOGOUT
# =========================
@app.route('/logout')
def logout():
    session.clear()
    return mensagem("info", "Logout realizado com sucesso!")


# =========================
# PAINEL
# =========================
@app.route('/painel')
def painel():

    if 'usuario_id' not in session:
        return mensagem("erro", "Acesso negado!")

    return mensagem("info", "Painel carregado com sucesso!")


# =========================
# DASHBOARD ADMIN
# =========================
@app.route('/dashboard/admin')
def dashboard_admin():

    if 'usuario_id' not in session:
        return mensagem("erro", "Acesso negado!")

    if session['tipo'] != 'admin':
        return mensagem("erro", "Apenas administradores")

    total = Usuario.query.count()
    alunos = Usuario.query.filter_by(tipo_usuario='aluno').count()
    avaliadores = Usuario.query.filter_by(tipo_usuario='avaliador').count()

    return f"""
    DASHBOARD ADMIN

    Usuários: {total}
    Alunos: {alunos}
    Avaliadores: {avaliadores}

    Trabalhos: (não implementado ainda)
    Avaliações: (não implementado ainda)
    """


# =========================
# AVALIAÇÃO (BASE)
# =========================
@app.route('/avaliacao', methods=['POST'])
def avaliacao():

    if 'usuario_id' not in session:
        return mensagem("erro", "Acesso negado!")

    if session['tipo'] != 'avaliador':
        return mensagem("erro", "Apenas avaliadores")

    originalidade = request.form.get('originalidade')
    clareza = request.form.get('clareza')
    metodologia = request.form.get('metodologia')
    relevancia = request.form.get('relevancia')
    organizacao = request.form.get('organizacao')
    comentario = request.form.get('comentario')

    if not all([originalidade, clareza, metodologia, relevancia, organizacao]):
        return mensagem("erro", "Preencha todas as notas!")

    return mensagem("sucesso", "Avaliação registrada com sucesso!")


# =========================
# RODAR APP
# =========================
if __name__ == '__main__':
    app.run(debug=True)