from sqlalchemy import create_engine, event
from sqlalchemy.orm import sessionmaker, declarative_base

URL_BANCO = "sqlite:///./consultoria.db"

engine = create_engine(URL_BANCO, connect_args={'check_same_thread': False})

@event.listens_for(engine, "connect")
def habilitar_foreign_keys(conexao, registro_conexao):
    cursor = conexao.cursor()
    cursor.execute("PRAGMA foreign_keys=ON")
    cursor.close()

SessaoLocal = sessionmaker (autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

def obter_sessao():
    sessao = SessaoLocal()
    try:
        yield sessao
    finally:
        sessao.close()