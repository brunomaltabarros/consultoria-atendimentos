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
