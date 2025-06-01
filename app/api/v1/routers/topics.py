"""
API endpoints for managing blog topics.
"""
from typing import List, Optional

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session

from app import crud, models, schemas
from app.db.database import get_db
from app.utils.slugify import unique_slug

router = APIRouter()

@router.get("/", response_model=schemas.TopicList, summary="List all topics")
def read_topics(
    skip: int = Query(0, ge=0, description="Number of records to skip"),
    limit: int = Query(100, le=1000, description="Maximum number of records to return"),
    order_by: str = Query("position", description="Field to order by"),
    order: str = Query("asc", description="Sort order ('asc' or 'desc')"),
    db: Session = Depends(get_db)
):
    """
    Retrieve a list of topics with pagination and ordering.
    """
    if order.lower() not in ("asc", "desc"):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Order must be either 'asc' or 'desc'"
        )
    
    topics = crud.topic.get_topics(
        db, skip=skip, limit=limit, order_by=order_by, order=order
    )
    total = db.query(models.topic.Topic).count()
    
    return {"items": topics, "total": total}

@router.post(
    "/", 
    response_model=schemas.Topic, 
    status_code=status.HTTP_201_CREATED,
    summary="Create a new topic"
)
def create_topic(
    topic: schemas.TopicCreate,
    db: Session = Depends(get_db)
):
    """
    Create a new topic.
    """
    # Check if topic with the same name already exists
    db_topic = crud.topic.get_topic_by_slug(db, slug=unique_slug(db, models.topic.Topic, topic.name))
    if db_topic:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="A topic with this name already exists"
        )
    
    return crud.topic.create_topic(db=db, topic=topic)

@router.get(
    "/{topic_id}", 
    response_model=schemas.Topic,
    summary="Get a topic by ID"
)
def read_topic(
    topic_id: str,
    db: Session = Depends(get_db)
):
    """
    Get a specific topic by its ID.
    """
    db_topic = crud.topic.get_topic(db, topic_id=topic_id)
    if db_topic is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Topic not found"
        )
    return db_topic

@router.put(
    "/{topic_id}", 
    response_model=schemas.Topic,
    summary="Update a topic"
)
def update_topic(
    topic_id: str,
    topic_update: schemas.TopicUpdate,
    db: Session = Depends(get_db)
):
    """
    Update a topic.
    """
    db_topic = crud.topic.get_topic(db, topic_id=topic_id)
    if db_topic is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Topic not found"
        )
    
    # If name is being updated, check if the new name is already taken
    if topic_update.name and topic_update.name != db_topic.name:
        new_slug = unique_slug(db, models.topic.Topic, topic_update.name)
        existing_topic = crud.topic.get_topic_by_slug(db, slug=new_slug)
        if existing_topic and existing_topic.id != db_topic.id:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="A topic with this name already exists"
            )
    
    return crud.topic.update_topic(db=db, db_topic=db_topic, topic_update=topic_update)

@router.delete(
    "/{topic_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Delete a topic"
)
def delete_topic(
    topic_id: str,
    db: Session = Depends(get_db)
):
    """
    Delete a topic.
    """
    db_topic = crud.topic.get_topic(db, topic_id=topic_id)
    if db_topic is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Topic not found"
        )
    
    # Check if the topic has any associated posts
    post_count = db.query(models.post.Post).filter(models.post.Post.topic_id == topic_id).count()
    if post_count > 0:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Cannot delete a topic that has associated posts"
        )
    
    crud.topic.delete_topic(db, topic_id=topic_id)
    return None

@router.post(
    "/reorder/",
    status_code=status.HTTP_200_OK,
    summary="Reorder topics"
)
def reorder_topics(
    topic_ids: List[str],
    db: Session = Depends(get_db)
):
    """
    Reorder topics based on the provided list of topic IDs.
    """
    if not topic_ids:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="No topic IDs provided"
        )
    
    # Verify all topic IDs exist
    for topic_id in topic_ids:
        if not crud.topic.get_topic(db, topic_id=topic_id):
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Topic with ID {topic_id} not found"
            )
    
    success = crud.topic.reorder_topics(db, topic_ids=topic_ids)
    if not success:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to reorder topics"
        )
    
    return {"message": "Topics reordered successfully"}
