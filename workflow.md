# Promps I used

## Prompt to generate a list of post topics
Review the workflow.md file High Level steps section and make suggestions for creating an agentic workflow. 
Use supabase as the database and langchain to create the agent.
# Prompt Topic and Post Management Workflow

## High level steps
1. Allow a user to create and edit a list of post topics
2. The list should be stored in a permanent location (e.g. a database or a file)
~~3. Allow a user to select a post topic from the list~~
4. User can generate posts for unused topics
5. The post should be generated according to a template
    1. The template will be a markdown file for Hugo with front matter
    2. The front matter will be in the same format as the template
5. After the post generates, the agent should review it and make any necessary edits
6. After review, the agent should generate a prompt for an image based on the post content
7. Then use the image prompt to generate an image of a specific size (e.g. 1024x1024) and format (e.g. jpg)
8. The post should be saved to a permanent location (e.g. a database or a file)
9. The image should be saved to a permanent location (e.g. a database or a file)
10. The image prompt should be saved to a permanent location (e.g. a database or a file)
    1. The image and image prompt should be saved in the same folder as the post
    2. Or have a relationship to the post
11. A list of Draft posts should be displayed
    1. The list could be a query of all posts in Draft status
12. A list of Published posts should be displayed
    1. The list could be a query of all posts in Published status 
13. The user can review a Draft post
    1. The user can edit or regenerate the post
    2. Old versions of the post should be stored along with the current version
14. On the same page as the Draft post review, the user should be able to see the image and image prompt for the post
    1. The user should be able to edit the image and image prompt
    2. The user should be able to regenerate the image
    3. Multiple versions of images should be visible for the user to choose from
    4. Old versions of the image and image prompt should be stored along with the current version   
15. The user can publish a Draft post
    1. The Post and Image are put into a folder following the Hugo folder structure
    2. a git commit is made and pushed
    3. The post should be moved to Published status



## Database Schema

### Tables

#### Topics
Stores all post topics and their metadata.

```sql
create table topics (
  id uuid primary key default uuid_generate_v4(),
  title text not null,
  created_at timestamp with time zone default timezone('utc'::text, now()) not null,
  updated_at timestamp with time zone default timezone('utc'::text, now()) not null,
  position integer not null default 0,
  is_used boolean default false
);
```

#### Posts
Contains the main post content and metadata.

```sql
create table posts (
  id uuid primary key default uuid_generate_v4(),
  topic_id uuid references topics(id),
  title text not null,
  content text not null,
  status text check (status in ('draft', 'published', 'archived')) default 'draft',
  created_at timestamp with time zone default timezone('utc'::text, now()) not null,
  updated_at timestamp with time zone default timezone('utc'::text, now()) not null
);
```

#### Post Versions
Tracks historical versions of posts for audit and rollback.

```sql
create table post_versions (
  id uuid primary key default uuid_generate_v4(),
  post_id uuid references posts(id) on delete cascade,
  content text not null,
  created_at timestamp with time zone default timezone('utc'::text, now()) not null
);
```

#### Images
Manages generated images and their associated metadata.

```sql
create table images (
  id uuid primary key default uuid_generate_v4(),
  post_id uuid references posts(id) on delete cascade,
  prompt text not null,
  image_url text not null,
  is_selected boolean default false,
  created_at timestamp with time zone default timezone('utc'::text, now()) not null
);
```

### Relationships
- One-to-many: One topic can have many posts
- One-to-many: One post can have many versions
- One-to-many: One post can have many images (with one selected as active)

### Indexes
```sql
create index idx_posts_topic_id on posts(topic_id);
create index idx_post_versions_post_id on post_versions(post_id);
create index idx_images_post_id on images(post_id);
create index idx_posts_status on posts(status);
create index idx_topics_is_used on topics(is_used);
```

### Storage
- Post content and metadata stored in PostgreSQL tables
- Image files stored in object storage (e.g., Supabase Storage)
- Image metadata and URLs stored in the database

### Security
- Row-level security (RLS) policies for all tables
- Service role for backend operations
- Authenticated user role for frontend operations

### Detailed prompt topic management steps
1. Allow a user to create and edit a list of post topics
    2. The list should be stored in a permanent location (e.g. a database or a file)
    3. Allow a user to edit a post topic
    4. Allow a user to delete a post topic
    5. Allow a user to move a post topic to the top of the list
    6. Allow a user to move a post topic to the bottom of the list
    7. Allow a user to move a post topic up one position in the list
    9. Allow a user to move a post topic down one position in the list
2. A UI needs to be created to allow the user to do this
