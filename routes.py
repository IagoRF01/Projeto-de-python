from database import app
from flask import render_template
from models import Trabalho

@app.route("/trabalho/<id>")
def visualizar_trabalho(id):
    trabalho = Trabalho.query.get(id)
    return render_template("trabalho.html", trabalho=trabalho)