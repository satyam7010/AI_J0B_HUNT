# Database Schema

This document outlines the database schema used in the AI Job Hunt system.

## Overview

The system uses SQLite for data storage, with the database file located at `job_applications.db`.

## Tables

### Resume

Stores parsed resume data.

| Column      | Type    | Description                     |
|-------------|---------|---------------------------------|
| id          | TEXT    | Primary key (UUID)              |
| content     | TEXT    | Raw resume text                 |
| parsed_data | TEXT    | JSON of parsed resume data      |
| user_id     | TEXT    | Associated user ID              |
| created_at  | TEXT    | Creation timestamp              |
| updated_at  | TEXT    | Last update timestamp           |

### Job

Stores job descriptions and their analysis.

| Column      | Type    | Description                     |
|-------------|---------|---------------------------------|
| id          | TEXT    | Primary key (UUID)              |
| title       | TEXT    | Job title                       |
| company     | TEXT    | Company name                    |
| description | TEXT    | Raw job description             |
| analysis    | TEXT    | JSON of job analysis            |
| url         | TEXT    | Source URL of job listing       |
| created_at  | TEXT    | Creation timestamp              |

### Application

Stores applications that match resumes to jobs.

| Column         | Type    | Description                           |
|----------------|---------|---------------------------------------|
| id             | TEXT    | Primary key (UUID)                    |
| resume_id      | TEXT    | Foreign key to Resume table           |
| job_id         | TEXT    | Foreign key to Job table              |
| optimized_data | TEXT    | JSON of optimized resume data         |
| match_score    | REAL    | Score indicating resume-job match     |
| status         | TEXT    | Application status                    |
| submitted_at   | TEXT    | Submission timestamp                  |
| created_at     | TEXT    | Creation timestamp                    |
| updated_at     | TEXT    | Last update timestamp                 |

## Relationships

- Each Application is associated with exactly one Resume and one Job
- A Resume can be used in multiple Applications
- A Job can have multiple Applications

## Indexes

- Index on `resume_id` in the Application table
- Index on `job_id` in the Application table

## Example Queries

### Get all applications for a specific resume

```sql
SELECT a.*, j.title, j.company
FROM Application a
JOIN Job j ON a.job_id = j.id
WHERE a.resume_id = '123e4567-e89b-12d3-a456-426614174000';
```

### Get match score statistics

```sql
SELECT 
    MIN(match_score) as min_score,
    MAX(match_score) as max_score,
    AVG(match_score) as avg_score
FROM Application;
```

### Get applications by status

```sql
SELECT a.*, j.title, j.company
FROM Application a
JOIN Job j ON a.job_id = j.id
WHERE a.status = 'submitted'
ORDER BY a.submitted_at DESC;
```
