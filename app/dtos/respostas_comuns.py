from app.dtos.erro_dto import ErroRespostaDTO

RESPOSTA_400 = {400: {"model": ErroRespostaDTO, "description": "Requisição inválida"}}
RESPOSTA_401 = {401: {"model": ErroRespostaDTO, "description": "Token ausente, inválido ou expirado"}}
RESPOSTA_403 = {403: {"model": ErroRespostaDTO, "description": "Sem permissão para esta operação"}}
RESPOSTA_404 = {404: {"model": ErroRespostaDTO, "description": "Recurso não encontrado"}}
RESPOSTA_409 = {409: {"model": ErroRespostaDTO, "description": "Conflito com um registro existente"}}
RESPOSTA_401_CREDENCIAIS = {401: {"model": ErroRespostaDTO, "description": "E-mail ou senha inválidos"}}