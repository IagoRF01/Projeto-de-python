from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

class Usuario(db.Model):

    id = db.Column(db.Integer, primary_key=True)

    nome = db.Column(db.String(100), nullable=False)

    email = db.Column(db.String(120), nullable=False, unique=True)

    senha = db.Column(db.String(255), nullable=False)

    tipo_usuario = db.Column(db.String(50), nullable=False)

with app.app_context():
    db.create_all()

@app.route('/cadastro', methods=['GET', 'POST'])

def cadastro():

    if request.method == 'POST':

        nome = request.form.get('nome')

        email = request.form.get('email')

        senha = request.form.get('senha')

        tipo_usuario = request.form.get('tipo_usuario')

        if not nome or not email or not senha or not tipo_usuario:
            return 'Preencha todos os campos!'

        senha_criptografada = generate_password_hash(senha)

        novo_usuario = Usuario(
            nome=nome,
            email=email,
            senha=senha_criptografada,
            tipo_usuario=tipo_usuario
        )

        db.session.add(novo_usuario)
        db.session.commit()

        return redirect('/cadastro')

    return render_template('cadastro.html')

if __name__ == '__main__':
    app.run(debug=True)
