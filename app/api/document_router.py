import os
import shutil
from typing import List
from fastapi import APIRouter, Depends, UploadFile, File, HTTPException, status
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.core.config import settings
from app.repositories import DocumentRepository
from app.services import OCRService
from app.schemas import (
    DocumentUploadResponse,
    DocumentExtractionResponse
)

router = APIRouter(prefix="/documents", tags=["documents"])


@router.post("/upload", response_model=DocumentUploadResponse, status_code=status.HTTP_201_CREATED)
async def upload_document(
    file: UploadFile = File(...),
    db: Session = Depends(get_db)
):
    """
    Upload de documento (imagem ou PDF) para extração de dados
    """
    # Validar tipo de arquivo
    allowed_extensions = ['.pdf', '.jpg', '.jpeg', '.png']
    file_extension = os.path.splitext(file.filename)[1].lower()
    
    if file_extension not in allowed_extensions:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Tipo de arquivo não permitido. Use: {', '.join(allowed_extensions)}"
        )
    
    # Validar tamanho do arquivo
    file.file.seek(0, 2)
    file_size = file.file.tell()
    file.file.seek(0)
    
    if file_size > settings.MAX_UPLOAD_SIZE:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Arquivo muito grande. Tamanho máximo: {settings.MAX_UPLOAD_SIZE / 1024 / 1024}MB"
        )
    
    # Criar diretório de upload se não existir
    os.makedirs(settings.UPLOAD_DIR, exist_ok=True)
    
    # Salvar arquivo
    file_path = os.path.join(settings.UPLOAD_DIR, file.filename)
    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)
    
    # Determinar tipo de arquivo
    file_type = "pdf" if file_extension == ".pdf" else "image"
    
    # Salvar no banco de dados
    repo = DocumentRepository(db)
    document = repo.create_document(
        filename=file.filename,
        file_path=file_path,
        file_type=file_type
    )
    
    return document


@router.post("/{document_id}/extract", response_model=List[DocumentExtractionResponse])
async def extract_document_data(
    document_id: int,
    db: Session = Depends(get_db)
):
    """
    Extrair dados de um documento usando OCR
    """
    repo = DocumentRepository(db)
    document = repo.get_document(document_id)
    
    if not document:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Documento não encontrado"
        )
    
    # Verificar se arquivo existe
    if not os.path.exists(document.file_path):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Arquivo do documento não encontrado"
        )
    
    # Extrair texto usando OCR
    ocr_service = OCRService()
    raw_text = ocr_service.extract_text(document.file_path, document.file_type)
    
    if not raw_text:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail="Não foi possível extrair texto do documento"
        )
    
    # Parsear experiências profissionais
    experiences = ocr_service.parse_work_experience(raw_text)
    
    if not experiences:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail="Não foi possível identificar experiências profissionais no documento"
        )
    
    # Salvar extrações no banco
    extractions = []
    for exp in experiences:
        extraction = repo.create_extraction(
            document_id=document.id,
            company_name=exp.get('company_name'),
            position=exp.get('position'),
            start_date=exp.get('start_date'),
            end_date=exp.get('end_date'),
            months_worked=exp.get('months_worked'),
            raw_text=raw_text,
            extracted_data=exp
        )
        extractions.append(extraction)
    
    return extractions


@router.get("/{document_id}", response_model=DocumentUploadResponse)
async def get_document(
    document_id: int,
    db: Session = Depends(get_db)
):
    """
    Buscar informações de um documento
    """
    repo = DocumentRepository(db)
    document = repo.get_document(document_id)
    
    if not document:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Documento não encontrado"
        )
    
    return document


@router.get("/{document_id}/extractions", response_model=List[DocumentExtractionResponse])
async def get_document_extractions(
    document_id: int,
    db: Session = Depends(get_db)
):
    """
    Buscar todas as extrações de um documento
    """
    repo = DocumentRepository(db)
    document = repo.get_document(document_id)
    
    if not document:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Documento não encontrado"
        )
    
    extractions = repo.get_extractions_by_document(document_id)
    return extractions


@router.get("/", response_model=List[DocumentUploadResponse])
async def list_documents(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db)
):
    """
    Listar todos os documentos
    """
    repo = DocumentRepository(db)
    documents = repo.get_all_documents(skip=skip, limit=limit)
    return documents


@router.delete("/{document_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_document(
    document_id: int,
    db: Session = Depends(get_db)
):
    """
    Deletar um documento e seus dados relacionados
    """
    repo = DocumentRepository(db)
    document = repo.get_document(document_id)
    
    if not document:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Documento não encontrado"
        )
    
    # Deletar arquivo físico
    if os.path.exists(document.file_path):
        os.remove(document.file_path)
    
    # Deletar do banco
    repo.delete_document(document_id)
    
    return None
