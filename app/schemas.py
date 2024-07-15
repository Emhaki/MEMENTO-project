from pydantic import BaseModel
from typing import Optional
import datetime

class URLExpire(BaseModel):
    expires_at: Optional[datetime.datetime] = None

class URLResponse(BaseModel):
    short_url: str

class URL(BaseModel):
    id: int
    short_url: str
    created_at: datetime.datetime
    expires_at: Optional[datetime.datetime] = None
    visit_count: int

    class Config:
        from_attributes = True

