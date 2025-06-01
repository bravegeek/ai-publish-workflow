# AI Publish Workflow

A FastAPI-based backend for managing AI-powered blog publishing workflows, featuring topic management, post creation, and content generation.

## Features

- **Topics Management**: Create, read, update, and delete blog topics
- **RESTful API**: Follows REST principles with proper HTTP methods and status codes
- **Database Integration**: Built with SQLAlchemy ORM and PostgreSQL
- **Testing**: Comprehensive test suite with pytest
- **Documentation**: Auto-generated API documentation with Swagger UI and ReDoc

## Tech Stack

- Python 3.9+
- FastAPI
- SQLAlchemy
- PostgreSQL
- Pydantic
- Pytest

## Getting Started

### Prerequisites

- Python 3.9 or higher
- PostgreSQL 13 or higher
- pip (Python package installer)

### Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/yourusername/ai-publish-workflow.git
   cd ai-publish-workflow
   ```

2. **Create a virtual environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: .\venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Set up environment variables**
   Create a `.env` file in the root directory with the following variables:
   ```env
   DATABASE_URL=postgresql://username:password@localhost:5432/ai_publish_workflow
   ```

5. **Initialize the database**
   ```bash
   # Apply migrations
   # (You'll need to set up your database first)
   # TODO: Add migration commands once Alembic is set up
   ```

## Running the Application

### Development Server

```bash
uvicorn app.main:app --reload
```

The API will be available at `http://localhost:8000`

### API Documentation

- **Swagger UI**: http://localhost:8000/api/docs
- **ReDoc**: http://localhost:8000/api/redoc

## API Endpoints

### Topics

- `GET /api/v1/topics/` - List all topics
- `POST /api/v1/topics/` - Create a new topic
- `GET /api/v1/topics/{topic_id}` - Get a specific topic
- `PUT /api/v1/topics/{topic_id}` - Update a topic
- `DELETE /api/v1/topics/{topic_id}` - Delete a topic
- `POST /api/v1/topics/reorder/` - Reorder topics

## Testing

Run the test suite with pytest:

```bash
pytest
```

## Project Structure

```
ai-publish-workflow/
├── app/                           # Application package
│   ├── api/                       # API routes
│   │   └── v1/                    # API version 1
│   │       └── routers/           # API route handlers
│   ├── crud/                      # Database CRUD operations
│   ├── db/                        # Database configuration
│   ├── models/                    # SQLAlchemy models
│   ├── schemas/                   # Pydantic models/schemas
│   └── utils/                     # Utility functions
├── tests/                         # Test files
│   └── api/                       # API tests
│       └── v1/                    # API v1 tests
├── .env.example                   # Example environment variables
├── requirements.txt               # Project dependencies
└── README.md                     # This file
```

## Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
