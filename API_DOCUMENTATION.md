# Research Management System - REST API Documentation

## Base URL
```
http://localhost:5000/api/v1
```

## Authentication
Most endpoints require authentication using Flask-Login session cookies.

## Response Format
All responses follow this structure:

### Success Response
```json
{
  "success": true,
  "data": {...}
}
```

### Error Response
```json
{
  "success": false,
  "error": "Error message"
}
```

---

## Research Endpoints

### 1. Get All Researches
```http
GET /api/v1/researches
```

#### Query Parameters
| Parameter | Type | Description |
|-----------|------|-------------|
| page | integer | Page number (default: 1) |
| per_page | integer | Items per page (default: 10, max: 100) |
| search | string | Search in title, authors, keywords |
| category_id | integer | Filter by category ID |
| publication_type | string | Filter by publication type |
| year | integer | Filter by publication year |
| sort_by | string | Sort field (created_at, title, year, view_count) |
| order | string | Sort order (ASC, DESC) |

#### Example Request
```bash
curl "http://localhost:5000/api/v1/researches?page=1&per_page=10&search=machine learning&category_id=1"
```

#### Example Response
```json
{
  "success": true,
  "data": [
    {
      "id": 1,
      "title": "Machine Learning Applications",
      "title_en": "Machine Learning Applications",
      "authors": "John Doe, Jane Smith",
      "year": 2023,
      "publication_type": "journal",
      "view_count": 150,
      "download_count": 45,
      "created_at": "2023-01-15T10:30:00",
      "updated_at": "2023-01-15T10:30:00"
    }
  ],
  "pagination": {
    "page": 1,
    "per_page": 10,
    "total": 100,
    "pages": 10,
    "has_next": true,
    "has_prev": false
  }
}
```

---

### 2. Get Single Research
```http
GET /api/v1/researches/{id}
```

#### Path Parameters
| Parameter | Type | Description |
|-----------|------|-------------|
| id | integer | Research ID |

#### Example Request
```bash
curl "http://localhost:5000/api/v1/researches/1"
```

#### Example Response
```json
{
  "success": true,
  "data": {
    "id": 1,
    "title": "Machine Learning Applications",
    "title_en": "Machine Learning Applications",
    "authors": "John Doe, Jane Smith",
    "abstract": "This research explores...",
    "keywords": "machine learning, AI, neural networks",
    "year": 2023,
    "publication_type": "journal",
    "journal_name": "Journal of AI Research",
    "volume": "15",
    "issue": "3",
    "pages": "45-67",
    "doi": "10.1234/example",
    "url": "https://example.com/research",
    "file_path": "uploads/researches/paper_20230115.pdf",
    "view_count": 150,
    "download_count": 45,
    "category": {
      "id": 1,
      "name": "Artificial Intelligence"
    },
    "uploader": {
      "id": 1,
      "username": "john_doe",
      "full_name": "John Doe"
    },
    "tags": [
      {"id": 1, "name": "machine learning"},
      {"id": 2, "name": "AI"}
    ],
    "comments_count": 5,
    "created_at": "2023-01-15T10:30:00",
    "updated_at": "2023-01-15T10:30:00"
  }
}
```

---

### 3. Create Research
```http
POST /api/v1/researches
```

#### Request Headers
```
Content-Type: application/json
```

#### Request Body
```json
{
  "title": "New Research Title",
  "title_en": "New Research Title (EN)",
  "authors": "Author 1, Author 2",
  "abstract": "Research abstract...",
  "keywords": "keyword1, keyword2",
  "year": 2023,
  "publication_type": "journal",
  "journal_name": "Journal Name",
  "volume": "10",
  "issue": "2",
  "pages": "10-20",
  "doi": "10.1234/example",
  "url": "https://example.com",
  "category_id": 1
}
```

#### Example Request
```bash
curl -X POST http://localhost:5000/api/v1/researches \
  -H "Content-Type: application/json" \
  -d '{
    "title": "AI Research",
    "authors": "John Doe",
    "year": 2023
  }'
```

#### Example Response
```json
{
  "success": true,
  "data": {
    "id": 123,
    "title": "AI Research",
    ...
  }
}
```

---

### 4. Update Research
```http
PUT /api/v1/researches/{id}
```

#### Request Body
Same as Create Research (all fields optional)

#### Example Request
```bash
curl -X PUT http://localhost:5000/api/v1/researches/123 \
  -H "Content-Type: application/json" \
  -d '{
    "title": "Updated Title"
  }'
```

---

### 5. Delete Research
```http
DELETE /api/v1/researches/{id}
```

#### Example Request
```bash
curl -X DELETE http://localhost:5000/api/v1/researches/123
```

#### Example Response
```json
{
  "success": true,
  "message": "ลบงานวิจัยสำเร็จ"
}
```

---

## Category Endpoints

### 1. Get All Categories
```http
GET /api/v1/categories
```

#### Example Response
```json
{
  "success": true,
  "data": [
    {
      "id": 1,
      "name": "Artificial Intelligence",
      "description": "AI related research",
      "research_count": 25
    }
  ]
}
```

---

### 2. Get Single Category
```http
GET /api/v1/categories/{id}
```

---

## Tag Endpoints

### Get All Tags
```http
GET /api/v1/tags
```

#### Example Response
```json
{
  "success": true,
  "data": [
    {
      "id": 1,
      "name": "machine learning",
      "research_count": 42
    }
  ]
}
```

---

## Bookmark Endpoints

### 1. Get User Bookmarks
```http
GET /api/v1/bookmarks
```
**Requires authentication**

#### Example Response
```json
{
  "success": true,
  "data": [
    {
      "id": 1,
      "research": {
        "id": 5,
        "title": "Bookmarked Research",
        ...
      },
      "created_at": "2023-01-20T14:30:00"
    }
  ]
}
```

---

### 2. Add Bookmark
```http
POST /api/v1/bookmarks/{research_id}
```
**Requires authentication**

#### Example Request
```bash
curl -X POST http://localhost:5000/api/v1/bookmarks/5
```

#### Example Response
```json
{
  "success": true,
  "message": "เพิ่มบุ๊กมาร์กสำเร็จ"
}
```

---

### 3. Remove Bookmark
```http
DELETE /api/v1/bookmarks/{research_id}
```
**Requires authentication**

---

## Comment Endpoints

### 1. Get Research Comments
```http
GET /api/v1/researches/{research_id}/comments
```

#### Example Response
```json
{
  "success": true,
  "data": [
    {
      "id": 1,
      "content": "Great research!",
      "rating": 5,
      "user": {
        "id": 2,
        "username": "jane_smith",
        "full_name": "Jane Smith"
      },
      "created_at": "2023-01-21T09:15:00",
      "updated_at": "2023-01-21T09:15:00"
    }
  ]
}
```

---

### 2. Add Comment
```http
POST /api/v1/researches/{research_id}/comments
```
**Requires authentication**

#### Request Body
```json
{
  "content": "This is a great research paper!",
  "rating": 5
}
```

#### Example Request
```bash
curl -X POST http://localhost:5000/api/v1/researches/5/comments \
  -H "Content-Type: application/json" \
  -d '{
    "content": "Excellent work!",
    "rating": 5
  }'
```

---

## Statistics Endpoint

### Get System Statistics
```http
GET /api/v1/statistics
```

#### Example Response
```json
{
  "success": true,
  "data": {
    "totals": {
      "researches": 150,
      "users": 25,
      "categories": 10,
      "tags": 50,
      "bookmarks": 200,
      "comments": 85
    },
    "publication_types": [
      {"type": "journal", "count": 80},
      {"type": "conference", "count": 50},
      {"type": "thesis", "count": 20}
    ],
    "by_year": [
      {"year": 2023, "count": 45},
      {"year": 2022, "count": 38},
      {"year": 2021, "count": 32}
    ],
    "popular": [
      {
        "id": 1,
        "title": "Most Viewed Research",
        "view_count": 500
      }
    ]
  }
}
```

---

## Error Codes

| Code | Description |
|------|-------------|
| 200 | Success |
| 201 | Created |
| 400 | Bad Request |
| 401 | Unauthorized |
| 403 | Forbidden |
| 404 | Not Found |
| 500 | Internal Server Error |

---

## Examples

### Python (requests)
```python
import requests

# Get all researches
response = requests.get('http://localhost:5000/api/v1/researches')
data = response.json()

# Create research
new_research = {
    'title': 'My Research',
    'authors': 'John Doe',
    'year': 2023
}
response = requests.post(
    'http://localhost:5000/api/v1/researches',
    json=new_research
)
```

### JavaScript (fetch)
```javascript
// Get all researches
fetch('http://localhost:5000/api/v1/researches')
  .then(response => response.json())
  .then(data => console.log(data));

// Create research
fetch('http://localhost:5000/api/v1/researches', {
  method: 'POST',
  headers: {
    'Content-Type': 'application/json'
  },
  body: JSON.stringify({
    title: 'My Research',
    authors: 'John Doe',
    year: 2023
  })
})
  .then(response => response.json())
  .then(data => console.log(data));
```

### cURL
```bash
# Get researches with filters
curl "http://localhost:5000/api/v1/researches?search=AI&year=2023&sort_by=view_count&order=DESC"

# Create research
curl -X POST http://localhost:5000/api/v1/researches \
  -H "Content-Type: application/json" \
  -d '{
    "title": "Machine Learning Study",
    "authors": "John Doe, Jane Smith",
    "year": 2023,
    "publication_type": "journal"
  }'

# Update research
curl -X PUT http://localhost:5000/api/v1/researches/1 \
  -H "Content-Type: application/json" \
  -d '{"title": "Updated Title"}'

# Delete research
curl -X DELETE http://localhost:5000/api/v1/researches/1

# Get statistics
curl http://localhost:5000/api/v1/statistics
```

---

## Rate Limiting
Currently no rate limiting is implemented. Consider implementing rate limiting for production use.

## CORS
CORS is enabled for all `/api/*` endpoints with origin `*`. Configure appropriately for production.

## Pagination
All list endpoints support pagination:
- Default: 10 items per page
- Maximum: 100 items per page

---

**API Version**: v1
**Last Updated**: 2025-11-05
