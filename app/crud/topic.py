"""
CRUD operations for Topic model.
"""
import uuid
from typing import List, Optional

from sqlalchemy.orm import Session

from app.models.topic import Topic as TopicModel
from app.schemas.topic import TopicCreate, TopicUpdate

def get_topic(db: Session, topic_id: str) -> Optional[TopicModel]:
    """
    Get a single topic by ID.
    
    Args:
        db: Database session
        topic_id: ID of the topic to retrieve
        
    Returns:
        TopicModel if found, None otherwise
    """
    try:
        topic_uuid = uuid.UUID(topic_id)
        return db.query(TopicModel).filter(TopicModel.id == topic_uuid).first()
    except (ValueError, AttributeError):
        return None

def get_topic_by_slug(db: Session, slug: str) -> Optional[TopicModel]:
    """
    Get a single topic by slug.
    
    Args:
        db: Database session
        slug: Slug of the topic to retrieve
        
    Returns:
        TopicModel if found, None otherwise
    """
    return db.query(TopicModel).filter(TopicModel.slug == slug).first()

def get_topics(
    db: Session, 
    skip: int = 0, 
    limit: int = 100,
    order_by: str = "position",
    order: str = "asc"
) -> List[TopicModel]:
    """
    Get a list of topics with pagination and ordering.
    
    Args:
        db: Database session
        skip: Number of records to skip (for pagination)
        limit: Maximum number of records to return
        order_by: Field to order by (default: position)
        order: Sort order ('asc' or 'desc')
        
    Returns:
        List of TopicModel instances
    """
    query = db.query(TopicModel)
    
    # Apply ordering
    order_field = getattr(TopicModel, order_by, TopicModel.position)
    if order.lower() == "desc":
        query = query.order_by(order_field.desc())
    else:
        query = query.order_by(order_field.asc())
    
    return query.offset(skip).limit(limit).all()

def create_topic(db: Session, topic: TopicCreate) -> TopicModel:
    """
    Create a new topic.
    
    Args:
        db: Database session
        topic: Topic data to create
        
    Returns:
        Created TopicModel instance
    """
    # In a real app, you might want to generate a slug from the name
    # For now, we'll use a simple slugify function
    from app.utils.slugify import slugify
    
    db_topic = TopicModel(
        name=topic.name,
        slug=slugify(topic.name),
        description=topic.description,
        position=topic.position
    )
    
    db.add(db_topic)
    db.commit()
    db.refresh(db_topic)
    return db_topic

def update_topic(
    db: Session, 
    db_topic: TopicModel, 
    topic_update: TopicUpdate
) -> TopicModel:
    """
    Update an existing topic.
    
    Args:
        db: Database session
        db_topic: Topic to update
        topic_update: Updated topic data
        
    Returns:
        Updated TopicModel instance
    """
    update_data = topic_update.dict(exclude_unset=True)
    
    for field, value in update_data.items():
        setattr(db_topic, field, value)
    
    db.add(db_topic)
    db.commit()
    db.refresh(db_topic)
    return db_topic

def delete_topic(db: Session, topic_id: str) -> bool:
    """
    Delete a topic.
    
    Args:
        db: Database session
        topic_id: ID of the topic to delete
        
    Returns:
        bool: True if the topic was deleted, False otherwise
    """
    try:
        topic_uuid = uuid.UUID(topic_id)
        db_topic = db.query(TopicModel).filter(TopicModel.id == topic_uuid).first()
        if not db_topic:
            return False
            
        db.delete(db_topic)
        db.commit()
        return True
    except (ValueError, AttributeError):
        return False

def reorder_topics(db: Session, topic_ids: List[str]) -> bool:
    """
    Reorder topics based on the provided list of IDs.
    
    Args:
        db: Database session
        topic_ids: List of topic IDs in the new order
        
    Returns:
        bool: True if reordering was successful, False otherwise
    """
    try:
        # Start a transaction
        db.begin()
        
        # Update position for each topic
        for position, topic_id in enumerate(topic_ids, 1):
            db.query(TopicModel).filter(TopicModel.id == uuid.UUID(topic_id))\
                .update({"position": position})
        
        db.commit()
        return True
    except Exception:
        db.rollback()
        return False
