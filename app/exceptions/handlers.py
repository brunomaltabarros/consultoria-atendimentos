from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from app.exceptions.exceptions import AppException, ConflictException, NotFoundException

def register_exception_handlers(app: FastAPI) -> None:
    @app.exception_handler(NotFoundException)
    def handle_not_found(request: Request, exc: NotFoundException) -> JSONResponse:
        return JSONResponse(
            status_code=404,
            content={"erro": exc.message})
    
    @app.exception_handler(ConflictException)
    def handle_conflict(request: Request, exc: ConflictException) -> JSONResponse:
        return JSONResponse(
            status_code= 409,
            content={"erro": exc.message})
    
    @app.exception_handler(AppException)
    def handle_app_exception(request: Request, exc: AppException) -> JSONResponse:
        return JSONResponse(
            status_code=500,
            content={"erro": exc.message})
    
    @app.exception_handler(Exception)
    def handle_unexpected_exception(request: Request, exc: Exception) -> JSONResponse:
        return JSONResponse(
            status_code=500,
            content={"erro": "Ocorreu um erro interno no servidor. Por favor, tente novamente mais tarde."})