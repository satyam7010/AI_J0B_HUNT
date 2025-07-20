# AI Job Hunt API Reference

This document provides a reference for the API endpoints available in the AI Job Hunt system.

## Base URL

All API endpoints are prefixed with: `/api`

## Authentication

Most endpoints require authentication. Include the API key in the `X-API-Key` header.

## Endpoints

### Resume Endpoints

#### `POST /api/resumes/upload`

Upload and parse a resume.

**Request Body:**
- `file`: Resume file (PDF, DOCX, or TXT)

**Response:**
```json
{
  "resume_id": "123e4567-e89b-12d3-a456-426614174000",
  "parsed_data": {
    "name": "John Doe",
    "email": "john@example.com",
    "skills": ["Python", "JavaScript", "React"],
    ...
  }
}
```

#### `GET /api/resumes/{resume_id}`

Get a specific resume by ID.

**Response:**
```json
{
  "resume_id": "123e4567-e89b-12d3-a456-426614174000",
  "parsed_data": { ... },
  "created_at": "2025-07-15T12:00:00Z",
  "updated_at": "2025-07-15T12:00:00Z"
}
```

### Job Endpoints

#### `POST /api/jobs/analyze`

Analyze a job description.

**Request Body:**
- `job_description`: Job description text

**Response:**
```json
{
  "job_id": "123e4567-e89b-12d3-a456-426614174000",
  "analysis": {
    "required_skills": ["Python", "JavaScript", "React"],
    "preferred_skills": ["TypeScript", "Docker"],
    "responsibilities": ["Develop web applications", ...],
    ...
  }
}
```

#### `GET /api/jobs/{job_id}`

Get a specific job by ID.

**Response:**
```json
{
  "job_id": "123e4567-e89b-12d3-a456-426614174000",
  "analysis": { ... },
  "created_at": "2025-07-15T12:00:00Z"
}
```

### Application Endpoints

#### `POST /api/applications/optimize`

Optimize a resume for a specific job.

**Request Body:**
- `resume_id`: ID of the resume
- `job_id`: ID of the job
- `optimization_level`: Level of optimization (conservative, balanced, aggressive)

**Response:**
```json
{
  "application_id": "123e4567-e89b-12d3-a456-426614174000",
  "optimized_resume": { ... },
  "match_analysis": {
    "match_score": 85,
    "matching_skills": ["Python", "JavaScript"],
    "missing_skills": ["TypeScript"],
    ...
  }
}
```

#### `POST /api/applications/submit`

Submit an application.

**Request Body:**
- `application_id`: ID of the application
- `platform`: Platform to submit to (linkedin, indeed, etc.)
- `credentials`: Platform credentials (if required)

**Response:**
```json
{
  "status": "submitted",
  "platform_reference": "A123456",
  "submitted_at": "2025-07-15T12:00:00Z"
}
```

### Dashboard Endpoints

#### `GET /api/dashboard/stats`

Get dashboard statistics.

**Response:**
```json
{
  "total_resumes": 5,
  "total_jobs": 10,
  "total_applications": 8,
  "application_statuses": {
    "pending": 2,
    "submitted": 4,
    "rejected": 1,
    "interview": 1
  }
}
```

## Error Responses

All endpoints may return the following error responses:

- `400 Bad Request`: Invalid request
- `401 Unauthorized`: Missing or invalid API key
- `404 Not Found`: Resource not found
- `500 Internal Server Error`: Server error
