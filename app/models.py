from sqlalchemy import Column, Integer, String, DateTime
from .database import declarative_base
import datetime
from app.database import Base

class URL(Base):
    __tablename__ = "urls"
    
    id = Column(Integer, primary_key=True, index=True)
    original_url = Column(String(255), index=True)
    short_url = Column(String(255), unique=True, index=True)
    visit_count = Column(Integer, default=0)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)
    expires_at = Column(DateTime, default=(datetime.datetime.utcnow() + datetime.timedelta(minutes=5)))
    