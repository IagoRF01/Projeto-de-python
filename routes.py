from flask import render_template, redirect, request
from database import app, db
from models import Trabalho, HistoricoMovimentacao
import uuid


@app.route("/")
def dashboard():
    trabalhos = Trabalho.query.all()
    return render_template("dashboard.html", trabalhos=trabalhos)


@app.route("/trabalho/<id>")
def visualizar_trabalho(id):
    trabalho = Trabalho.query.get(id)
    return render_template("trabalho.html", trabalho=trabalho)


@app.route("/criar_trabalho", methods=["GET", "POST"])
def criar_trabalho():
    if request.method == "POST":

        titulo = request.form["titulo"]
        resumo = request.form["resumo"]

        novo = Trabalho(
            id=str(uuid.uuid4()),
            titulo=titulo,
            resumo=resumo,
            status="Enviado",
            aluno_id="11111111-1111-1111-1111-111111111111"
        )

        db.session.add(novo)
        historico = HistoricoMovimentacao(
        trabalho_id=novo.id,
        descricao="Trabalho criado"
        )

        db.session.add(historico)

        db.session.commit()

        return redirect("/")

    return render_template("criar_trabalho.html")

@app.route("/avaliador")
def dashboard_avaliador():

    status = request.args.get("status")

    if status:
        trabalhos = Trabalho.query.filter_by(status=status).all()
    else:
        trabalhos = Trabalho.query.all()

    return render_template(
        "dashboard_avaliador.html",
        trabalhos=trabalhos
    )

@app.route("/avaliar/<id>")
def avaliar_trabalho(id):
    trabalho = Trabalho.query.get(id)

    return render_template(
        "avaliar_trabalho.html",
        trabalho=trabalho
    )

@app.route("/aprovar/<id>", methods=["POST"])
def aprovar_trabalho(id):

    trabalho = Trabalho.query.get(id)

    trabalho.status = "Aprovado"

    historico = HistoricoMovimentacao(
    trabalho_id=id,
    descricao="Trabalho aprovado"
)

    db.session.add(historico)

    db.session.commit()

    return redirect("/avaliador")


@app.route("/rejeitar/<id>", methods=["POST"])
def rejeitar_trabalho(id):

    trabalho = Trabalho.query.get(id)

    trabalho.status = "Rejeitado"
    historico = HistoricoMovimentacao(
    trabalho_id=id,
    descricao="Trabalho rejeitado"
)

    db.session.add(historico)
    db.session.commit()

    return redirect("/avaliador")