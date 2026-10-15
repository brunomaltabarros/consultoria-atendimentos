from sqlalchemy import Column, Integer, String
from app.database import Base
from sqlalchemy.orm import relationship
from app.models.especialidade import consultor_especialidade 

class Consultor(Base):
    __tablename__ = "consultores"

    id = Column(Integer, primary_key=True, index=True)
    nome = Column(String, nullable=False)
    cpf = Column(String, nullable=True, unique=True)
    email = Column(String, nullable=False, unique=True)
    telefone = Column(String, nullable=False)
    bio = Column(String, nullable=True)

    atendimentos = relationship("Atendimento", back_populates="consultor")
    especialidades = relationship(
        "Especialidade",
        secondary=consultor_especialidade,
        back_populates="consultores",
    )