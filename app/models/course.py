from sqlalchemy import Column, Integer, String, Text, JSON, Boolean
from sqlalchemy.orm import relationship
from app.core.database import Base


class Course(Base):
    """Modelo para cursos técnicos"""
    __tablename__ = "courses"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=False, unique=True)
    code = Column(String(50), nullable=False, unique=True)
    description = Column(Text)
    
    # Requisitos de experiência
    minimum_months = Column(Integer, nullable=False, default=12)
    accepted_positions = Column(JSON)  # Lista de cargos aceitos
    
    # Configurações
    is_active = Column(Boolean, default=True)
    
    # Relacionamento
    validations = relationship("Validation", back_populates="course")
