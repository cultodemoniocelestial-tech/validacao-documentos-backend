from sqlalchemy import Column, Integer, String, DateTime, Text, JSON, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime
from app.core.database import Base


class Document(Base):
    """Modelo para documentos enviados"""
    __tablename__ = "documents"
    
    id = Column(Integer, primary_key=True, index=True)
    filename = Column(String(255), nullable=False)
    file_path = Column(String(500), nullable=False)
    file_type = Column(String(50), nullable=False)  # pdf, image
    uploaded_at = Column(DateTime, default=datetime.utcnow)
    
    # Relacionamento com extrações
    extractions = relationship("DocumentExtraction", back_populates="document", cascade="all, delete-orphan")
    validations = relationship("Validation", back_populates="document", cascade="all, delete-orphan")


class DocumentExtraction(Base):
    """Modelo para dados extraídos do documento"""
    __tablename__ = "document_extractions"
    
    id = Column(Integer, primary_key=True, index=True)
    document_id = Column(Integer, ForeignKey("documents.id"), nullable=False)
    
    # Dados extraídos
    company_name = Column(String(255))
    position = Column(String(255))
    start_date = Column(String(50))
    end_date = Column(String(50))
    months_worked = Column(Integer)
    
    # OCR raw data
    raw_text = Column(Text)
    extracted_data = Column(JSON)
    
    extracted_at = Column(DateTime, default=datetime.utcnow)
    
    # Relacionamento
    document = relationship("Document", back_populates="extractions")


class Validation(Base):
    """Modelo para validações realizadas"""
    __tablename__ = "validations"
    
    id = Column(Integer, primary_key=True, index=True)
    document_id = Column(Integer, ForeignKey("documents.id"), nullable=False)
    course_id = Column(Integer, ForeignKey("courses.id"), nullable=False)
    
    # Resultado da validação
    status = Column(String(50), nullable=False)  # approved, rejected, manual_review
    required_months = Column(Integer)
    found_months = Column(Integer)
    position_match = Column(String(255))
    
    # Detalhes
    validation_details = Column(JSON)
    validated_at = Column(DateTime, default=datetime.utcnow)
    
    # Relacionamentos
    document = relationship("Document", back_populates="validations")
    course = relationship("Course", back_populates="validations")
