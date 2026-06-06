from database import app, db
import routes  # registra todas as rotas via __init__.py

if __name__ == "__main__":
    # NÃO usamos db.create_all() — as tabelas já existem no Supabase.
    # Se precisar recriar localmente para testes, descomente a linha abaixo:
    # with app.app_context(): db.create_all()
    app.run(debug=True)