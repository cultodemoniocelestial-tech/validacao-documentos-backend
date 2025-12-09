from typing import List, Optional
from sqlalchemy.orm import Session
from app.models import Document, DocumentExtraction, Validation


class DocumentRepository:
    """Repositório para operações com documentos"""
    
    def __init__(self, db: Session):
        self.db = db
    
    def create_document(
        self,
        filename: str,
        file_path: str,
        file_type: str
    ) -> Document:
        """Criar novo documento"""
        document = Document(
            filename=filename,
            file_path=file_path,
            file_type=file_type
        )
        self.db.add(document)
        self.db.commit()
        self.db.refresh(document)
        return document
    
    def get_document(self, document_id: int) -> Optional[Document]:
        """Buscar documento por ID"""
        return self.db.query(Document).filter(Document.id == document_id).first()
    
    def get_all_documents(self, skip: int = 0, limit: int = 100) -> List[Document]:
        """Listar todos os documentos"""
        return self.db.query(Document).offset(skip).limit(limit).all()
    
    def delete_document(self, document_id: int) -> bool:
        """Deletar documento"""
        document = self.get_document(document_id)
        if document:
            self.db.delete(document)
            self.db.commit()
            return True
        return False
    
    def create_extraction(
        self,
        document_id: int,
        company_name: Optional[str],
        position: Optional[str],
        start_date: Optional[str],
        end_date: Optional[str],
        months_worked: Optional[int],
        raw_text: Optional[str],
        extracted_data: Optional[dict]
    ) -> DocumentExtraction:
        """Criar nova extração de dados"""
        extraction = DocumentExtraction(
            document_id=document_id,
            company_name=company_name,
            position=position,
            start_date=start_date,
            end_date=end_date,
            months_worked=months_worked,
            raw_text=raw_text,
            extracted_data=extracted_data
        )
        self.db.add(extraction)
        self.db.commit()
        self.db.refresh(extraction)
        return extraction
    
    def get_extractions_by_document(self, document_id: int) -> List[DocumentExtraction]:
        """Buscar todas as extrações de um documento"""
        return self.db.query(DocumentExtraction).filter(
            DocumentExtraction.document_id == document_id
        ).all()
    
    def create_validation(
        self,
        document_id: int,
        course_id: int,
        status: str,
        required_months: Optional[int],
        found_months: Optional[int],
        position_match: Optional[str],
        validation_details: Optional[dict]
    ) -> Validation:
        """Criar nova validação"""
        validation = Validation(
            document_id=document_id,
            course_id=course_id,
            status=status,
            required_months=required_months,
            found_months=found_months,
            position_match=position_match,
            validation_details=validation_details
        )
        self.db.add(validation)
        self.db.commit()
        self.db.refresh(validation)
        return validation
    
    def get_validations_by_document(self, document_id: int) -> List[Validation]:
        """Buscar todas as validações de um documento"""
        return self.db.query(Validation).filter(
            Validation.document_id == document_id
        ).all()
    
    def get_validation(self, validation_id: int) -> Optional[Validation]:
        """Buscar validação por ID"""
        return self.db.query(Validation).filter(Validation.id == validation_id).first()
