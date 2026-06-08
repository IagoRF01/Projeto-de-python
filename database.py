from dotenv import load_dotenv
load_dotenv()
import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

# ── Segurança ──────────────────────────────────────────────────
# Em produção, mova para variável de ambiente:
# export SECRET_KEY="algo-muito-secreto"
app.secret_key = os.environ.get("SECRET_KEY", "dev-secret-troque-em-producao")

# ── Supabase (PostgreSQL) ──────────────────────────────────────
# Em produção, use variável de ambiente:
# export DATABASE_URL="postgresql://..."
SUPABASE_URI = os.environ.get(
    "DATABASE_URL",
    "postgresql://postgres.zppeatcebobyddjpbmsv:projetopython@aws-1-us-west-2.pooler.supabase.com:5432/postgres"
)

app.config["SQLALCHEMY_DATABASE_URI"] = SUPABASE_URI
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

# Pool resiliente para conexões remotas (Supabase fecha conexões ociosas)
app.config["SQLALCHEMY_ENGINE_OPTIONS"] = {
    "pool_pre_ping": True,       # testa a conexão antes de usar
    "pool_recycle": 300,         # recicla conexões a cada 5 min
    "connect_args": {
        "connect_timeout": 10,   # timeout de 10s na conexão
        "sslmode": "require",    # Supabase exige SSL
    }
}

db = SQLAlchemy(app)