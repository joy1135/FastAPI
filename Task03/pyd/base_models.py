from datetime import datetime
from typing import Optional
from pydantic import BaseModel, Field

class BaseFilm(BaseModel):
    id: int = Field(example=1)
    name: str = Field(example="Star Wars")
    year: int = Field(example=1999)
    duration: float = Field(example=120)
    rating: int = Field(example=10, ge=0, le=10)
    description: Optional[str] = None
    img: Optional[str] = None
    date_added: datetime = Field(example=datetime.now())
  

class BaseGenre(BaseModel):
    id: int = Field(None, gt=0, example=1)
    name: str = Field(max_length=255, example='Фантастика')
    description: Optional[str] = None
    