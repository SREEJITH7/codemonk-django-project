# Text Analytics API - Codemonk Internship Portfolio Project

> A comprehensive backend system demonstrating advanced Django development skills for **Codemonk** internship application.

This project showcases a full-featured text analysis platform built with Django, PostgreSQL, Celery, and Docker. It demonstrates proficiency in REST API development, asynchronous processing, database optimization, and containerized deployment - key skills valuable for backend development at Codemonk.

##  Project Overview

**Text Analytics API** is a robust backend system that ingests textual content, intelligently processes paragraphs, computes word frequencies, and provides powerful search capabilities. This project highlights my expertise in:

- **Python Django Development** - Clean, scalable REST API architecture
- **Database Design** - Optimized PostgreSQL schemas with strategic indexing
- **Asynchronous Processing** - Celery-based background task handling
- **Containerization** - Docker-first deployment strategy
- **Performance Optimization** - Efficient search algorithms and caching

##  Table of Contents

- [Features](#-features)
- [Tech Stack](#-tech-stack)
- [System Architecture](#-system-architecture)
- [Quick Start](#-quick-start)
- [API Documentation](#-api-documentation)
- [Docker Deployment](#-docker-deployment)
- [Future Enhancements](#-future-enhancements)
- [Contact](#-contact)

##  Features

### Core Functionality
- **JWT Authentication System** - Secure user registration and token-based authentication
- **Intelligent Text Processing** - Automatic paragraph splitting and content ingestion
- **Real-time Word Analytics** - Dynamic word frequency computation per user and globally
- **Advanced Search API** - Fast text search with contextual result excerpts
- **Asynchronous Task Processing** - Background job handling with Celery and Redis

### Technical Excellence
- **Containerized Architecture** - Complete Docker and Docker Compose setup
- **Database Optimization** - PostgreSQL with strategic indexes for sub-second queries
- **Scalable Design** - Microservices-ready architecture with separated concerns
- **Production-Ready** - Environment configuration and deployment best practices

##  Tech Stack

| Category | Technologies |
|----------|-------------|
| **Backend** | Python 3.11, Django 4.2, Django REST Framework |
| **Database** | PostgreSQL 15 with optimized indexing |
| **Task Queue** | Celery 5.3, Redis 7.0 |
| **Authentication** | JWT (djangorestframework-simplejwt) |
| **Containerization** | Docker, Docker Compose |
| **Development** | Python-dotenv, PGAdmin 4 |

## 🏗 System Architecture

```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   Client Apps   │───▶│  Django REST    │───▶│   PostgreSQL    │
│                 │    │      API        │    │    Database     │
└─────────────────┘    └─────────────────┘    └─────────────────┘
                               │
                               ▼
                       ┌─────────────────┐    ┌─────────────────┐
                       │  Celery Worker  │◀──▶│  Redis Broker   │
                       │  (Background    │    │   & Cache       │
                       │   Processing)   │    │                 │
                       └─────────────────┘    └─────────────────┘
```

### Key Components:
- **Django REST API** - Handles authentication, data ingestion, and search requests
- **PostgreSQL Database** - Stores users, paragraphs, and word frequencies with optimized indexes
- **Celery Workers** - Process text analysis tasks asynchronously
- **Redis** - Message broker and caching layer
- **Docker Compose** - Orchestrates all services for seamless deployment

##  Quick Start

### Prerequisites
- Docker & Docker Compose
- Git

### Installation

1. **Clone the Repository**
   ```bash
   git clone https://github.com/SREEJITH7/text-analytics-api.git
   cd text-analytics-api
   ```

2. **Environment Configuration**
   ```bash
   # Create .env file with the following variables:
   cat > .env << EOL
   POSTGRES_DB=textanalytics_db
   POSTGRES_USER=textanalytics_user
   POSTGRES_PASSWORD=your_secure_password
   POSTGRES_HOST=db
   POSTGRES_PORT=5432
   SECRET_KEY=your_django_secret_key_here
   DEBUG=True
   CELERY_BROKER_URL=redis://redis:6379/0
   CELERY_RESULT_BACKEND=redis://redis:6379/1
   EOL
   ```

3. **Launch the Application**
   ```bash
   # Build and start all services
   docker-compose up --build
   
   # Apply database migrations
   docker-compose exec web python manage.py migrate
   
   # Create superuser (optional)
   docker-compose exec web python manage.py createsuperuser
   ```

4. **Access the Services**
   - **API Server**: http://localhost:8000
   - **PGAdmin**: http://localhost:5050 (admin@admin.com / admin)
   - **API Documentation**: http://localhost:8000/api/docs/

##  API Documentation

### Authentication Endpoints

| Endpoint | Method | Description | Request Body |
|----------|--------|-------------|--------------|
| `/api/v1/auth/register/` | POST | Register new user | `{"username": "user", "email": "user@email.com", "password": "password"}` |
| `/api/v1/auth/login/` | POST | Login and get JWT tokens | `{"username": "user", "password": "password"}` |
| `/api/v1/auth/refresh/` | POST | Refresh access token | `{"refresh": "refresh_token"}` |

### Core API Endpoints

| Endpoint | Method | Description | Parameters |
|----------|--------|-------------|------------|
| `/api/v1/paragraphs/` | POST | Upload and process text | `{"content": "Your text content here"}` |
| `/api/v1/search/` | GET | Search for words | `?word=example&limit=10&offset=0` |
| `/api/v1/analytics/` | GET | Get user's word frequency stats | `?top=20` |

### Error Responses

All API errors follow a consistent format:

```json
// 400 Bad Request
{
    "error": "Bad Request",
    "details": {"content": ["This field is required."]}
}

// 401 Unauthorized  
{
    "error": "Unauthorized",
    "message": "Authentication credentials were not provided."
}

// 404 Not Found
{
    "error": "Not Found", 
    "message": "The requested resource was not found."
}
```

### Example Usage

```bash
# Register a new user
curl -X POST http://localhost:8000/api/v1/auth/register/ \
  -H "Content-Type: application/json" \
  -d '{"username": "testuser", "email": "test@example.com", "password": "securepass123"}'
```

**Response (201 Created):**
```json
{
    "user": {"id": 1, "username": "testuser", "email": "test@example.com"},
    "access": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...",
    "refresh": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9..."
}
```

```bash
# Login and get tokens
curl -X POST http://localhost:8000/api/v1/auth/login/ \
  -H "Content-Type: application/json" \
  -d '{"username": "testuser", "password": "securepass123"}'
```

**Response (200 OK):**
```json
{
    "access": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...",
    "refresh": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9..."
}
```

```bash
# Upload text content
curl -X POST http://localhost:8000/api/v1/paragraphs/ \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN" \
  -d '{"content": "This is a sample paragraph for text analysis."}'
```

**Response (201 Created):**
```json
{
    "id": 1,
    "content": "This is a sample paragraph for text analysis.",
    "word_count": 8,
    "processing_status": "completed",
    "created_at": "2025-08-14T10:30:00Z"
}
```

```bash
# Search for words
curl "http://localhost:8000/api/v1/search/?word=sample&limit=5" \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN"
```

**Response (200 OK):**
```json
{
    "count": 1,
    "results": [
        {
            "paragraph_id": 1,
            "content": "This is a **sample** paragraph for text analysis.",
            "word_frequency": 1,
            "created_at": "2025-08-14T10:30:00Z"
        }
    ]
}
```

## 🐳 Docker Deployment

### Services Overview

| Service | Description | Port | Purpose |
|---------|-------------|------|---------|
| **web** | Django application | 8000 | Main API server |
| **db** | PostgreSQL database | 5432 | Data persistence |
| **redis** | Redis cache/broker | 6379 | Message queuing |
| **celery** | Background worker | - | Async task processing |
| **celery-beat** | Task scheduler | - | Periodic tasks |
| **pgadmin** | DB management | 5050 | Database administration |

### Deployment Commands

```bash
# Start all services
docker-compose up -d

# View logs
docker-compose logs -f web

# Scale celery workers
docker-compose up --scale celery=3

# Stop all services
docker-compose down

# Reset database
docker-compose down -v && docker-compose up --build
```

## 🔮 Future Enhancements

### Performance & Scalability
- **Elasticsearch Integration** - Advanced full-text search capabilities
- **Redis Caching** - Implement comprehensive caching strategy
- **Database Sharding** - Horizontal scaling for large datasets
- **API Rate Limiting** - Implement request throttling

### Features & Functionality
- **Rich Analytics Dashboard** - Web-based visualization of word frequency trends
- **Export Capabilities** - PDF/Excel reports of text analytics
- **Multi-language Support** - Text processing for multiple languages
- **Batch Processing** - Handle large document uploads efficiently

### Development & Operations
- **Comprehensive Test Suite** - Unit, integration, and end-to-end tests
- **CI/CD Pipeline** - Automated testing and deployment with GitHub Actions
- **Monitoring & Logging** - Application performance monitoring
- **API Documentation** - Interactive Swagger/OpenAPI documentation

## 📞 Contact

**Sreejith TK**  
*Aspiring Backend Developer | Django Enthusiast*

- **Email**: sree7ith@gmail.com
- **GitHub**: [@SREEJITH7](https://github.com/SREEJITH7)
- **LinkedIn**: [sreejith-tk-348028257](https://linkedin.com/in/sreejith-tk-348028257)

---

*This project demonstrates advanced Django development skills and backend engineering capabilities for the **Codemonk** internship opportunity. Built with passion for clean code, scalable architecture, and modern development practices.*

