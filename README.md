# 📚 Plataforma de Submissão Acadêmica

Sistema web desenvolvido em Flask para gerenciamento de submissão, avaliação e acompanhamento de trabalhos acadêmicos.

---

## 🚀 Funcionalidades

### 👨‍🎓 Aluno
- Cadastro e login de usuário
- Submissão de trabalhos acadêmicos
- Visualização de status (pendente, em avaliação, aprovado, rejeitado)
- Dashboard com resumo dos trabalhos

### 🧑‍🏫 Avaliador
- Visualização de trabalhos submetidos
- Avaliação de trabalhos
- Atualização de status dos trabalhos

### 🛠️ Administrador
- Gerenciamento de usuários
- Visão geral do sistema

---

## 🧱 Tecnologias utilizadas

- Python 3
- Flask
- Flask-SQLAlchemy
- PostgreSQL (Supabase)
- HTML5
- CSS3
- Jinja2
- Git & GitHub

---

## 🗂️ Estrutura do projeto
Projeto-de-python/
│
├── database.py
├── main.py
├── models.py
├── routes/
│ ├── init.py
│ ├── dashboard_aluno.py
│ ├── login.py
│ └── ...
│
├── templates/
│ ├── base.html
│ ├── login.html
│ ├── dashboard_aluno.html
│ └── ...
│
├── static/
│ └── style.css
│
├── instance/
├── venv/
└── README.md

---

## ⚙️ Como rodar o projeto

### 1. Clonar o repositório
```bash
git clone https://github.com/IagoRF01/Projeto-de-python.git
cd Projeto-de-python
2. Criar ambiente virtual
python -m venv venv
3. Ativar ambiente virtual
venv\Scripts\activate
4. Instalar dependências
pip install -r requirements.txt
5. Rodar o projeto
python main.py
🔐 Variáveis de ambiente

Crie um arquivo .env:

DATABASE_URL=sua_url_do_supabase
SECRET_KEY=sua_chave_secreta
🧠 Aprendizados
Estruturação de projeto Flask
Autenticação com sessões
Integração com banco de dados (Supabase/PostgreSQL)
Organização de rotas e templates
CRUD de entidades (usuários e trabalhos)
📌 Status do projeto

✔ Em desenvolvimento
✔ Funcional base implementada
⏳ Melhorias futuras:

Upload de arquivos reais
Sistema de avaliação completo
Painel admin avançado
Deploy em produção
