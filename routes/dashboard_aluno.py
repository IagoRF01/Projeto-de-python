from flask import render_template
from flask import session

from database import app
from models import Trabalho


@app.route('/dashboard-aluno')
def dashboard_aluno():

    if 'usuario_id' not in session:
        return render_template(
            'login.html'
        )

    trabalhos = Trabalho.query.filter_by(
        estudante_id=session['usuario_id']
    ).all()

    return render_template(
        'dashboard_aluno.html',
        trabalhos=trabalhos
    )