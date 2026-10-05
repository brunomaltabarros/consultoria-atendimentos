import os

CHAVE_SECRETA = os.environ.get('CHAVE_SECRETA', 'chave-secreta-de-desenvolvimento-trocar-em-producao')
ALGORITMO = "HS256"
MINUTOS_EXPIRACAO_TOKEN = int(os.getenv('MINUTOS_EXPIRACAO_TOKEN', 60))