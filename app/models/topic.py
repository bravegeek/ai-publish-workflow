"""
SQLAlchemy model for the Topic entity.
"""
import uuid
from datetime import datetime
from typing import Optional

from sqlalchemy import Column, DateTime, Integer, String, Text, func
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import declarative_base

from app.db.database import Base

class Topic(Base):
    """
    SQLAlchemy model representing a topic in the blog.
    """
    __tablename__ = "topics"

    id = Column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
        unique=True,
        nullable=False,
    )
    name = Column(String(100), nullable=False, index=True)
    slug = Column(String(100), unique=True, nullable=False, index=True)
    description = Column(Text, nullable=True)
    position = Column(Integer, default=0, nullable=False)
    created_at = Column(
        DateTime(timezone=True), server_default=func.now(), nullable=False
    )
    updated_at = Column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now(),
        nullable=False,
    )

    def __repr__(self) -> str:
        return f"<Topic(id={self.id}, name='{self.name}', slug='{self.slug}')>"

    def to_dict(self) -> dict:
        """
        Convert the Topic instance to a dictionary.
        
        Returns:
            dict: Dictionary representation of the Topic
        """
        return {
            "id": str(self.id),
            "name": self.name,
            "slug": self.slug,
            "description": self.description,
            "position": self.position,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "updated_at": self.updated_at.isoformat() if self.updated_at else None,
        }
