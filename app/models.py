from sqlalchemy import Column, Integer, String, Date, func
from app.database import Base
from pydantic import BaseModel

class URLRequest(BaseModel):
    long_url: str

class URL(Base):
    __tablename__ = "urls"

    id = Column(Integer, primary_key=True, index=True)
    long_url = Column(String(2048))
    short_url = Column(String(255))
    hit_count = Column(Integer, default=0)
    last_hit_date = Column(Date, default=func.current_date())
