"""
Tests for the topics API endpoints.
"""
import uuid
from typing import Dict

import pytest
from fastapi.testclient import TestClient
from sqlalchemy.orm import Session

from app.main import app
from app.models.topic import Topic as TopicModel
from app.schemas.topic import TopicCreate, TopicUpdate

client = TestClient(app)

def test_create_topic(db: Session) -> None:
    """Test creating a new topic."""
    topic_data = {
        "name": "Test Topic",
        "description": "A test topic",
        "position": 1
    }
    response = client.post("/api/v1/topics/", json=topic_data)
    assert response.status_code == 201
    data = response.json()
    assert data["name"] == topic_data["name"]
    assert data["description"] == topic_data["description"]
    assert data["position"] == topic_data["position"]
    assert "id" in data
    assert "slug" in data
    assert "created_at" in data
    assert "updated_at" in data

def test_read_topic(db: Session, test_topic: Dict) -> None:
    """Test reading a topic by ID."""
    response = client.get(f"/api/v1/topics/{test_topic['id']}")
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == test_topic["id"]
    assert data["name"] == test_topic["name"]
    assert data["slug"] == test_topic["slug"]

def test_read_topic_not_found() -> None:
    """Test reading a non-existent topic."""
    non_existent_id = str(uuid.uuid4())
    response = client.get(f"/api/v1/topics/{non_existent_id}")
    assert response.status_code == 404

def test_list_topics(db: Session, test_topic: Dict) -> None:
    """Test listing topics."""
    response = client.get("/api/v1/topics/")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data["items"], list)
    assert len(data["items"]) > 0
    assert any(topic["id"] == test_topic["id"] for topic in data["items"])

def test_update_topic(db: Session, test_topic: Dict) -> None:
    """Test updating a topic."""
    update_data = {
        "name": "Updated Topic Name",
        "description": "Updated description"
    }
    response = client.put(
        f"/api/v1/topics/{test_topic['id']}",
        json=update_data
    )
    assert response.status_code == 200
    data = response.json()
    assert data["name"] == update_data["name"]
    assert data["description"] == update_data["description"]
    assert data["id"] == test_topic["id"]
    assert data["slug"] != test_topic["slug"]  # Slug should be updated

def test_delete_topic(db: Session, test_topic: Dict) -> None:
    """Test deleting a topic."""
    # First create a topic to delete
    topic_data = {
        "name": "Topic to Delete",
        "description": "Will be deleted"
    }
    create_response = client.post("/api/v1/topics/", json=topic_data)
    assert create_response.status_code == 201
    topic_id = create_response.json()["id"]
    
    # Now delete it
    delete_response = client.delete(f"/api/v1/topics/{topic_id}")
    assert delete_response.status_code == 204
    
    # Verify it's gone
    get_response = client.get(f"/api/v1/topics/{topic_id}")
    assert get_response.status_code == 404

def test_reorder_topics(db: Session, test_topics: list) -> None:
    """Test reordering topics."""
    # Get current order
    response = client.get("/api/v1/topics/")
    assert response.status_code == 200
    original_order = [t["id"] for t in response.json()["items"]]
    
    # Reverse the order
    new_order = list(reversed(original_order))
    
    # Reorder
    response = client.post("/api/v1/topics/reorder/", json=new_order)
    assert response.status_code == 200
    
    # Verify new order
    response = client.get("/api/v1/topics/")
    assert response.status_code == 200
    updated_order = [t["id"] for t in response.json()["items"]]
    assert updated_order == new_order
