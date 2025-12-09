from typing import List, Optional
from sqlalchemy.orm import Session
from app.models import Course
from app.schemas import CourseCreate, CourseUpdate


class CourseRepository:
    """Repositório para operações com cursos"""
    
    def __init__(self, db: Session):
        self.db = db
    
    def create_course(self, course_data: CourseCreate) -> Course:
        """Criar novo curso"""
        course = Course(
            name=course_data.name,
            code=course_data.code,
            description=course_data.description,
            minimum_months=course_data.minimum_months,
            accepted_positions=course_data.accepted_positions,
            is_active=course_data.is_active
        )
        self.db.add(course)
        self.db.commit()
        self.db.refresh(course)
        return course
    
    def get_course(self, course_id: int) -> Optional[Course]:
        """Buscar curso por ID"""
        return self.db.query(Course).filter(Course.id == course_id).first()
    
    def get_course_by_code(self, code: str) -> Optional[Course]:
        """Buscar curso por código"""
        return self.db.query(Course).filter(Course.code == code).first()
    
    def get_all_courses(
        self,
        skip: int = 0,
        limit: int = 100,
        active_only: bool = False
    ) -> List[Course]:
        """Listar todos os cursos"""
        query = self.db.query(Course)
        if active_only:
            query = query.filter(Course.is_active == True)
        return query.offset(skip).limit(limit).all()
    
    def update_course(
        self,
        course_id: int,
        course_data: CourseUpdate
    ) -> Optional[Course]:
        """Atualizar curso"""
        course = self.get_course(course_id)
        if not course:
            return None
        
        update_data = course_data.model_dump(exclude_unset=True)
        for field, value in update_data.items():
            setattr(course, field, value)
        
        self.db.commit()
        self.db.refresh(course)
        return course
    
    def delete_course(self, course_id: int) -> bool:
        """Deletar curso"""
        course = self.get_course(course_id)
        if course:
            self.db.delete(course)
            self.db.commit()
            return True
        return False
    
    def count_courses(self) -> int:
        """Contar total de cursos"""
        return self.db.query(Course).count()
