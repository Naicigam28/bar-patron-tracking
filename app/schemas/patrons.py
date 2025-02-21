from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime
from app.models import Patron


class ListPatrons(BaseModel):
    page: int
    per_page: int


class PostPatron(BaseModel):
    name: str
    email: str
    phone: str
    weight: float
    gender: str
    birthdate: str

class PatronResponse(BaseModel):
    data: Optional[list[Patron]]
    total: Optional[int]
    current_page: Optional[int]
    total_pages: Optional[int]
    results_per_page: Optional[int]
