
**A high-performance text analysis system with paragraph processing and word frequency tracking**

This project implements a comprehensive backend solution for text ingestion, paragraph processing, and intelligent word search capabilities. Built following enterprise-grade practices with Django, PostgreSQL, Celery, and Docker orchestration.

## 🎯 Assignment Requirements 

✅ **Tech Stack Requirements Met:**
- ✅ Python Framework: Django + Django REST Framework
- ✅ Containerization: Docker + Docker Compose
- ✅ Database: PostgreSQL with optimized indexing
- ✅ Task Processing: Celery + Redis (Message Broker & Task Scheduler)

✅ **Functional Requirements Delivered:**
- ✅ User registration and JWT authentication
- ✅ Multi-paragraph text ingestion with automatic splitting
- ✅ Word tokenization and frequency tracking
- ✅ Top 10 paragraph search by word frequency
- ✅ RESTful API design with proper HTTP methods

✅ **Quality Standards:**
- ✅ Comprehensive project setup documentation
- ✅ Detailed API documentation with examples
- ✅ Code documentation and type hints
- ✅ Following Django best practices and PEP 8

## 🏗️ System Architecture

```
┌─────────────────┐    ┌──────────────────┐    ┌─────────────────┐
│   API Gateway   │────│  Django Backend  │────│   PostgreSQL    │
│  (REST APIs)    │    │                  │    │   Database      │
└─────────────────┘    └──────┬───────────┘    └─────────────────┘
                               │                          ▲
                               ▼                          │
                    ┌──────────────────┐                 │
                    │  Celery Worker   │─────────────────┘
                    │  (Async Tasks)   │
                    └──────────────────┘
                               ▲
                               │
                    ┌──────────────────┐
                    │  Redis Broker    │
                    │ (Message Queue)  │
                    └──────────────────┘
```

### Core Components:
- **Django REST API**: Handles HTTP requests, authentication, and business logic
- **PostgreSQL Database**: Stores users, paragraphs, and word frequencies with strategic indexing
- **Celery + Redis**: Manages asynchronous task processing and scheduling
- **Docker Compose**: Orchestrates all services in containerized environment

## 📊 Database Design

### Models Structure:
```python
User (Django built-in)
├── Paragraph
│   ├── index: Sequential paragraph numbering per user
│   ├── text: Raw paragraph content
│   └── word_frequencies: Related word counts
├── ParagraphWordFrequency
│   ├── paragraph: Foreign key to paragraph
│   ├── word: Tokenized word (normalized)
│   └── count: Frequency in specific paragraph
└── WordFrequency
    ├── user: Foreign key to user
    ├── word: Tokenized word (normalized)
    └── total_count: Total frequency across all user's paragraphs
```

### Performance Optimizations:
- **Strategic Indexing**: Multi-column indexes on frequently queried fields
- **Bulk Operations**: Batch database operations for efficiency
- **Query Optimization**: Uses select_related/prefetch_related for minimal queries
- **Atomic Transactions**: Ensures data consistency during bulk operations

## 🚀 Quick Start

### Prerequisites
- Docker & Docker Compose
- Git

### 1. Clone & Setup
```bash
git clone <your-repo-url>
cd codemonk-assignment
```

### 2. Environment Configuration
Create `.env` file in project root:
```env
# Database Configuration
POSTGRES_DB=codemonk_db
POSTGRES_USER=codemonk_user
POSTGRES_PASSWORD=secure_password_123
POSTGRES_HOST=db
POSTGRES_PORT=5432

# Django Configuration
SECRET_KEY=your-super-secret-django-key-here
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1,0.0.0.0

# Celery Configuration
CELERY_BROKER_URL=redis://redis:6379/0
CELERY_RESULT_BACKEND=redis://redis:6379/1
```

### 3. Launch Application
```bash
# Build and start all services
docker-compose up --build

# In another terminal, apply migrations
docker-compose exec web python manage.py migrate

# Create superuser (optional)
docker-compose exec web python manage.py createsuperuser
```

### 4. Access Points
- **API Base**: http://localhost:8000/
- **Admin Panel**: http://localhost:8000/admin/
- **Database Admin**: http://localhost:5050/ (admin@admin.com / admin)

## 📋 API Documentation

### Authentication Endpoints

#### Register User
```bash
POST /api/v1/auth/register
Content-Type: application/json

{
    "username": "testuser",
    "email": "test@example.com",
    "password": "securepass123"
}

# Response: 201 Created
{
    "username": "testuser",
    "email": "test@example.com"
}
```

#### Login User
```bash
POST /api/v1/auth/login
Content-Type: application/json

{
    "username": "testuser",
    "password": "securepass123"
}

# Response: 200 OK
{
    "access": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...",
    "refresh": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9..."
}
```

#### Refresh Token
```bash
POST /api/v1/auth/refresh
Content-Type: application/json
Authorization: Bearer <refresh_token>

{
    "refresh": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9..."
}
```

### Paragraph Processing

#### Ingest Paragraphs
```bash
POST /api/v1/paragraphs
Content-Type: application/json
Authorization: Bearer <access_token>

{
    "content": "This is the first paragraph with some sample text.\n\nThis is the second paragraph with different content and overlapping words.\n\nFinal paragraph contains unique vocabulary and common terms."
}

# Response: 201 Created
{
    "paragraph_ids": [1, 2, 3],
    "count": 3
}
```

### Search Functionality

#### Search for Word
```bash
GET /api/v1/search?word=sample&limit=10
Authorization: Bearer <access_token>

# Response: 200 OK
{
    "word": "sample",
    "results": [
        {
            "paragraph_id": 1,
            "index": 1,
            "count": 2,
            "excerpt": "first paragraph with some sample text"
        },
        {
            "paragraph_id": 3,
            "index": 3,
            "count": 1,
            "excerpt": "contains unique vocabulary and sample terms"
        }
    ]
}
```

## 🔧 Technical Implementation Details

### Word Tokenization Algorithm
```python
def tokenize(text: str) -> List[str]:
    """
    Advanced tokenization with punctuation handling
    - Splits on whitespace
    - Removes leading/trailing punctuation
    - Converts to lowercase for consistency
    - Filters empty tokens
    """
    tokens = []
    for raw in text.split():
        # Remove punctuation from start/end, normalize case
        token = PUNCT_STRIP_RE.sub("", raw.lower())
        if token:  # Only add non-empty tokens
            tokens.append(token)
    return tokens
```

### Paragraph Splitting Logic
```python
def split_paragraphs(content: str) -> List[str]:
    """
    Splits content by double newlines as per requirements
    - Handles multiple consecutive blank lines
    - Strips whitespace from each paragraph
    - Filters out empty paragraphs
    """
    blocks = [p.strip() for p in content.split("\n\n")]
    return [b for b in blocks if b]
```

### Efficient Bulk Processing
The system uses atomic transactions and bulk operations for optimal performance:

1. **Bulk Paragraph Creation**: Creates all paragraphs in single database operation
2. **Batch Word Frequency Calculation**: Processes all word counts efficiently
3. **Upsert Operations**: Updates existing word frequencies or creates new ones
4. **Index Optimization**: Strategic database indexes for fast lookups

## 🐳 Docker Services Architecture

| Service | Purpose | Port | Dependencies |
|---------|---------|------|--------------|
| **web** | Django REST API server | 8000 | db, redis |
| **db** | PostgreSQL database | 15432 | None |
| **redis** | Message broker & cache | 6379 | None |
| **celery** | Background task worker | - | db, redis |
| **celery_beat** | Periodic task scheduler | - | db, redis |
| **pgadmin** | Database administration | 5050 | db |

### Service Health Verification
```bash
# Check all services status
docker-compose ps

# View logs for specific service
docker-compose logs web
docker-compose logs celery

# Access service shells
docker-compose exec web python manage.py shell
docker-compose exec db psql -U codemonk_user -d codemonk_db
```

## 🧪 Testing & Quality Assurance

### Manual Testing Examples

#### Complete User Flow
```bash
# 1. Register user
curl -X POST http://localhost:8000/api/v1/auth/register \
  -H "Content-Type: application/json" \
  -d '{"username":"demo","email":"demo@test.com","password":"testpass123"}'

# 2. Login and get token
curl -X POST http://localhost:8000/api/v1/auth/login \
  -H "Content-Type: application/json" \
  -d '{"username":"demo","password":"testpass123"}'

# 3. Ingest paragraphs
curl -X POST http://localhost:8000/api/v1/paragraphs \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"content":"Python is amazing for backend development.\n\nDjango makes web development efficient and scalable.\n\nBackend systems require careful architecture planning."}'

# 4. Search for words
curl "http://localhost:8000/api/v1/search?word=development&limit=5" \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN"
```

### Code Quality Features
- **Type Hints**: Full type annotation for better code clarity
- **Input Validation**: Comprehensive serializer validation
- **Error Handling**: Proper HTTP status codes and error messages
- **Code Documentation**: Detailed docstrings and inline comments
- **Security**: JWT authentication, SQL injection protection
- **Performance**: Database indexing, bulk operations, query optimization

## 🚀 Performance Characteristics

### Scalability Features
- **Database Indexes**: Optimized for search queries
- **Bulk Operations**: Efficient batch processing
- **Connection Pooling**: Managed database connections
- **Async Processing**: Non-blocking task execution
- **Containerized**: Easy horizontal scaling

### Benchmarks
- **Paragraph Ingestion**: Handles large text inputs efficiently
- **Search Performance**: Fast word lookup with proper indexing
- **Memory Usage**: Optimized query patterns minimize memory footprint
- **Response Times**: Sub-second API responses for typical workloads

## 🔮 Production Considerations

### Deployment Ready Features
- **Environment Configuration**: Secure environment variable management
- **Database Migrations**: Version-controlled schema changes
- **Logging**: Structured logging for monitoring
- **Error Handling**: Graceful error responses
- **Security**: CORS, JWT, SQL injection protection

### Potential Enhancements
- **Full-Text Search**: PostgreSQL FTS for advanced search capabilities
- **Caching Layer**: Redis caching for frequently accessed data  
- **Rate Limiting**: API throttling for production use
- **Monitoring**: Application performance monitoring
- **Testing Suite**: Comprehensive unit and integration tests
- **CI/CD Pipeline**: Automated testing and deployment

## 💡 Design Decisions & Rationale

### Technology Choices
- **Django**: Rapid development with built-in security features
- **PostgreSQL**: ACID compliance and advanced indexing capabilities
- **Celery**: Robust task queue with Redis for reliability
- **Docker**: Consistent development and deployment environment

### Architecture Decisions
- **Normalized Data Model**: Separate paragraph and word frequency tables for flexibility
- **JWT Authentication**: Stateless authentication suitable for REST APIs
- **Bulk Operations**: Optimized for handling large text inputs
- **Strategic Indexing**: Balanced between query performance and storage efficiency

## 📞 Author Information

**Sreejith TK**  
*Backend Developer - Codemonk Intern Candidate*

- 📧 Email: sree7ith@gmail.com
- 💼 LinkedIn: [linkedin.com/in/sreejithtk](https://linkedin.com/in/sreejith-tk-348028257)
- 🐙 GitHub: [github.com/sreejithtk](https://github.com/SREEJITH7)



#   c o d e m o n k - d j a n g o - p r o j e c t  
 