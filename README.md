# Guia de Contribuição - Passo a Passo

Este documento descreve como configurar o projeto e criar branches para desenvolvimento sem mexer na branch `main`.

## 1️⃣ Clonar o repositório

Abra o terminal e execute:

```bash
git clone https://github.com/seu-usuario/seu-repositorio.git
cd seu-repositorio
```

> Substitua `seu-usuario/seu-repositorio` pela URL real do seu repositório GitHub

## 2️⃣ Configurar identidade local (primeira vez)

Configure seu nome e email para que os commits tenham sua identidade:

```bash
git config user.name "Seu Nome Completo"
git config user.email "seu-email@example.com"
```

> Dica: Para configurar globalmente (em todos os projetos), adicione a flag `--global`:
> ```bash
> git config --global user.name "Seu Nome Completo"
> git config --global user.email "seu-email@example.com"
> ```

## 3️⃣ Verificar branch atual

Sempre verifique em qual branch você está:

```bash
git branch
```

Você deverá ver algo como:
```
* main
```

O asterisco (*) indica a branch atual.

## 4️⃣ Atualizar a branch main (importante!)

Antes de criar uma nova branch, sempre atualize a `main` com as mudanças mais recentes do repositório:

```bash
git checkout main
git pull origin main
```

## 5️⃣ Criar uma nova branch

Crie uma branch com um nome descritivo (nunca trabalhe direto na `main`):

```bash
git checkout -b nome-da-sua-branch
```

### Exemplos de bons nomes para branches:
```bash
git checkout -b feature/login-usuario
git checkout -b bugfix/corrigir-erro-conexao
git checkout -b docs/atualizar-readme
git checkout -b feature/adicionar-validacao
```

> **Convenção recomendada:**
> - `feature/` - para novas funcionalidades
> - `bugfix/` - para correções de bugs
> - `docs/` - para atualizações de documentação
> - `hotfix/` - para correções urgentes

## 6️⃣ Fazer alterações no código

Edite os arquivos do projeto conforme necessário.

## 7️⃣ Verificar arquivos modificados

Para ver quais arquivos foram alterados:

```bash
git status
```

## 8️⃣ Adicionar arquivos para commit

Adicione os arquivos ao staging area:

```bash
# Adicionar arquivo específico
git add caminho/do/arquivo.py

# OU adicionar todos os arquivos modificados
git add .
```

## 9️⃣ Fazer um commit

Crie um commit com uma mensagem descritiva:

```bash
git commit -m "Descrição clara das mudanças realizadas"
```

### Exemplos de boas mensagens de commit:
```bash
git commit -m "Feature: Adicionar função de login"
git commit -m "Bugfix: Corrigir erro de conexão ao banco de dados"
git commit -m "Docs: Atualizar README com instruções de setup"
git commit -m "Refactor: Melhorar estrutura do código principal"
```

## 🔟 Enviar a branch para o GitHub

Envie sua branch para o repositório remoto:

```bash
git push origin nome-da-sua-branch
```

## 1️⃣1️⃣ Criar um Pull Request (PR)

1. Acesse o repositório no GitHub
2. Você verá uma notificação para criar um Pull Request
3. Clique em "Compare & pull request"
4. Adicione uma descrição das mudanças
5. Clique em "Create pull request"

> Um revisor irá analisar seu código e aprovar ou pedir alterações

## 1️⃣2️⃣ Sincronizar sua branch local com a main

Se a `main` foi atualizada enquanto você trabalha em sua branch:

```bash
git fetch origin
git rebase origin/main
```

Ou use merge (alternativa mais simples):

```bash
git fetch origin
git merge origin/main
```

## 1️⃣3️⃣ Deletar uma branch local (após PR aprovado)

Depois que sua branch for aprovada e mesclada:

```bash
# Deletar branch local
git branch -d nome-da-sua-branch

# OU forçar deleção se necessário
git branch -D nome-da-sua-branch
```

## 1️⃣4️⃣ Voltar para a main quando terminar

Sempre retorne para a `main` e atualize:

```bash
git checkout main
git pull origin main
```

---

## ⚠️ REGRAS IMPORTANTES

✅ **FAÇA:**
- Sempre crie uma branch nova para cada tarefa
- Sempre atualize a `main` antes de criar uma branch
- Use nomes descritivos para branches
- Faça commits frequentes com mensagens claras
- Sempre faça push da sua branch, não da `main`

❌ **NÃO FAÇA:**
- Não trabalhe direto na branch `main`
- Não faça push direto na `main`
- Não faça grandes commits sem mensagem descritiva
- Não delete a branch `main` local

---

## 📋 Fluxo Completo (Resumido)

```bash
# 1. Clonar repositório
git clone https://github.com/seu-usuario/seu-repositorio.git
cd seu-repositorio

# 2. Atualizar main
git checkout main
git pull origin main

# 3. Criar branch
git checkout -b feature/minha-funcionalidade

# 4. Fazer alterações nos arquivos
# (editar arquivos com seu editor)

# 5. Adicionar mudanças
git add .

# 6. Fazer commit
git commit -m "Descrição das mudanças"

# 7. Enviar para GitHub
git push origin feature/minha-funcionalidade

# 8. Criar Pull Request no GitHub

# 9. Após aprovação, deletar branch
git branch -d feature/minha-funcionalidade

# 10. Retornar à main
git checkout main
git pull origin main
```

---

## ❓ Dúvidas?

Se tiver dúvidas sobre os comandos, consulte a documentação oficial do Git:
https://git-scm.com/doc

Ou execute no terminal:
```bash
git help <comando>
# Exemplo:
git help branch
git help commit
```
