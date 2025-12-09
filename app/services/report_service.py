from typing import Dict, Any, List
from datetime import datetime
from sqlalchemy.orm import Session
from app.models import Document, DocumentExtraction, Validation, Course


class ReportService:
    """Serviço para geração de relatórios"""
    
    def generate_document_report(
        self,
        document_id: int,
        db: Session
    ) -> Dict[str, Any]:
        """
        Gerar relatório completo de um documento
        """
        # Buscar documento
        document = db.query(Document).filter(Document.id == document_id).first()
        if not document:
            return {"error": "Documento não encontrado"}
        
        # Buscar extrações
        extractions = db.query(DocumentExtraction).filter(
            DocumentExtraction.document_id == document_id
        ).all()
        
        # Buscar validações
        validations = db.query(Validation).filter(
            Validation.document_id == document_id
        ).all()
        
        # Calcular estatísticas
        total_months = sum(e.months_worked or 0 for e in extractions)
        approved_validations = [v for v in validations if v.status == "approved"]
        rejected_validations = [v for v in validations if v.status == "rejected"]
        manual_review_validations = [v for v in validations if v.status == "manual_review"]
        
        # Montar relatório
        report = {
            "document": {
                "id": document.id,
                "filename": document.filename,
                "file_type": document.file_type,
                "uploaded_at": document.uploaded_at.isoformat()
            },
            "extractions": [
                {
                    "id": e.id,
                    "company_name": e.company_name,
                    "position": e.position,
                    "start_date": e.start_date,
                    "end_date": e.end_date,
                    "months_worked": e.months_worked,
                    "extracted_at": e.extracted_at.isoformat()
                }
                for e in extractions
            ],
            "validations": [
                {
                    "id": v.id,
                    "course_id": v.course_id,
                    "course_name": v.course.name if v.course else None,
                    "status": v.status,
                    "required_months": v.required_months,
                    "found_months": v.found_months,
                    "position_match": v.position_match,
                    "validation_details": v.validation_details,
                    "validated_at": v.validated_at.isoformat()
                }
                for v in validations
            ],
            "summary": {
                "total_experiences": len(extractions),
                "total_months_worked": total_months,
                "total_validations": len(validations),
                "approved_validations": len(approved_validations),
                "rejected_validations": len(rejected_validations),
                "manual_review_validations": len(manual_review_validations),
                "generated_at": datetime.utcnow().isoformat()
            }
        }
        
        return report
    
    def generate_validation_summary(
        self,
        validation_id: int,
        db: Session
    ) -> Dict[str, Any]:
        """
        Gerar resumo de uma validação específica
        """
        validation = db.query(Validation).filter(Validation.id == validation_id).first()
        if not validation:
            return {"error": "Validação não encontrada"}
        
        # Buscar informações relacionadas
        document = validation.document
        course = validation.course
        extraction = db.query(DocumentExtraction).filter(
            DocumentExtraction.document_id == document.id
        ).first()
        
        summary = {
            "validation_id": validation.id,
            "status": validation.status,
            "document": {
                "id": document.id,
                "filename": document.filename
            },
            "course": {
                "id": course.id,
                "name": course.name,
                "code": course.code,
                "minimum_months": course.minimum_months,
                "accepted_positions": course.accepted_positions
            },
            "experience": {
                "company_name": extraction.company_name if extraction else None,
                "position": extraction.position if extraction else None,
                "months_worked": extraction.months_worked if extraction else None
            },
            "validation_result": {
                "required_months": validation.required_months,
                "found_months": validation.found_months,
                "position_match": validation.position_match,
                "details": validation.validation_details
            },
            "validated_at": validation.validated_at.isoformat()
        }
        
        return summary
    
    def generate_course_statistics(
        self,
        course_id: int,
        db: Session
    ) -> Dict[str, Any]:
        """
        Gerar estatísticas de validações de um curso
        """
        course = db.query(Course).filter(Course.id == course_id).first()
        if not course:
            return {"error": "Curso não encontrado"}
        
        validations = db.query(Validation).filter(Validation.course_id == course_id).all()
        
        approved = [v for v in validations if v.status == "approved"]
        rejected = [v for v in validations if v.status == "rejected"]
        manual_review = [v for v in validations if v.status == "manual_review"]
        
        statistics = {
            "course": {
                "id": course.id,
                "name": course.name,
                "code": course.code,
                "minimum_months": course.minimum_months
            },
            "validations": {
                "total": len(validations),
                "approved": len(approved),
                "rejected": len(rejected),
                "manual_review": len(manual_review),
                "approval_rate": len(approved) / len(validations) * 100 if validations else 0
            },
            "generated_at": datetime.utcnow().isoformat()
        }
        
        return statistics
