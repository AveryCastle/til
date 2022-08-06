from sqlalchemy import Column, DateTime, Integer, String
from sqlalchemy.sql import func

from .database import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    sns_id = Column(String, unique=True, index=True)
    email = Column(String, unique=True)
    name = Column(String)
    access_token = Column(String)
    refresh_token = Column(String)
    last_login_at = Column(DateTime(timezone=True), default=func.now())
    created_at = Column(DateTime(timezone=True), default=func.now())
