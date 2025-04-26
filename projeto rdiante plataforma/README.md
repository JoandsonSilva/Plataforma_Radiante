# Radiante Perfumaria

Plataforma de gestão para perfumaria com controle de revendedores e sistema de tarefas.

## Funcionalidades

- Sistema de autenticação para administradores e revendedores
- Gestão de produtos e estoque
- Controle de revendedores
- Sistema de tarefas similar ao Trello
- Dashboard com métricas importantes
- Interface moderna e responsiva

## Tecnologias Utilizadas

- Backend: Python (Flask)
- Frontend: HTML, CSS, JavaScript
- Banco de Dados: SQLite (desenvolvimento) / PostgreSQL (produção)
- Autenticação: Flask-Login
- Formulários: Flask-WTF

## Instalação

1. Clone o repositório
2. Crie um ambiente virtual:
```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate     # Windows
```
3. Instale as dependências:
```bash
pip install -r requirements.txt
```
4. Configure as variáveis de ambiente:
```bash
cp .env.example .env
```
5. Execute a aplicação:
```bash
python app.py
```

## Estrutura do Projeto

```
radiante-perfumaria/
├── app/
│   ├── __init__.py
│   ├── models/
│   ├── routes/
│   ├── static/
│   └── templates/
├── instance/
├── migrations/
├── .env
├── .gitignore
├── app.py
├── config.py
└── requirements.txt
``` 