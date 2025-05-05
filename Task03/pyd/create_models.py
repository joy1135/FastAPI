from datetime import datetime
from typing import List
from pydantic import BaseModel, Field

class CreateFilm(BaseModel):
    name: str = Field(..., max_length=255)
    year: int = Field(..., ge=1700, le=2025)
    duration: float = Field(..., ge=0.1, le=500)
    rating: int = Field(..., ge=0, le=10)
    description: str | None = Field(None, min_length=3,max_length=255)
    
    genre: List[int] = None
    
  

class CreateGenre(BaseModel):
    name: str = Field(..., min_length=3, max_length=255)
    description: str | None = Field(None,max_length=255)

class CreateUser(BaseModel):
    username: str = Field(..., max_length=60)
    passwrod: str = Field(..., max_length=255)
    email: str = Field(..., max_length=255)