# Task List for AI-Powered Blog Publishing System

## Database Setup
- [x] Create Supabase project
- [x] Initialize database schema
  - [x] Create `topics` table
  - [x] Create `posts` table
  - [x] Create `post_versions` table
  - [x] Create `images` table
- [x] Set up Row Level Security (RLS) policies
- [x] Create necessary indexes

## API Endpoints
- [x] Topics API
  - [x] GET /api/v1/topics/ - List all topics
  - [x] POST /api/v1/topics/ - Create new topic
  - [x] PUT /api/v1/topics/{topic_id} - Update topic
  - [x] DELETE /api/v1/topics/{topic_id} - Delete topic
  - [x] POST /api/v1/topics/reorder/ - Reorder topics

- [ ] Posts API
  - [ ] GET /api/posts - List posts (with filters)
  - [ ] POST /api/posts - Create new post
  - [ ] GET /api/posts/:id - Get post details
  - [ ] PUT /api/posts/:id - Update post
  - [ ] POST /api/posts/:id/generate - Generate AI content
  - [ ] POST /api/posts/:id/publish - Publish post

- [ ] Images API
  - [ ] POST /api/images/generate - Generate image from prompt
  - [ ] GET /api/images/:postId - Get images for post
  - [ ] POST /api/images/select - Select image for post

## Frontend Components
- [ ] Layout
  - [ ] Main layout with navigation
  - [ ] Sidebar for topic list
  - [ ] Content area

- [ ] Topic Management
  - [ ] Topic list view
  - [ ] Add/Edit topic modal
  - [ ] Topic reordering controls

- [ ] Post Management
  - [ ] Post list view (drafts/published)
  - [ ] Post editor
  - [ ] Post preview
  - [ ] Version history viewer

- [ ] Image Generation
  - [ ] Image prompt editor
  - [ ] Image gallery
  - [ ] Image selection interface

## AI Integration
- [ ] Set up LangChain
- [ ] Implement prompt templates
- [ ] Create content generation logic
- [ ] Implement content review and editing
- [ ] Create image prompt generation
- [ ] Integrate with image generation API

## Publishing Workflow
- [ ] Implement draft state management
- [ ] Create publishing pipeline
- [ ] Set up Hugo export functionality
- [ ] Implement git integration
  - [ ] Commit changes
  - [ ] Push to repository

## Testing
- [ ] Unit tests for API endpoints
- [ ] Integration tests for workflows
- [ ] UI component tests
- [ ] End-to-end tests

## Deployment
- [ ] Set up CI/CD pipeline
- [ ] Configure production environment
- [ ] Set up monitoring and logging

## Documentation
- [ ] API documentation
- [ ] User guide
- [ ] Development setup guide
