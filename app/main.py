from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app import models
from app.controllers import atendimento_controller, auth_controller, consultor_controller, especialidade_controller, usuario_controller
from app.exceptions.handlers import registrar_tratadores_excecao

app = FastAPI(title="Portal do Credenciamento")

ORIGENS_PERMITIDAS = ["http://localhost:5173", "http://127.0.0.1:5173"]
app.add_middleware(
    CORSMiddleware,
    allow_origins=ORIGENS_PERMITIDAS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

registrar_tratadores_excecao(app)

app .include_router(atendimento_controller.rotas)
app .include_router(auth_controller.rotas)
app .include_router(consultor_controller.rotas)
app .include_router(especialidade_controller.rotas)
app .include_router(usuario_controller.rotas)

@app.get("/")
def raiz():
    return {"mensagem": "Olá, Mundo!"}