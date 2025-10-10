from sqlalchemy import Column, Integer, String, Text, DateTime
from sqlalchemy.sql import func
from app.database import Base


class Admin(Base):
    __tablename__ = "admins"
    
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(100), unique=True, index=True, nullable=False)
    hashed_password = Column(String(255), nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())


class QuietTimeEntry(Base):
    __tablename__ = "quiet_time_entries"
    
    id = Column(Integer, primary_key=True, index=True)
    song_title = Column(String(255), nullable=False)
    song_youtube_id = Column(String(100), nullable=False)
    scripture_reference = Column(String(255), nullable=False)
    scripture_text = Column(Text, nullable=False)
    prayer_title = Column(String(255), nullable=False)
    prayer_content = Column(Text, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())

