from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime
from app.models import Patron,PatronDrink


class ListPatrons(BaseModel):
    page: int=0
    per_page: int=25


class PostPatron(BaseModel):
    name: str
    email: str
    phone: str
    weight: float
    gender: str
    birthdate: datetime

class PatronResponse(BaseModel):
    data: Optional[list[Patron|PatronDrink]]
    total: Optional[int]
    current_page: Optional[int]
    total_pages: Optional[int]
    results_per_page: Optional[int]
