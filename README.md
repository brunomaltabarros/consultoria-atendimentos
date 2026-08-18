# Consultoria Atendimentos

API para cadastro de consultores e registro de atendimentos, desenvolvida como
trabalho da AV01.

## Requisitos atendidos

- Arquitetura em MVC
- Pattern Repository
- Pattern DTO
- Pattern Mapper
- Endpoints GET, POST, PUT e DELETE
- Persistência via ORM
- Documentação via Swagger

## Stack

- Python 3.12
- FastAPI
- SQLAlchemy (ORM)
- SQLite

## Como rodar

```bash
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
uvicorn app.main:app --reload
```

Depois, acesse a documentação Swagger em http://127.0.0.1:8000/docs
