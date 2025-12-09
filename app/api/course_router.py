from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.repositories import CourseRepository
from app.schemas import (
    CourseCreate,
    CourseUpdate,
    CourseResponse,
    CourseListResponse
)

router = APIRouter(prefix="/courses", tags=["courses"])


@router.post("/", response_model=CourseResponse, status_code=status.HTTP_201_CREATED)
async def create_course(
    course_data: CourseCreate,
    db: Session = Depends(get_db)
):
    """
    Criar novo curso técnico
    """
    repo = CourseRepository(db)
    
    # Verificar se código já existe
    existing = repo.get_course_by_code(course_data.code)
    if existing:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Curso com código '{course_data.code}' já existe"
        )
    
    course = repo.create_course(course_data)
    return course


@router.get("/", response_model=CourseListResponse)
async def list_courses(
    skip: int = 0,
    limit: int = 100,
    active_only: bool = False,
    db: Session = Depends(get_db)
):
    """
    Listar todos os cursos
    """
    repo = CourseRepository(db)
    courses = repo.get_all_courses(skip=skip, limit=limit, active_only=active_only)
    total = repo.count_courses()
    
    return {
        "courses": courses,
        "total": total
    }


@router.get("/{course_id}", response_model=CourseResponse)
async def get_course(
    course_id: int,
    db: Session = Depends(get_db)
):
    """
    Buscar curso por ID
    """
    repo = CourseRepository(db)
    course = repo.get_course(course_id)
    
    if not course:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Curso não encontrado"
        )
    
    return course


@router.put("/{course_id}", response_model=CourseResponse)
async def update_course(
    course_id: int,
    course_data: CourseUpdate,
    db: Session = Depends(get_db)
):
    """
    Atualizar curso existente
    """
    repo = CourseRepository(db)
    
    # Verificar se curso existe
    existing = repo.get_course(course_id)
    if not existing:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Curso não encontrado"
        )
    
    # Verificar se novo código já existe em outro curso
    if course_data.code:
        code_exists = repo.get_course_by_code(course_data.code)
        if code_exists and code_exists.id != course_id:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Código '{course_data.code}' já está em uso"
            )
    
    course = repo.update_course(course_id, course_data)
    return course


@router.delete("/{course_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_course(
    course_id: int,
    db: Session = Depends(get_db)
):
    """
    Deletar curso
    """
    repo = CourseRepository(db)
    course = repo.get_course(course_id)
    
    if not course:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Curso não encontrado"
        )
    
    repo.delete_course(course_id)
    return None
