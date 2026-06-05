from flask import render_template, session
from database import app

@app.route("/dashboard-avaliador")
def dashboard_avaliador():
    if "usuario_id" not in session:
        return "Acesso negado"
    return render_template("dashboard_avaliador.html")