from functools import wraps
from flask import session, redirect, url_for

def login_required(perfil=None):
    """
    Decorator que protege rotas autenticadas.

    Uso sem restrição de perfil (qualquer usuário logado):
        @login_required()
        def minha_rota(): ...

    Uso com perfil específico:
        @login_required(perfil="aluno")
        def dashboard_aluno(): ...

        @login_required(perfil="avaliador")
        def dashboard_avaliador(): ...
    """
    def decorator(f):
        @wraps(f)
        def decorated(*args, **kwargs):
            # Não está logado
            if "usuario_id" not in session:
                return redirect(url_for("home"))

            # Está logado mas tentando acessar perfil errado
            if perfil and session.get("tipo") != perfil:
                # Redireciona para o dashboard correto do usuário
                tipo = session.get("tipo")
                if tipo == "aluno":
                    return redirect(url_for("dashboard_aluno"))
                if tipo == "avaliador":
                    return redirect(url_for("dashboard_avaliador"))
                if tipo == "admin":
                    return redirect(url_for("dashboard_admin"))
                return redirect(url_for("home"))

            return f(*args, **kwargs)
        return decorated
    return decorator