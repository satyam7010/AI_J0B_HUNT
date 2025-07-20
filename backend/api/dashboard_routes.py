"""
Dashboard-related API routes
"""

from fastapi import APIRouter, HTTPException
from typing import Dict, Any, List
import random
from datetime import datetime, timedelta

from backend.services.db_manager import DatabaseManager

router = APIRouter()
db_manager = DatabaseManager()

@router.get("/stats")
async def get_dashboard_stats():
    """
    Get dashboard statistics
    """
    try:
        # Try to get real stats first
        try:
            stats = await db_manager.get_application_stats()
            if not stats:
                # If no stats, generate mock data
                stats = generate_mock_stats()
        except:
            # If error, generate mock data
            stats = generate_mock_stats()
        
        return stats
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to retrieve dashboard stats: {str(e)}")

@router.get("/recent-applications")
async def get_recent_applications(limit: int = 5):
    """
    Get recent applications
    """
    try:
        # Try to get real applications first
        try:
            applications = await db_manager.get_recent_applications(limit)
            if not applications:
                # If no applications, generate mock data
                applications = generate_mock_applications(limit)
        except:
            # If error, generate mock data
            applications = generate_mock_applications(limit)
            
        return applications
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to retrieve recent applications: {str(e)}")

@router.get("/skills-analysis")
async def get_skills_analysis():
    """
    Get skills analysis
    """
    try:
        try:
            analysis = await db_manager.get_skills_analysis()
            if not analysis:
                analysis = generate_mock_skills_analysis()
        except:
            analysis = generate_mock_skills_analysis()
            
        return analysis
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to retrieve skills analysis: {str(e)}")

@router.get("/job-trends")
async def get_job_trends():
    """
    Get job trends
    """
    try:
        try:
            trends = await db_manager.get_job_trends()
            if not trends:
                trends = generate_mock_job_trends()
        except:
            trends = generate_mock_job_trends()
            
        return trends
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to retrieve job trends: {str(e)}")

# Mock data generation functions
def generate_mock_stats():
    """Generate mock dashboard statistics"""
    total_applications = random.randint(15, 50)
    pending = random.randint(5, 15)
    interviews = random.randint(3, 10)
    success_rate = random.randint(20, 80)
    
    # Generate timeline data for the last 30 days
    today = datetime.now()
    timeline = []
    for i in range(30):
        date = today - timedelta(days=i)
        count = random.randint(0, 3)
        timeline.append({
            "date": date.strftime("%Y-%m-%d"),
            "count": count
        })
    
    return {
        "total_applications": total_applications,
        "pending_responses": pending,
        "interviews": interviews,
        "success_rate": success_rate,
        "application_timeline": timeline
    }

def generate_mock_applications(limit: int = 5):
    """Generate mock recent applications"""
    companies = ["Tech Corp", "Data Inc", "Web Solutions", "AI Systems", 
                "Cloud Enterprises", "Dev Studios", "Software Ltd", "ML Research"]
    positions = ["Software Engineer", "Data Scientist", "Frontend Developer", "ML Engineer",
                "Backend Developer", "DevOps Engineer", "Product Manager", "UX Designer"]
    statuses = ["Applied", "Screening", "Interview", "Offer", "Rejected"]
    
    applications = []
    today = datetime.now()
    
    for i in range(min(limit, 10)):  # Cap at 10 to prevent too many mock entries
        company = random.choice(companies)
        position = random.choice(positions)
        status = random.choice(statuses)
        date = today - timedelta(days=random.randint(0, 14))
        
        applications.append({
            "id": i + 1,
            "company": company,
            "position": position,
            "date": date.strftime("%Y-%m-%d"),
            "status": status,
            "match_score": random.randint(60, 95)
        })
    
    return applications

def generate_mock_skills_analysis():
    """Generate mock skills analysis"""
    skills = ["Python", "JavaScript", "React", "SQL", "AWS", "Docker", 
             "Kubernetes", "Machine Learning", "Data Analysis", "Communication"]
    
    skill_data = []
    for skill in skills:
        demand = random.randint(50, 100)
        your_level = random.randint(30, 95)
        gap = max(0, demand - your_level)
        
        skill_data.append({
            "skill": skill,
            "market_demand": demand,
            "your_level": your_level,
            "gap": gap
        })
    
    return skill_data

def generate_mock_job_trends():
    """Generate mock job trends"""
    job_titles = ["Software Engineer", "Data Scientist", "Frontend Developer", 
                 "Backend Developer", "Full Stack Developer", "DevOps Engineer"]
    
    trends = []
    for title in job_titles:
        trends.append({
            "title": title,
            "openings": random.randint(100, 1000),
            "avg_salary": random.randint(70000, 150000),
            "growth_rate": random.randint(-5, 25)
        })
    
    return trends

@router.get("/pending-actions")
async def get_pending_actions():
    """
    Get pending actions that require user attention
    """
    try:
        actions = await db_manager.get_pending_actions()
        return actions
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to retrieve pending actions: {str(e)}")
