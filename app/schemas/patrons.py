from pydantic import BaseModel, Field
from typing import Optional

class ListPatrons(BaseModel):
    page: int
    per_page: int