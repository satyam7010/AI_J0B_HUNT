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

from ..utils.logger import setup_logger
from ..config.settings import settings

logger = setup_logger(__name__)

class DatabaseManager:
    """Database management service"""
    
    def __init__(self, db_path: Optional[str] = None):
        """Initialize database manager"""
        self.logger = logger
        self.db_path = db_path or settings.DATABASE_URL or "job_applications.db"
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
            
            # Create search_criteria table
            cursor.execute('''
            CREATE TABLE IF NOT EXISTS search_criteria (
                id INTEGER PRIMARY KEY,
                job_titles TEXT NOT NULL,
                skills TEXT NOT NULL,
                locations TEXT,
                experience_level TEXT,
                job_type TEXT,
                salary_min INTEGER,
                salary_max INTEGER,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
            ''')
            
            # Create application_activities table
            cursor.execute('''
            CREATE TABLE IF NOT EXISTS application_activities (
                id INTEGER PRIMARY KEY,
                application_id INTEGER NOT NULL,
                activity_type TEXT NOT NULL,
                timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                details TEXT,
                FOREIGN KEY (application_id) REFERENCES applications (id)
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
            self.connection.row_factory = sqlite3.Row
        return self.connection
    
    def close(self):
        """Close the database connection"""
        if self.connection:
            self.connection.close()
            self.connection = None
    
    async def save_resume(self, parsed_data: Dict[str, Any], file_path: Optional[str] = None) -> int:
        """
        Save a parsed resume to the database
        
        Args:
            parsed_data: Parsed resume data
            file_path: Path to the original resume file
            
        Returns:
            int: Resume ID
        """
        try:
            conn = self._get_connection()
            cursor = conn.cursor()
            
            name = parsed_data.get('name', 'Unknown')
            content = json.dumps(parsed_data)
            
            cursor.execute(
                '''
                INSERT INTO resumes (name, content, parsed_data, file_path)
                VALUES (?, ?, ?, ?)
                ''',
                (name, content, json.dumps(parsed_data), file_path)
            )
            
            conn.commit()
            resume_id = cursor.lastrowid
            
            self.logger.info(f"Resume saved to database: {name} (ID: {resume_id})")
            return resume_id
            
        except Exception as e:
            self.logger.error(f"Error saving resume: {str(e)}")
            raise
    
    async def save_job(self, job_data: Dict[str, Any]) -> int:
        """
        Save a job posting to the database
        
        Args:
            job_data: Job posting data
            
        Returns:
            int: Job ID
        """
        try:
            conn = self._get_connection()
            cursor = conn.cursor()
            
            cursor.execute(
                '''
                INSERT INTO jobs (
                    title, company, location, description, url,
                    salary_range, job_type, experience_level, remote_status, platform
                )
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                ''',
                (
                    job_data.get('title', 'Unknown'),
                    job_data.get('company'),
                    job_data.get('location'),
                    job_data.get('description', ''),
                    job_data.get('url'),
                    job_data.get('salary_range'),
                    job_data.get('job_type'),
                    job_data.get('experience_level'),
                    job_data.get('remote_status'),
                    job_data.get('platform')
                )
            )
            
            conn.commit()
            job_id = cursor.lastrowid
            
            self.logger.info(f"Job saved to database: {job_data.get('title')} (ID: {job_id})")
            return job_id
            
        except Exception as e:
            self.logger.error(f"Error saving job: {str(e)}")
            raise
    
    async def save_application(self, application_data: Dict[str, Any]) -> int:
        """
        Save a job application to the database
        
        Args:
            application_data: Application data
            
        Returns:
            int: Application ID
        """
        try:
            conn = self._get_connection()
            cursor = conn.cursor()
            
            cursor.execute(
                '''
                INSERT INTO applications (
                    job_id, resume_id, optimized_resume_id, cover_letter_id,
                    status, notes, platform, platform_application_id
                )
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)
                ''',
                (
                    application_data.get('job_id'),
                    application_data.get('resume_id'),
                    application_data.get('optimized_resume_id'),
                    application_data.get('cover_letter_id'),
                    application_data.get('status', 'pending'),
                    application_data.get('notes'),
                    application_data.get('platform'),
                    application_data.get('platform_application_id')
                )
            )
            
            conn.commit()
            application_id = cursor.lastrowid
            
            # Add activity for creation
            await self.add_application_activity(
                application_id=application_id,
                activity_type="created",
                details={"status": application_data.get('status', 'pending')}
            )
            
            self.logger.info(f"Application saved to database (ID: {application_id})")
            return application_id
            
        except Exception as e:
            self.logger.error(f"Error saving application: {str(e)}")
            raise
    
    async def save_search_criteria(self, criteria: Dict[str, Any]) -> int:
        """
        Save job search criteria to the database
        
        Args:
            criteria: Search criteria
            
        Returns:
            int: Criteria ID
        """
        try:
            conn = self._get_connection()
            cursor = conn.cursor()
            
            cursor.execute(
                '''
                INSERT INTO search_criteria (
                    job_titles, skills, locations, experience_level,
                    job_type, salary_min, salary_max
                )
                VALUES (?, ?, ?, ?, ?, ?, ?)
                ''',
                (
                    json.dumps(criteria.get('job_titles', [])),
                    json.dumps(criteria.get('skills', [])),
                    json.dumps(criteria.get('locations', [])),
                    criteria.get('experience_level'),
                    criteria.get('job_type'),
                    criteria.get('salary_min'),
                    criteria.get('salary_max')
                )
            )
            
            conn.commit()
            criteria_id = cursor.lastrowid
            
            self.logger.info(f"Search criteria saved to database (ID: {criteria_id})")
            return criteria_id
            
        except Exception as e:
            self.logger.error(f"Error saving search criteria: {str(e)}")
            raise
    
    async def add_application_activity(self, application_id: int, activity_type: str, details: Dict[str, Any]) -> int:
        """
        Add an activity to an application
        
        Args:
            application_id: Application ID
            activity_type: Type of activity (e.g., "status_change", "note_added")
            details: Activity details
            
        Returns:
            int: Activity ID
        """
        try:
            conn = self._get_connection()
            cursor = conn.cursor()
            
            cursor.execute(
                '''
                INSERT INTO application_activities (
                    application_id, activity_type, details
                )
                VALUES (?, ?, ?)
                ''',
                (
                    application_id,
                    activity_type,
                    json.dumps(details)
                )
            )
            
            conn.commit()
            activity_id = cursor.lastrowid
            
            self.logger.info(f"Activity added to application {application_id}: {activity_type}")
            return activity_id
            
        except Exception as e:
            self.logger.error(f"Error adding application activity: {str(e)}")
            raise
    
    async def get_search_criteria(self, criteria_id: Optional[int] = None) -> Dict[str, Any]:
        """
        Get job search criteria from the database
        
        Args:
            criteria_id: Criteria ID (optional, gets the most recent if not provided)
            
        Returns:
            Dict: Search criteria
        """
        try:
            conn = self._get_connection()
            cursor = conn.cursor()
            
            if criteria_id:
                cursor.execute("SELECT * FROM search_criteria WHERE id = ?", (criteria_id,))
            else:
                cursor.execute("SELECT * FROM search_criteria ORDER BY created_at DESC LIMIT 1")
            
            row = cursor.fetchone()
            
            if row:
                return {
                    'id': row['id'],
                    'job_titles': json.loads(row['job_titles']),
                    'skills': json.loads(row['skills']),
                    'locations': json.loads(row['locations']) if row['locations'] else [],
                    'experience_level': row['experience_level'],
                    'job_type': row['job_type'],
                    'salary_min': row['salary_min'],
                    'salary_max': row['salary_max'],
                    'created_at': row['created_at']
                }
            
            return {
                'job_titles': [],
                'skills': [],
                'locations': [],
                'experience_level': None,
                'job_type': None,
                'salary_min': None,
                'salary_max': None
            }
            
        except Exception as e:
            self.logger.error(f"Error getting search criteria: {str(e)}")
            raise
    
    async def get_application_stats(self) -> Dict[str, Any]:
        """
        Get application statistics
        
        Returns:
            Dict: Application statistics
        """
        try:
            conn = self._get_connection()
            cursor = conn.cursor()
            
            # Total applications
            cursor.execute("SELECT COUNT(*) as count FROM applications")
            total_count = cursor.fetchone()['count']
            
            # Status counts
            cursor.execute(
                """
                SELECT status, COUNT(*) as count
                FROM applications
                GROUP BY status
                """
            )
            status_counts = {row['status']: row['count'] for row in cursor.fetchall()}
            
            # Recent activity
            cursor.execute(
                """
                SELECT a.activity_type, a.timestamp, app.status, j.title, j.company
                FROM application_activities a
                JOIN applications app ON a.application_id = app.id
                JOIN jobs j ON app.job_id = j.id
                ORDER BY a.timestamp DESC
                LIMIT 5
                """
            )
            recent_activity = [
                {
                    'activity_type': row['activity_type'],
                    'timestamp': row['timestamp'],
                    'status': row['status'],
                    'job_title': row['title'],
                    'company': row['company']
                }
                for row in cursor.fetchall()
            ]
            
            # Platform breakdown
            cursor.execute(
                """
                SELECT platform, COUNT(*) as count
                FROM applications
                WHERE platform IS NOT NULL
                GROUP BY platform
                """
            )
            platform_counts = {row['platform']: row['count'] for row in cursor.fetchall()}
            
            return {
                'total_applications': total_count,
                'status_counts': status_counts,
                'recent_activity': recent_activity,
                'platform_counts': platform_counts
            }
            
        except Exception as e:
            self.logger.error(f"Error getting application stats: {str(e)}")
            # Return empty stats on error
            return {
                'total_applications': 0,
                'status_counts': {},
                'recent_activity': [],
                'platform_counts': {}
            }
    
    async def get_recent_applications(self, limit: int = 5) -> List[Dict[str, Any]]:
        """
        Get recent applications
        
        Args:
            limit: Maximum number of applications to return
            
        Returns:
            List[Dict]: Recent applications
        """
        try:
            conn = self._get_connection()
            cursor = conn.cursor()
            
            cursor.execute(
                """
                SELECT a.id, a.status, a.created_at, a.updated_at,
                       j.id as job_id, j.title as job_title, j.company, j.location
                FROM applications a
                JOIN jobs j ON a.job_id = j.id
                ORDER BY a.updated_at DESC
                LIMIT ?
                """,
                (limit,)
            )
            
            return [
                {
                    'id': row['id'],
                    'status': row['status'],
                    'created_at': row['created_at'],
                    'updated_at': row['updated_at'],
                    'job': {
                        'id': row['job_id'],
                        'title': row['job_title'],
                        'company': row['company'],
                        'location': row['location']
                    }
                }
                for row in cursor.fetchall()
            ]
            
        except Exception as e:
            self.logger.error(f"Error getting recent applications: {str(e)}")
            return []
    
    async def get_skills_analysis(self) -> Dict[str, Any]:
        """
        Get skills analysis
        
        Returns:
            Dict: Skills analysis data
        """
        # In a real implementation, this would analyze the skills from jobs and resumes
        # For now, return mock data
        return {
            'most_requested_skills': [
                {'skill': 'Python', 'count': 15},
                {'skill': 'React', 'count': 12},
                {'skill': 'JavaScript', 'count': 10},
                {'skill': 'AWS', 'count': 8},
                {'skill': 'SQL', 'count': 7}
            ],
            'skill_gap_analysis': [
                {'skill': 'Docker', 'demand': 8, 'your_level': 'None'},
                {'skill': 'Kubernetes', 'demand': 6, 'your_level': 'Beginner'},
                {'skill': 'TypeScript', 'demand': 9, 'your_level': 'Beginner'}
            ],
            'skill_match_rate': 75  # Percentage of your skills matching job requirements
        }
    
    async def get_job_trends(self) -> Dict[str, Any]:
        """
        Get job market trends
        
        Returns:
            Dict: Job trends data
        """
        # In a real implementation, this would analyze job trends from the database
        # For now, return mock data
        return {
            'trending_titles': [
                {'title': 'Full Stack Developer', 'count': 25},
                {'title': 'Data Engineer', 'count': 18},
                {'title': 'DevOps Engineer', 'count': 15},
                {'title': 'ML Engineer', 'count': 12},
                {'title': 'Cloud Architect', 'count': 10}
            ],
            'salary_ranges': {
                'entry': '$70,000 - $90,000',
                'mid': '$90,000 - $120,000',
                'senior': '$120,000 - $160,000'
            },
            'remote_vs_onsite': {
                'remote': 45,
                'hybrid': 40,
                'onsite': 15
            }
        }
    
    async def get_pending_actions(self) -> List[Dict[str, Any]]:
        """
        Get pending actions that require user attention
        
        Returns:
            List[Dict]: Pending actions
        """
        try:
            conn = self._get_connection()
            cursor = conn.cursor()
            
            # Get pending applications that need review
            cursor.execute(
                """
                SELECT a.id, a.status, a.created_at,
                       j.title as job_title, j.company
                FROM applications a
                JOIN jobs j ON a.job_id = j.id
                WHERE a.status = 'pending'
                ORDER BY a.created_at DESC
                LIMIT 5
                """
            )
            
            pending_applications = [
                {
                    'type': 'application_review',
                    'id': row['id'],
                    'job_title': row['job_title'],
                    'company': row['company'],
                    'created_at': row['created_at'],
                    'message': f"Review application for {row['job_title']} at {row['company']}"
                }
                for row in cursor.fetchall()
            ]
            
            # In a real implementation, you would add other types of pending actions
            # For now, just return the pending applications
            return pending_applications
            
        except Exception as e:
            self.logger.error(f"Error getting pending actions: {str(e)}")
            return []
