"""
Database manager service
Handles all database operations
"""

import os
import sqlite3
import json
from typing import Dict, Any, List, Optional, Tuple
from datetime import datetime
import asyncio

from utils.logger import setup_logger
from config.settings import settings

logger = setup_logger(__name__)

class DatabaseManager:
    """Database management service"""
    
    def __init__(self, db_path: Optional[str] = None):
        """Initialize database manager"""
        self.logger = logger
        self.db_path = db_path or settings.database.url or "job_applications.db"
        # Convert SQLAlchemy URL to SQLite path if needed
        if self.db_path.startswith("sqlite:///"):
            self.db_path = self.db_path.replace("sqlite:///", "")
        self.connection = None
    
    async def init_db(self):
        """Initialize the database schema"""
        try:
            conn = self._get_connection()
            cursor = conn.cursor()
            
            # Create resumes table
            cursor.execute('''
            CREATE TABLE IF NOT EXISTS resumes (
                id INTEGER PRIMARY KEY,
                name TEXT NOT NULL,
                content TEXT NOT NULL,
                parsed_data TEXT NOT NULL,
                file_path TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
            ''')
            
            # Create jobs table
            cursor.execute('''
            CREATE TABLE IF NOT EXISTS jobs (
                id INTEGER PRIMARY KEY,
                title TEXT NOT NULL,
                company TEXT,
                location TEXT,
                description TEXT NOT NULL,
                url TEXT,
                salary_range TEXT,
                job_type TEXT,
                experience_level TEXT,
                remote_status TEXT,
                platform TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
            ''')
            
            # Create applications table
            cursor.execute('''
            CREATE TABLE IF NOT EXISTS applications (
                id INTEGER PRIMARY KEY,
                job_id INTEGER NOT NULL,
                resume_id INTEGER NOT NULL,
                optimized_resume_id INTEGER,
                cover_letter_id INTEGER,
                status TEXT DEFAULT 'pending',
                notes TEXT,
                platform TEXT,
                platform_application_id TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (job_id) REFERENCES jobs (id),
                FOREIGN KEY (resume_id) REFERENCES resumes (id),
                FOREIGN KEY (optimized_resume_id) REFERENCES resumes (id),
                FOREIGN KEY (cover_letter_id) REFERENCES cover_letters (id)
            )
            ''')
            
            # Create cover_letters table
            cursor.execute('''
            CREATE TABLE IF NOT EXISTS cover_letters (
                id INTEGER PRIMARY KEY,
                resume_id INTEGER NOT NULL,
                job_id INTEGER NOT NULL,
                content TEXT NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (resume_id) REFERENCES resumes (id),
                FOREIGN KEY (job_id) REFERENCES jobs (id)
            )
            ''')
            
            # Create search_queries table
            cursor.execute('''
            CREATE TABLE IF NOT EXISTS search_queries (
                id INTEGER PRIMARY KEY,
                query TEXT NOT NULL,
                platform TEXT NOT NULL,
                location TEXT,
                job_type TEXT,
                date_range TEXT,
                remote_only BOOLEAN DEFAULT 0,
                results_count INTEGER DEFAULT 0,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
            ''')
            
            # Create settings table
            cursor.execute('''
            CREATE TABLE IF NOT EXISTS settings (
                id INTEGER PRIMARY KEY,
                key TEXT UNIQUE NOT NULL,
                value TEXT NOT NULL,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
            ''')
            
            # Create job_skills table for many-to-many relationship
            cursor.execute('''
            CREATE TABLE IF NOT EXISTS job_skills (
                id INTEGER PRIMARY KEY,
                job_id INTEGER NOT NULL,
                skill TEXT NOT NULL,
                is_required BOOLEAN DEFAULT 1,
                FOREIGN KEY (job_id) REFERENCES jobs (id)
            )
            ''')
            
            # Create resume_skills table for many-to-many relationship
            cursor.execute('''
            CREATE TABLE IF NOT EXISTS resume_skills (
                id INTEGER PRIMARY KEY,
                resume_id INTEGER NOT NULL,
                skill TEXT NOT NULL,
                FOREIGN KEY (resume_id) REFERENCES resumes (id)
            )
            ''')
            
            # Create user_credentials table for storing encrypted credentials
            cursor.execute('''
            CREATE TABLE IF NOT EXISTS user_credentials (
                id INTEGER PRIMARY KEY,
                platform TEXT UNIQUE NOT NULL,
                username TEXT NOT NULL,
                password_encrypted TEXT NOT NULL,
                auth_token TEXT,
                refresh_token TEXT,
                last_used TIMESTAMP,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
            ''')
            
            # Create logs table
            cursor.execute('''
            CREATE TABLE IF NOT EXISTS logs (
                id INTEGER PRIMARY KEY,
                level TEXT NOT NULL,
                message TEXT NOT NULL,
                context TEXT,
                timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
            ''')
            
            conn.commit()
            self.logger.info("Database initialized successfully")
            
        except Exception as e:
            self.logger.error(f"Error initializing database: {str(e)}")
            raise
    
    def _get_connection(self):
        """Get a database connection"""
        if self.connection is None:
            self.connection = sqlite3.connect(self.db_path)
            # Enable foreign keys
            self.connection.execute("PRAGMA foreign_keys = ON")
            # Configure row factory to return dictionaries
            self.connection.row_factory = self._dict_factory
        return self.connection
    
    @staticmethod
    def _dict_factory(cursor, row):
        """Convert row to dictionary"""
        d = {}
        for idx, col in enumerate(cursor.description):
            d[col[0]] = row[idx]
        return d
    
    def close(self):
        """Close database connection"""
        if self.connection:
            self.connection.close()
            self.connection = None
    
    async def save_resume(self, name: str, content: str, parsed_data: Dict[str, Any], file_path: Optional[str] = None) -> int:
        """
        Save a resume to the database
        
        Args:
            name: Resume name
            content: Raw resume content
            parsed_data: Parsed resume data
            file_path: Path to resume file
            
        Returns:
            ID of the saved resume
        """
        try:
            conn = self._get_connection()
            cursor = conn.cursor()
            
            # Check if resume already exists
            cursor.execute(
                "SELECT id FROM resumes WHERE name = ?",
                (name,)
            )
            existing = cursor.fetchone()
            
            if existing:
                # Update existing resume
                cursor.execute(
                    """
                    UPDATE resumes 
                    SET content = ?, parsed_data = ?, file_path = ?, updated_at = CURRENT_TIMESTAMP 
                    WHERE id = ?
                    """,
                    (content, json.dumps(parsed_data), file_path, existing["id"])
                )
                resume_id = existing["id"]
                self.logger.info(f"Updated existing resume: {name} (ID: {resume_id})")
            else:
                # Insert new resume
                cursor.execute(
                    """
                    INSERT INTO resumes (name, content, parsed_data, file_path)
                    VALUES (?, ?, ?, ?)
                    """,
                    (name, content, json.dumps(parsed_data), file_path)
                )
                resume_id = cursor.lastrowid
                self.logger.info(f"Saved new resume: {name} (ID: {resume_id})")
            
            # Save resume skills if present
            if "skills" in parsed_data and parsed_data["skills"]:
                # Delete existing skills
                cursor.execute("DELETE FROM resume_skills WHERE resume_id = ?", (resume_id,))
                
                # Insert new skills
                skills = parsed_data["skills"]
                if isinstance(skills, list):
                    for skill in skills:
                        cursor.execute(
                            "INSERT INTO resume_skills (resume_id, skill) VALUES (?, ?)",
                            (resume_id, skill)
                        )
            
            conn.commit()
            return resume_id
            
        except Exception as e:
            conn.rollback()
            self.logger.error(f"Error saving resume: {str(e)}")
            raise
    
    async def get_resume(self, resume_id: int) -> Optional[Dict[str, Any]]:
        """
        Get a resume by ID
        
        Args:
            resume_id: Resume ID
            
        Returns:
            Resume data or None if not found
        """
        try:
            conn = self._get_connection()
            cursor = conn.cursor()
            
            cursor.execute(
                "SELECT * FROM resumes WHERE id = ?",
                (resume_id,)
            )
            resume = cursor.fetchone()
            
            if not resume:
                return None
            
            # Parse JSON data
            resume["parsed_data"] = json.loads(resume["parsed_data"])
            
            # Get skills
            cursor.execute(
                "SELECT skill FROM resume_skills WHERE resume_id = ?",
                (resume_id,)
            )
            skills = [row["skill"] for row in cursor.fetchall()]
            resume["skills"] = skills
            
            return resume
            
        except Exception as e:
            self.logger.error(f"Error getting resume: {str(e)}")
            raise
    
    async def get_all_resumes(self) -> List[Dict[str, Any]]:
        """
        Get all resumes
        
        Returns:
            List of all resumes
        """
        try:
            conn = self._get_connection()
            cursor = conn.cursor()
            
            cursor.execute("SELECT * FROM resumes ORDER BY updated_at DESC")
            resumes = cursor.fetchall()
            
            # Parse JSON data and get skills for each resume
            for resume in resumes:
                resume["parsed_data"] = json.loads(resume["parsed_data"])
                
                # Get skills
                cursor.execute(
                    "SELECT skill FROM resume_skills WHERE resume_id = ?",
                    (resume["id"],)
                )
                skills = [row["skill"] for row in cursor.fetchall()]
                resume["skills"] = skills
            
            return resumes
            
        except Exception as e:
            self.logger.error(f"Error getting all resumes: {str(e)}")
            raise
    
    async def delete_resume(self, resume_id: int) -> bool:
        """
        Delete a resume by ID
        
        Args:
            resume_id: Resume ID
            
        Returns:
            True if deleted, False if not found
        """
        try:
            conn = self._get_connection()
            cursor = conn.cursor()
            
            # Check if resume exists
            cursor.execute(
                "SELECT id FROM resumes WHERE id = ?",
                (resume_id,)
            )
            if not cursor.fetchone():
                return False
            
            # Delete resume skills
            cursor.execute("DELETE FROM resume_skills WHERE resume_id = ?", (resume_id,))
            
            # Delete resume
            cursor.execute("DELETE FROM resumes WHERE id = ?", (resume_id,))
            
            conn.commit()
            self.logger.info(f"Deleted resume ID: {resume_id}")
            return True
            
        except Exception as e:
            conn.rollback()
            self.logger.error(f"Error deleting resume: {str(e)}")
            raise
            
    async def save_job(self, job_data: Dict[str, Any]) -> int:
        """
        Save a job to the database
        
        Args:
            job_data: Job data
            
        Returns:
            ID of the saved job
        """
        try:
            conn = self._get_connection()
            cursor = conn.cursor()
            
            # Extract job fields
            title = job_data.get("title", "")
            company = job_data.get("company", "")
            location = job_data.get("location", "")
            description = job_data.get("description", "")
            url = job_data.get("url", "")
            salary_range = job_data.get("salary_range", "")
            job_type = job_data.get("job_type", "")
            experience_level = job_data.get("experience_level", "")
            remote_status = job_data.get("remote_status", "")
            platform = job_data.get("platform", "")
            
            # Check if job already exists by URL
            if url:
                cursor.execute(
                    "SELECT id FROM jobs WHERE url = ?",
                    (url,)
                )
                existing = cursor.fetchone()
                
                if existing:
                    # Update existing job
                    cursor.execute(
                        """
                        UPDATE jobs 
                        SET title = ?, company = ?, location = ?, description = ?, 
                            salary_range = ?, job_type = ?, experience_level = ?, 
                            remote_status = ?, platform = ?, updated_at = CURRENT_TIMESTAMP 
                        WHERE id = ?
                        """,
                        (title, company, location, description, salary_range, 
                         job_type, experience_level, remote_status, platform, existing["id"])
                    )
                    job_id = existing["id"]
                    self.logger.info(f"Updated existing job: {title} at {company} (ID: {job_id})")
                else:
                    # Insert new job
                    cursor.execute(
                        """
                        INSERT INTO jobs (title, company, location, description, url, 
                                          salary_range, job_type, experience_level, 
                                          remote_status, platform)
                        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                        """,
                        (title, company, location, description, url, salary_range, 
                         job_type, experience_level, remote_status, platform)
                    )
                    job_id = cursor.lastrowid
                    self.logger.info(f"Saved new job: {title} at {company} (ID: {job_id})")
            else:
                # Insert new job without URL check
                cursor.execute(
                    """
                    INSERT INTO jobs (title, company, location, description, url, 
                                      salary_range, job_type, experience_level, 
                                      remote_status, platform)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                    """,
                    (title, company, location, description, url, salary_range, 
                     job_type, experience_level, remote_status, platform)
                )
                job_id = cursor.lastrowid
                self.logger.info(f"Saved new job: {title} at {company} (ID: {job_id})")
            
            # Save job skills if present
            if "required_skills" in job_data or "preferred_skills" in job_data:
                # Delete existing skills
                cursor.execute("DELETE FROM job_skills WHERE job_id = ?", (job_id,))
                
                # Insert required skills
                if "required_skills" in job_data and job_data["required_skills"]:
                    for skill in job_data["required_skills"]:
                        cursor.execute(
                            "INSERT INTO job_skills (job_id, skill, is_required) VALUES (?, ?, ?)",
                            (job_id, skill, True)
                        )
                
                # Insert preferred skills
                if "preferred_skills" in job_data and job_data["preferred_skills"]:
                    for skill in job_data["preferred_skills"]:
                        cursor.execute(
                            "INSERT INTO job_skills (job_id, skill, is_required) VALUES (?, ?, ?)",
                            (job_id, skill, False)
                        )
            
            conn.commit()
            return job_id
            
        except Exception as e:
            conn.rollback()
            self.logger.error(f"Error saving job: {str(e)}")
            raise
            
    async def get_job(self, job_id: int) -> Optional[Dict[str, Any]]:
        """
        Get a job by ID
        
        Args:
            job_id: Job ID
            
        Returns:
            Job data or None if not found
        """
        try:
            conn = self._get_connection()
            cursor = conn.cursor()
            
            cursor.execute(
                "SELECT * FROM jobs WHERE id = ?",
                (job_id,)
            )
            job = cursor.fetchone()
            
            if not job:
                return None
            
            # Get required skills
            cursor.execute(
                "SELECT skill FROM job_skills WHERE job_id = ? AND is_required = 1",
                (job_id,)
            )
            required_skills = [row["skill"] for row in cursor.fetchall()]
            job["required_skills"] = required_skills
            
            # Get preferred skills
            cursor.execute(
                "SELECT skill FROM job_skills WHERE job_id = ? AND is_required = 0",
                (job_id,)
            )
            preferred_skills = [row["skill"] for row in cursor.fetchall()]
            job["preferred_skills"] = preferred_skills
            
            return job
            
        except Exception as e:
            self.logger.error(f"Error getting job: {str(e)}")
            raise
            
    async def get_all_jobs(self, limit: int = 100, offset: int = 0, filters: Optional[Dict[str, Any]] = None) -> List[Dict[str, Any]]:
        """
        Get all jobs with optional filtering
        
        Args:
            limit: Maximum number of jobs to return
            offset: Offset for pagination
            filters: Optional filters to apply
            
        Returns:
            List of jobs
        """
        try:
            conn = self._get_connection()
            cursor = conn.cursor()
            
            query = "SELECT * FROM jobs"
            params = []
            
            # Apply filters if provided
            if filters:
                where_clauses = []
                
                if "title" in filters and filters["title"]:
                    where_clauses.append("title LIKE ?")
                    params.append(f"%{filters['title']}%")
                    
                if "company" in filters and filters["company"]:
                    where_clauses.append("company LIKE ?")
                    params.append(f"%{filters['company']}%")
                    
                if "location" in filters and filters["location"]:
                    where_clauses.append("location LIKE ?")
                    params.append(f"%{filters['location']}%")
                    
                if "job_type" in filters and filters["job_type"]:
                    where_clauses.append("job_type = ?")
                    params.append(filters["job_type"])
                    
                if "experience_level" in filters and filters["experience_level"]:
                    where_clauses.append("experience_level = ?")
                    params.append(filters["experience_level"])
                    
                if "remote_status" in filters and filters["remote_status"]:
                    where_clauses.append("remote_status = ?")
                    params.append(filters["remote_status"])
                    
                if "platform" in filters and filters["platform"]:
                    where_clauses.append("platform = ?")
                    params.append(filters["platform"])
                
                if where_clauses:
                    query += " WHERE " + " AND ".join(where_clauses)
            
            # Add sorting and pagination
            query += " ORDER BY created_at DESC LIMIT ? OFFSET ?"
            params.extend([limit, offset])
            
            cursor.execute(query, params)
            jobs = cursor.fetchall()
            
            # Get skills for each job
            for job in jobs:
                # Get required skills
                cursor.execute(
                    "SELECT skill FROM job_skills WHERE job_id = ? AND is_required = 1",
                    (job["id"],)
                )
                required_skills = [row["skill"] for row in cursor.fetchall()]
                job["required_skills"] = required_skills
                
                # Get preferred skills
                cursor.execute(
                    "SELECT skill FROM job_skills WHERE job_id = ? AND is_required = 0",
                    (job["id"],)
                )
                preferred_skills = [row["skill"] for row in cursor.fetchall()]
                job["preferred_skills"] = preferred_skills
            
            return jobs
            
        except Exception as e:
            self.logger.error(f"Error getting all jobs: {str(e)}")
            raise
            
    async def delete_job(self, job_id: int) -> bool:
        """
        Delete a job by ID
        
        Args:
            job_id: Job ID
            
        Returns:
            True if deleted, False if not found
        """
        try:
            conn = self._get_connection()
            cursor = conn.cursor()
            
            # Check if job exists
            cursor.execute(
                "SELECT id FROM jobs WHERE id = ?",
                (job_id,)
            )
            if not cursor.fetchone():
                return False
            
            # Delete job skills
            cursor.execute("DELETE FROM job_skills WHERE job_id = ?", (job_id,))
            
            # Delete job
            cursor.execute("DELETE FROM jobs WHERE id = ?", (job_id,))
            
            conn.commit()
            self.logger.info(f"Deleted job ID: {job_id}")
            return True
            
        except Exception as e:
            conn.rollback()
            self.logger.error(f"Error deleting job: {str(e)}")
            raise
    
    async def save_application_result(self, job_data: Dict[str, Any], application_result: Dict[str, Any]) -> int:
        """
        Save application result to database
        
        Args:
            job_data: Job data
            application_result: Application result data
            
        Returns:
            ID of the saved application
        """
        try:
            # First, save the job to get a job_id
            job_id = await self.save_job(job_data)
            
            # Get resume_id from application_result or use default
            resume_id = application_result.get("resume_id", 1)  # Default to first resume if not specified
            
            # Extract application fields
            status = application_result.get("application_status", "pending")
            notes = application_result.get("notes", "")
            platform = job_data.get("platform", "")
            platform_application_id = application_result.get("platform_application_id", "")
            
            # If we have an optimized resume, save it
            optimized_resume_id = None
            if "optimized_resume" in application_result and application_result["optimized_resume"]:
                optimized_resume = application_result["optimized_resume"]
                optimized_content = optimized_resume.get("optimized_resume", "")
                if optimized_content:
                    # Save optimized resume
                    optimized_resume_name = f"{job_data.get('title', 'Job')} - Optimized"
                    parsed_data = {
                        "source": "ai_optimized",
                        "original_resume_id": resume_id,
                        "job_id": job_id,
                        "optimization_score": optimized_resume.get("optimization_score", 0),
                        "changes_made": optimized_resume.get("changes_made", []),
                        "keywords_added": optimized_resume.get("keywords_added", [])
                    }
                    optimized_resume_id = await self.save_resume(
                        optimized_resume_name, 
                        optimized_content, 
                        parsed_data
                    )
            
            # If we have a cover letter, save it
            cover_letter_id = None
            if "cover_letter" in application_result and application_result["cover_letter"]:
                cover_letter_content = application_result["cover_letter"]
                if cover_letter_content:
                    # Save cover letter
                    conn = self._get_connection()
                    cursor = conn.cursor()
                    cursor.execute(
                        """
                        INSERT INTO cover_letters (resume_id, job_id, content)
                        VALUES (?, ?, ?)
                        """,
                        (resume_id, job_id, cover_letter_content)
                    )
                    cover_letter_id = cursor.lastrowid
                    conn.commit()
            
            # Save application
            conn = self._get_connection()
            cursor = conn.cursor()
            
            cursor.execute(
                """
                INSERT INTO applications (
                    job_id, resume_id, optimized_resume_id, cover_letter_id,
                    status, notes, platform, platform_application_id
                )
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)
                """,
                (
                    job_id, resume_id, optimized_resume_id, cover_letter_id,
                    status, notes, platform, platform_application_id
                )
            )
            
            application_id = cursor.lastrowid
            conn.commit()
            
            self.logger.info(f"Saved application result: ID {application_id}, Status: {status}")
            return application_id
            
        except Exception as e:
            self.logger.error(f"Error saving application result: {str(e)}")
            raise
    
    async def get_application(self, application_id: int) -> Optional[Dict[str, Any]]:
        """
        Get application by ID
        
        Args:
            application_id: Application ID
            
        Returns:
            Application data or None if not found
        """
        try:
            conn = self._get_connection()
            cursor = conn.cursor()
            
            cursor.execute(
                """
                SELECT a.*, j.title, j.company, j.location, j.description, j.url,
                       r.name as resume_name, 
                       or.name as optimized_resume_name, 
                       cl.content as cover_letter
                FROM applications a
                LEFT JOIN jobs j ON a.job_id = j.id
                LEFT JOIN resumes r ON a.resume_id = r.id
                LEFT JOIN resumes or ON a.optimized_resume_id = or.id
                LEFT JOIN cover_letters cl ON a.cover_letter_id = cl.id
                WHERE a.id = ?
                """,
                (application_id,)
            )
            
            application = cursor.fetchone()
            
            if not application:
                return None
            
            # Get job skills
            cursor.execute(
                "SELECT skill, is_required FROM job_skills WHERE job_id = ?",
                (application["job_id"],)
            )
            
            required_skills = []
            preferred_skills = []
            
            for row in cursor.fetchall():
                if row["is_required"]:
                    required_skills.append(row["skill"])
                else:
                    preferred_skills.append(row["skill"])
            
            application["required_skills"] = required_skills
            application["preferred_skills"] = preferred_skills
            
            return application
            
        except Exception as e:
            self.logger.error(f"Error getting application: {str(e)}")
            raise
    
    async def get_all_applications(self, limit: int = 100, offset: int = 0, filters: Optional[Dict[str, Any]] = None) -> List[Dict[str, Any]]:
        """
        Get all applications with optional filtering
        
        Args:
            limit: Maximum number of applications to return
            offset: Offset for pagination
            filters: Optional filters to apply
            
        Returns:
            List of applications
        """
        try:
            conn = self._get_connection()
            cursor = conn.cursor()
            
            query = """
                SELECT a.*, j.title, j.company, j.location, j.url,
                       r.name as resume_name
                FROM applications a
                LEFT JOIN jobs j ON a.job_id = j.id
                LEFT JOIN resumes r ON a.resume_id = r.id
            """
            
            params = []
            
            # Apply filters if provided
            if filters:
                where_clauses = []
                
                if "status" in filters and filters["status"]:
                    where_clauses.append("a.status = ?")
                    params.append(filters["status"])
                    
                if "platform" in filters and filters["platform"]:
                    where_clauses.append("a.platform = ?")
                    params.append(filters["platform"])
                    
                if "job_title" in filters and filters["job_title"]:
                    where_clauses.append("j.title LIKE ?")
                    params.append(f"%{filters['job_title']}%")
                    
                if "company" in filters and filters["company"]:
                    where_clauses.append("j.company LIKE ?")
                    params.append(f"%{filters['company']}%")
                    
                if "date_from" in filters and filters["date_from"]:
                    where_clauses.append("a.created_at >= ?")
                    params.append(filters["date_from"])
                    
                if "date_to" in filters and filters["date_to"]:
                    where_clauses.append("a.created_at <= ?")
                    params.append(filters["date_to"])
                
                if where_clauses:
                    query += " WHERE " + " AND ".join(where_clauses)
            
            # Add sorting and pagination
            query += " ORDER BY a.created_at DESC LIMIT ? OFFSET ?"
            params.extend([limit, offset])
            
            cursor.execute(query, params)
            applications = cursor.fetchall()
            
            return applications
            
        except Exception as e:
            self.logger.error(f"Error getting all applications: {str(e)}")
            raise
    
    async def update_application_status(self, application_id: int, status: str, error_message: Optional[str] = None) -> bool:
        """
        Update application status
        
        Args:
            application_id: Application ID
            status: New status
            error_message: Optional error message
            
        Returns:
            True if updated, False if not found
        """
        try:
            conn = self._get_connection()
            cursor = conn.cursor()
            
            # Check if application exists
            cursor.execute(
                "SELECT id FROM applications WHERE id = ?",
                (application_id,)
            )
            if not cursor.fetchone():
                return False
            
            # Update notes if error message provided
            if error_message:
                cursor.execute(
                    """
                    UPDATE applications 
                    SET status = ?, notes = ?, updated_at = CURRENT_TIMESTAMP 
                    WHERE id = ?
                    """,
                    (status, error_message, application_id)
                )
            else:
                cursor.execute(
                    """
                    UPDATE applications 
                    SET status = ?, updated_at = CURRENT_TIMESTAMP 
                    WHERE id = ?
                    """,
                    (status, application_id)
                )
            
            conn.commit()
            self.logger.info(f"Updated application ID {application_id} status to: {status}")
            return True
            
        except Exception as e:
            conn.rollback()
            self.logger.error(f"Error updating application status: {str(e)}")
            raise
    
    async def update_application(self, application_id: int, application_data: Dict[str, Any]) -> bool:
        """
        Update application data
        
        Args:
            application_id: Application ID
            application_data: New application data
            
        Returns:
            True if updated, False if not found
        """
        try:
            conn = self._get_connection()
            cursor = conn.cursor()
            
            # Check if application exists
            cursor.execute(
                "SELECT id FROM applications WHERE id = ?",
                (application_id,)
            )
            if not cursor.fetchone():
                return False
            
            # Extract fields to update
            status = application_data.get("application_status", application_data.get("status"))
            notes = application_data.get("notes")
            platform_application_id = application_data.get("platform_application_id")
            
            # Build update query dynamically
            update_parts = []
            params = []
            
            if status:
                update_parts.append("status = ?")
                params.append(status)
                
            if notes is not None:  # Allow empty notes
                update_parts.append("notes = ?")
                params.append(notes)
                
            if platform_application_id:
                update_parts.append("platform_application_id = ?")
                params.append(platform_application_id)
            
            # Add updated_at timestamp
            update_parts.append("updated_at = CURRENT_TIMESTAMP")
            
            # Only proceed if we have something to update
            if update_parts:
                query = f"""
                    UPDATE applications 
                    SET {", ".join(update_parts)}
                    WHERE id = ?
                """
                params.append(application_id)
                
                cursor.execute(query, params)
                conn.commit()
                
                self.logger.info(f"Updated application ID {application_id}")
                return True
            else:
                self.logger.warning(f"No fields to update for application ID {application_id}")
                return False
            
        except Exception as e:
            conn.rollback()
            self.logger.error(f"Error updating application: {str(e)}")
            raise
    
    async def delete_application(self, application_id: int) -> bool:
        """
        Delete application by ID
        
        Args:
            application_id: Application ID
            
        Returns:
            True if deleted, False if not found
        """
        try:
            conn = self._get_connection()
            cursor = conn.cursor()
            
            # Check if application exists
            cursor.execute(
                "SELECT id FROM applications WHERE id = ?",
                (application_id,)
            )
            if not cursor.fetchone():
                return False
            
            # Delete application
            cursor.execute("DELETE FROM applications WHERE id = ?", (application_id,))
            
            conn.commit()
            self.logger.info(f"Deleted application ID: {application_id}")
            return True
            
        except Exception as e:
            conn.rollback()
            self.logger.error(f"Error deleting application: {str(e)}")
            raise
    
    async def get_application_stats(self) -> Dict[str, Any]:
        """
        Get application statistics
        
        Returns:
            Dictionary with application statistics
        """
        try:
            conn = self._get_connection()
            cursor = conn.cursor()
            
            stats = {
                "total_applications": 0,
                "by_status": {},
                "by_platform": {},
                "by_date": {},
                "recent_applications": []
            }
            
            # Get total applications
            cursor.execute("SELECT COUNT(*) as count FROM applications")
            stats["total_applications"] = cursor.fetchone()["count"]
            
            # Get applications by status
            cursor.execute(
                """
                SELECT status, COUNT(*) as count 
                FROM applications 
                GROUP BY status
                """
            )
            for row in cursor.fetchall():
                stats["by_status"][row["status"]] = row["count"]
            
            # Get applications by platform
            cursor.execute(
                """
                SELECT platform, COUNT(*) as count 
                FROM applications 
                GROUP BY platform
                """
            )
            for row in cursor.fetchall():
                stats["by_platform"][row["platform"] or "unknown"] = row["count"]
            
            # Get applications by date (last 30 days)
            cursor.execute(
                """
                SELECT DATE(created_at) as date, COUNT(*) as count 
                FROM applications 
                WHERE created_at >= DATE('now', '-30 days')
                GROUP BY DATE(created_at)
                ORDER BY date
                """
            )
            for row in cursor.fetchall():
                stats["by_date"][row["date"]] = row["count"]
            
            # Get recent applications
            cursor.execute(
                """
                SELECT a.id, a.status, a.created_at, j.title, j.company
                FROM applications a
                LEFT JOIN jobs j ON a.job_id = j.id
                ORDER BY a.created_at DESC
                LIMIT 10
                """
            )
            stats["recent_applications"] = cursor.fetchall()
            
            return stats
            
        except Exception as e:
            self.logger.error(f"Error getting application stats: {str(e)}")
            raise
