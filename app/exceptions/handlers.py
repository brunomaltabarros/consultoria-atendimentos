from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from app.exceptions.exceptions import ExcecaoAplicacao, ExcecaoConflito, ExcecaoNaoEncontrado

def registrar_tratadores_excecao(app: FastAPI) -> None:
    @app.exception_handler(ExcecaoNaoEncontrado)
    def tratar_nao_encontrado(requisicao: Request, erro: ExcecaoNaoEncontrado) -> JSONResponse:
        return JSONResponse(
            status_code=404,
            content={"erro": erro.messagem})
    
    @app.exception_handler(ExcecaoConflito)
    def tratar_conflito(requisicao: Request, erro: ExcecaoConflito) -> JSONResponse:
        return JSONResponse(
            status_code= 409,
            content={"erro": erro.messagem})
    
    @app.exception_handler(ExcecaoAplicacao)
    def tratar_excecao_aplicacao(requisicao: Request, erro: ExcecaoAplicacao) -> JSONResponse:
        return JSONResponse(
            status_code=500,
            content={"erro": erro.messagem})
    
    @app.exception_handler(Exception)
    def tratar_excecao_inesperada(requisicao: Request, erro: Exception) -> JSONResponse:
        return JSONResponse(
            status_code=500,
            content={"erro": "Ocorreu um erro interno no servidor. Por favor, tente novamente mais tarde."})