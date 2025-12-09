from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.repositories import DocumentRepository, CourseRepository
from app.services import ValidationService, ReportService
from app.schemas import (
    ValidationRequest,
    ValidationResponse,
    ReportResponse
)

router = APIRouter(prefix="/validations", tags=["validations"])


@router.post("/", response_model=ValidationResponse, status_code=status.HTTP_201_CREATED)
async def validate_document(
    validation_request: ValidationRequest,
    db: Session = Depends(get_db)
):
    """
    Validar experiência profissional de um documento para um curso específico
    """
    doc_repo = DocumentRepository(db)
    course_repo = CourseRepository(db)
    
    # Verificar se documento existe
    document = doc_repo.get_document(validation_request.document_id)
    if not document:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Documento não encontrado"
        )
    
    # Verificar se curso existe
    course = course_repo.get_course(validation_request.course_id)
    if not course:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Curso não encontrado"
        )
    
    # Buscar extrações do documento
    extractions = doc_repo.get_extractions_by_document(validation_request.document_id)
    if not extractions:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Documento não possui dados extraídos. Execute a extração primeiro."
        )
    
    # Validar primeira extração (pode ser expandido para validar todas)
    validation_service = ValidationService()
    validation_result = validation_service.validate_experience(extractions[0], course)
    
    # Salvar validação no banco
    validation = doc_repo.create_validation(
        document_id=validation_request.document_id,
        course_id=validation_request.course_id,
        status=validation_result["status"],
        required_months=validation_result["required_months"],
        found_months=validation_result["found_months"],
        position_match=validation_result.get("position_match"),
        validation_details=validation_result.get("details")
    )
    
    return validation


@router.get("/{validation_id}", response_model=ValidationResponse)
async def get_validation(
    validation_id: int,
    db: Session = Depends(get_db)
):
    """
    Buscar validação por ID
    """
    repo = DocumentRepository(db)
    validation = repo.get_validation(validation_id)
    
    if not validation:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Validação não encontrada"
        )
    
    return validation


@router.get("/document/{document_id}", response_model=List[ValidationResponse])
async def get_document_validations(
    document_id: int,
    db: Session = Depends(get_db)
):
    """
    Buscar todas as validações de um documento
    """
    repo = DocumentRepository(db)
    document = repo.get_document(document_id)
    
    if not document:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Documento não encontrado"
        )
    
    validations = repo.get_validations_by_document(document_id)
    return validations


@router.get("/{validation_id}/summary")
async def get_validation_summary(
    validation_id: int,
    db: Session = Depends(get_db)
):
    """
    Gerar resumo detalhado de uma validação
    """
    report_service = ReportService()
    summary = report_service.generate_validation_summary(validation_id, db)
    
    if "error" in summary:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=summary["error"]
        )
    
    return summary
