from dotenv import load_dotenv
load_dotenv()
import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

# ── Segurança ──────────────────────────────────────────────────
# Em produção, mova para variável de ambiente:
# export SECRET_KEY="algo-muito-secreto"
app.secret_key = os.environ.get("SECRET_KEY", "9f3c4e6a1b2d8f7e5c0a9d1e3b4c6f8a2d1c3e5f7a9b0c2d4e6f8a1b3c5d7e9")

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