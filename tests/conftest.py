"""
Test configuration and fixtures.
"""
import os
import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from app.db.database import Base, get_db
from app.main import app

# Use a test database URL from environment or fall back to SQLite in-memory
TEST_DATABASE_URL = os.getenv(
    "TEST_DATABASE_URL", 
    "sqlite:///:memory:"
)

# Create a test engine
engine = create_engine(
    TEST_DATABASE_URL,
    connect_args={"check_same_thread": False} if "sqlite" in TEST_DATABASE_URL else {},
    poolclass=StaticPool if "sqlite" in TEST_DATABASE_URL else None
)

# Create a test session
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Create tables
Base.metadata.create_all(bind=engine)

def override_get_db():
    """Override the get_db dependency for testing."""
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()

# Override the get_db dependency in the app
app.dependency_overrides[get_db] = override_get_db

@pytest.fixture(scope="session")
def db():
    """Database session fixture."""
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()

@pytest.fixture(scope="function")
def client():
    """Test client fixture."""
    with TestClient(app) as c:
        yield c

@pytest.fixture(scope="function")
def test_topic(db):
    """Create a test topic."""
    from app.models.topic import Topic
    from app.utils.slugify import slugify
    
    topic = Topic(
        name="Test Topic",
        slug=slugify("Test Topic"),
        description="A test topic",
        position=1
    )
    db.add(topic)
    db.commit()
    db.refresh(topic)
    
    # Convert to dict for easier use in tests
    return {
        "id": str(topic.id),
        "name": topic.name,
        "slug": topic.slug,
        "description": topic.description,
        "position": topic.position
    }

@pytest.fixture(scope="function")
def test_topics(db):
    """Create multiple test topics."""
    from app.models.topic import Topic
    from app.utils.slugify import slugify
    
    topics = []
    for i in range(5):
        topic = Topic(
            name=f"Test Topic {i+1}",
            slug=slugify(f"Test Topic {i+1}"),
            description=f"Test Topic {i+1} Description",
            position=i+1
        )
        db.add(topic)
        topics.append(topic)
    
    db.commit()
    
    # Return topic data as dicts
    return [
        {
            "id": str(topic.id),
            "name": topic.name,
            "slug": topic.slug,
            "description": topic.description,
            "position": topic.position
        }
        for topic in topics
    ]
