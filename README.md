# Plataforma de Submissão e Avaliação de Trabalhos Acadêmicos

Um sistema web desenvolvido em Python com Flask para automatizar o processo de envio e avaliação de trabalhos acadêmicos. O projeto nasceu de uma necessidade real: substituir o caos de e-mails, planilhas e arquivos perdidos por uma plataforma centralizada, segura e fácil de usar.

---

## Sobre o projeto

A ideia é simples: o professor cria um trabalho e atribui a um aluno. O aluno envia o arquivo pela plataforma. O professor avalia com critérios claros e o resultado aparece direto no dashboard do aluno — sem e-mail, sem confusão, sem perda de arquivo.

O sistema foi pensado para funcionar com avaliação cega (o nome do aluno fica oculto para o avaliador), garantindo imparcialidade no processo.

---

## Quem usa o sistema

**Aluno** — acessa o dashboard, vê os trabalhos atribuídos pelo professor, envia o arquivo e acompanha o status. Quando avaliado, pode ver a nota, os critérios e baixar o certificado de participação.

**Avaliador** — cria trabalhos e os atribui para alunos específicos. Quando o aluno envia o arquivo, o trabalho aparece para avaliação. A nota é calculada automaticamente pela média de 4 critérios: Relevância, Metodologia, Clareza e Originalidade. Pode exportar relatórios em PDF ou Excel e baixar o certificado de revisor.

**Administrador** — visão completa do sistema. Cadastra novos usuários (alunos e avaliadores), acompanha todos os trabalhos e tem acesso às estatísticas gerais.

---

## Tecnologias utilizadas

- **Python 3** com **Flask** — backend e rotas
- **SQLAlchemy** — ORM para comunicação com o banco
- **Supabase (PostgreSQL)** — banco de dados em nuvem
- **Supabase Storage** — armazenamento dos arquivos enviados
- **Werkzeug** — criptografia de senhas
- **ReportLab** — geração de certificados e relatórios em PDF
- **HTML + CSS puro** — frontend sem frameworks externos

---

## Como rodar o projeto localmente

**1. Clone o repositório**
```bash
git clone https://github.com/seu-usuario/seu-repositorio.git
cd seu-repositorio
```

**2. Crie e ative o ambiente virtual**
```bash
python -m venv venv
venv\Scripts\activate  # Windows
source venv/bin/activate  # Mac/Linux
```

**3. Instale as dependências**
```bash
pip install -r requirements.txt
```

**4. Configure as variáveis de ambiente**

Crie um arquivo `.env` na raiz do projeto com o seguinte conteúdo:
```
SECRET_KEY=9f3c4e6a1b2d8f7e5c0a9d1e3b4c6f8a2d1c3e5f7a9b0c2d4e6f8a1b3c5d7e9
DATABASE_URL=postgresql://postgres.zppeatcebobyddjpbmsv:projetopython@aws-1-us-west-2.pooler.supabase.com:5432/postgres
SUPABASE_URL=https://zppeatcebobyddjpbmsv.supabase.co
SUPABASE_KEY=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InpwcGVhdGNlYm9ieWRkanBibXN2Iiwicm9sZSI6ImFub24iLCJpYXQiOjE3ODAwMTA3MjIsImV4cCI6MjA5NTU4NjcyMn0.PsugX-IJpHAvuYfpiDRiGqeypuTR0FOZjEB5o7k6lVw
```

**5. Rode o projeto**
```bash
python main.py
```

Acesse em `http://127.0.0.1:5000`

Usuário Estudante: teste@gmail.com        Senha: 123
Usuário Avaliador: teste2@gmail.com        Senha: 123456
Usuário Aministrador: admin@gmail.com        Senha: 123

---

## Estrutura de pastas

```
├── main.py               # Ponto de entrada da aplicação
├── database.py           # Configuração do banco de dados
├── models.py             # Modelos das tabelas (Usuario, Trabalho, Avaliacao)
├── routes/
│   ├── auth.py           # Decorator de proteção de rotas
│   ├── login.py          # Login e logout
│   ├── home.py           # Página inicial
│   ├── dashboard_aluno.py
│   ├── dashboard_avaliador.py
│   ├── dashboard_admin.py
│   ├── trabalho.py       # Submissão e upload de arquivos
│   ├── criar_trabalho.py # Avaliador cria trabalhos
│   ├── avaliacao.py      # Formulário de avaliação
│   ├── admin.py          # Criação de usuários
│   ├── certificado.py    # Geração de certificados PDF
│   └── exportar.py       # Exportação de relatórios
├── templates/            # HTMLs com Jinja2
├── static/
│   └── style.css         # Estilos da aplicação
├── .env                  # Variáveis de ambiente (não sobe pro Git)
├── .gitignore
└── requirements.txt
```

---

## Fluxo principal

```
Admin cadastra usuários
        ↓
Avaliador cria trabalho e atribui ao aluno
        ↓
Aluno envia o arquivo pela plataforma
        ↓
Avaliador avalia com 4 critérios (nota = média automática)
        ↓
Aluno vê resultado e baixa certificado
        ↓
Avaliador exporta relatório final
```

---

## Equipe

Projeto desenvolvido para a disciplina de **Programação de Computadores** — Turma 2226213

| Nome | Papel |
|---|---|
| Iago Roberto Ferreira | Tech Leader / QA |
| Rafael Lucena Costa de Oliveira | Dev |
| Thiago Braga Dantas de Oliveira | Dev |
| João Victor Oliveira Evangelista | Dev |
| Pedro Dantas | Dev |

**Professora:** Joanacelle C. Melo  
**Instituição:** UNIPÊ — Centro Universitário de João Pessoa  
**Março, 2026**
