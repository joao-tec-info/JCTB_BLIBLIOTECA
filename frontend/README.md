# Biblioteca Escolar — Frontend NiceGUI

Frontend visual para o sistema de gerenciamento de biblioteca escolar municipal.

## Como executar

```bash
pip install nicegui
cd biblioteca_frontend
python main.py
```

Acesse: http://localhost:8080

## Rotas

- `/` — Dashboard
- `/livros` — CRUD de livros
- `/alunos` — CRUD de alunos
- `/emprestimos` — Empréstimos (ativos / histórico)
- `/login` — Tela de login (visual)

## Estrutura

```
biblioteca_frontend/
├── main.py
├── components/      # navbar, sidebar, formulários, cards
├── screens/         # telas (dashboard, livros, alunos, empréstimos, login)
├── services/        # api_service.py (mock — substituir por chamadas FastAPI)
├── utils/           # constants.py, helpers.py
└── assets/
```

## Integração com a API

Os dados estão mockados em `services/api_service.py`.
Para conectar ao backend FastAPI/MongoDB, substitua os métodos da classe
`APIService` por chamadas HTTP (ex.: `httpx`), mantendo a mesma interface
pública usada pelas telas.
