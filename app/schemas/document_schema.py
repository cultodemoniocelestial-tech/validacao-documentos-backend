from pydantic import BaseModel, Field
from typing import Optional, List, Dict, Any
from datetime import datetime


class DocumentUploadResponse(BaseModel):
    """Resposta do upload de documento"""
    id: int
    filename: str
    file_path: str
    file_type: str
    uploaded_at: datetime
    
    class Config:
        from_attributes = True


class ExtractionData(BaseModel):
    """Dados extraídos de um documento"""
    company_name: Optional[str] = None
    position: Optional[str] = None
    start_date: Optional[str] = None
    end_date: Optional[str] = None
    months_worked: Optional[int] = None


class DocumentExtractionResponse(BaseModel):
    """Resposta da extração de dados"""
    id: int
    document_id: int
    company_name: Optional[str]
    position: Optional[str]
    start_date: Optional[str]
    end_date: Optional[str]
    months_worked: Optional[int]
    raw_text: Optional[str]
    extracted_data: Optional[Dict[str, Any]]
    extracted_at: datetime
    
    class Config:
        from_attributes = True


class ValidationRequest(BaseModel):
    """Requisição de validação"""
    document_id: int
    course_id: int


class ValidationResponse(BaseModel):
    """Resposta da validação"""
    id: int
    document_id: int
    course_id: int
    status: str  # approved, rejected, manual_review
    required_months: Optional[int]
    found_months: Optional[int]
    position_match: Optional[str]
    validation_details: Optional[Dict[str, Any]]
    validated_at: datetime
    
    class Config:
        from_attributes = True


class ReportResponse(BaseModel):
    """Resposta do relatório completo"""
    document: DocumentUploadResponse
    extractions: List[DocumentExtractionResponse]
    validations: List[ValidationResponse]
    summary: Dict[str, Any]
