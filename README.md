# 🍲 App Receitas

Aplicação web de receitas desenvolvida com **Django**, criada para compartilhar, visualizar e organizar receitas de forma prática e visual.

Este projeto demonstra um sistema completo com renderização de templates, organização de rotas, estrutura de pastas bem definida e deploy em plataforma de nuvem.

---

## 🚀 Visão Geral

O projeto consiste em um **site de receitas** onde usuários podem:
- Navegar por receitas
- Visualizar detalhes (nome, ingredientes, preparo)
- Filtrar ou buscar (conforme extensão do projeto)

🔗 Demo online: https://app-receitas-cy3g.onrender.com/ :contentReference[oaicite:1]{index=1}

---

## 🛠️ Tecnologias Utilizadas

### Back-end
- 🐍 **Python**
- 🌐 **Django**

### Front-end
- 📄 **HTML5**
- 🎨 **CSS3**

### Outros
- 🐘 **PostgreSQL** (deploy)
- ☁️ **Render** (deploy platform)
- ☁️ **Cloudinary**

---

## ⚙️ Como Rodar o Projeto Localmente

1️⃣ Clone o repositório

- git clone https://github.com/ronesanttos/app-receitas.git
cd app-receitas

2️⃣ Crie e ative um ambiente virtual
- python -m venv venv
  
- Windows
 venv\Scripts\activate

 - Linux / Mac
 source venv/bin/activate

3️⃣ Instale as dependências
- pip install -r requirements.txt

4️⃣ Configure o banco de dados
Você pode rodar com SQLite localmente (padrão) ou apontar para um PostgreSQL.
Se for local (padrão):
- python manage.py migrate

5️⃣ Rodar o servidor
- python manage.py runserver

---

👨‍💻 Autor

Rone Santos
Desenvolvedor Full Stack
🐍 Python | Django | JavaScript

🔗 GitHub: https://github.com/ronesanttos
