# 📚 Sistema de Biblioteca Escolar

Sistema web para gerenciamento de bibliotecas escolares, desenvolvido com Python. O projeto permite o controle de livros, alunos e empréstimos de forma simples, organizada e eficiente.

## 🚀 Tecnologias Utilizadas

### Backend

* Python
* FastAPI
* MongoDB
* Pydantic
* JWT Authentication

### Frontend

* NiceGUI
* HTTPX
* Python

## 📋 Funcionalidades

### 📖 Gerenciamento de Livros

* Cadastro de livros
* Edição de informações
* Exclusão de livros
* Consulta de acervo
* Controle de disponibilidade

### 👨‍🎓 Gerenciamento de Alunos

* Cadastro de alunos
* Atualização de dados
* Consulta de alunos cadastrados
* Histórico de empréstimos

### 🔄 Controle de Empréstimos

* Registro de empréstimos
* Registro de devoluções
* Controle de livros em atraso
* Histórico de movimentações

### 📊 Dashboard

* Quantidade total de livros
* Quantidade de alunos cadastrados
* Empréstimos ativos
* Livros disponíveis
* Indicadores gerais do sistema

## 📂 Estrutura do Projeto

```text
biblioteca/
│
├── backend/
│   ├── app/
│   ├── routes/
│   ├── models/
│   ├── schemas/
│   ├── services/
│   ├── database/
│   └── main.py
│
├── frontend/
│   ├── components/
│   ├── screens/
│   ├── services/
│   ├── utils/
│   └── main.py
│
└── README.md
```

## ⚙️ Instalação

### Clonar o repositório

```bash
git clone https://github.com/seu-usuario/seu-repositorio.git
```

### Backend

```bash
cd backend

python -m venv venv

# Windows
venv\Scripts\activate

pip install -r requirements.txt

uvicorn main:app --reload
```

### Frontend

```bash
cd frontend

python -m venv venv

# Windows
venv\Scripts\activate

pip install -r requirements.txt

python main.py
```

## 🌐 Variáveis de Ambiente

### Backend (.env)

```env
MONGO_URI=
DATABASE_NAME=

```

### Frontend (.env)

```env
API_BASE_URL=http://localhost:8000
```

## ☁️ Deploy

### Backend

* Render


### Frontend

* Render

O sistema está preparado para utilizar a porta fornecida automaticamente pelo serviço de hospedagem através da variável de ambiente `PORT`.

## 🎯 Objetivo

Este projeto foi desenvolvido para auxiliar escolas no gerenciamento do acervo bibliográfico, automatizando processos de empréstimo e devolução, reduzindo erros e facilitando o acesso às informações da biblioteca.

## 👨‍💻 Autor

João Emanuel Carlos Lima

* GitHub: https://github.com/joao-tec-info
* LinkedIn: https://linkedin.com/in/joao-emanuel-carlos-lima
