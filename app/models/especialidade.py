from sqlalchemy import Column, ForeignKey, Integer, String, Table
from sqlalchemy.orm import relationship
from app.database import Base

consultor_especialidade = Table(
    "consultor_especialidade",
    Base.metadata,
    Column("consultor_id", Integer, ForeignKey("consultores.id"), primary_key=True),
    Column("especialidade_id", Integer, ForeignKey("especialidades.id"), primary_key=True),
)

class Especialidade(Base):
    __tablename__ = "especialidades"

    id = Column(Integer, primary_key=True, index=True)
    nome = Column(String, nullable=False, unique=True, index=True)
    descricao = Column(String, nullable = True)

    consultores = relationship(
        "Consultor",
        secondary=consultor_especialidade,
        back_populates="especialidades",
    )