from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.services import ReportService

router = APIRouter(prefix="/reports", tags=["reports"])


@router.get("/document/{document_id}")
async def get_document_report(
    document_id: int,
    db: Session = Depends(get_db)
):
    """
    Gerar relatório completo de um documento
    Inclui: informações do documento, extrações e validações
    """
    report_service = ReportService()
    report = report_service.generate_document_report(document_id, db)
    
    if "error" in report:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=report["error"]
        )
    
    return report


@router.get("/course/{course_id}/statistics")
async def get_course_statistics(
    course_id: int,
    db: Session = Depends(get_db)
):
    """
    Gerar estatísticas de validações de um curso
    """
    report_service = ReportService()
    statistics = report_service.generate_course_statistics(course_id, db)
    
    if "error" in statistics:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=statistics["error"]
        )
    
    return statistics
