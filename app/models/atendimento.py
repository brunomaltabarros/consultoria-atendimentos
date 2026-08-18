from sqlalchemy import Column, Integer, String, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from app.database import Base

class Atendimento(Base):
    __tablename__ = "atendimentos"
    id = Column(Integer, primary_key=True, index=True)
    consultor_id = Column(Integer, ForeignKey("consultores.id"), nullable=False)
    cliente_nome = Column(String, nullable=False)
    data_atendimento = Column(DateTime, nullable=False)
    descricao = Column(String, nullable=False)
    tipo = Column(String, nullable=False)
    consultor = relationship("Consultor", back_populates="atendimentos")