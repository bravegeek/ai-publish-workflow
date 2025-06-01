"""
Pydantic models for Topic data validation and serialization.
"""
from datetime import datetime
from typing import List, Optional
from pydantic import BaseModel, Field, validator


class TopicBase(BaseModel):
    """Base schema for Topic with common attributes."""
    name: str = Field(..., min_length=1, max_length=100, description="Name of the topic")
    description: Optional[str] = Field(
        None, max_length=500, description="Optional description of the topic"
    )
    position: int = Field(
        default=0, ge=0, description="Position for ordering topics"
    )


class TopicCreate(TopicBase):
    """Schema for creating a new topic."""
    pass


class TopicUpdate(BaseModel):
    """Schema for updating an existing topic."""
    name: Optional[str] = Field(
        None, min_length=1, max_length=100, description="Updated name of the topic"
    )
    description: Optional[str] = Field(
        None, max_length=500, description="Updated description of the topic"
    )
    position: Optional[int] = Field(
        None, ge=0, description="Updated position for ordering"
    )


class TopicInDBBase(TopicBase):
    """Base schema for Topic in database."""
    id: str
    slug: str
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True


class Topic(TopicInDBBase):
    """Schema for returning Topic data."""
    pass


class TopicList(BaseModel):
    """Schema for returning a list of topics."""
    items: List[Topic]
    total: int
