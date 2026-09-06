from fastapi import FastAPI

from app import models
from app.controllers import atendimento_controller, consultor_controller
from app.database import Base, engine
from app.exceptions.handlers import registrar_tratadores_excecao

Base.metadata.create_all(bind=engine)

app = FastAPI(title="Portal do Credenciamento")

registrar_tratadores_excecao(app)

app .include_router(atendimento_controller.rotas)
app .include_router(consultor_controller.rotas)

@app.get("/")
def root():
    return {"mensagem": "Olá, Mundo!"}