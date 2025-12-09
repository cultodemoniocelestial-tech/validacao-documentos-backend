from pydantic import BaseModel, Field
from typing import Optional, List


class CourseBase(BaseModel):
    """Schema base para curso"""
    name: str = Field(..., min_length=1, max_length=255)
    code: str = Field(..., min_length=1, max_length=50)
    description: Optional[str] = None
    minimum_months: int = Field(default=12, ge=1)
    accepted_positions: List[str] = Field(default_factory=list)
    is_active: bool = True


class CourseCreate(CourseBase):
    """Schema para criação de curso"""
    pass


class CourseUpdate(BaseModel):
    """Schema para atualização de curso"""
    name: Optional[str] = Field(None, min_length=1, max_length=255)
    code: Optional[str] = Field(None, min_length=1, max_length=50)
    description: Optional[str] = None
    minimum_months: Optional[int] = Field(None, ge=1)
    accepted_positions: Optional[List[str]] = None
    is_active: Optional[bool] = None


class CourseResponse(CourseBase):
    """Schema de resposta de curso"""
    id: int
    
    class Config:
        from_attributes = True


class CourseListResponse(BaseModel):
    """Schema de resposta de lista de cursos"""
    courses: List[CourseResponse]
    total: int
