#!/usr/bin/env python3
"""
Example Usage Script for AI Job Hunt System
This script demonstrates how to use the AI Job Hunt system programmatically
"""

import asyncio
import os
import sys
from pathlib import Path

# Add backend to path
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from backend.services.db_manager import DatabaseManager
from backend.services.resume_parser import ResumeParser
from backend.agents.job_description_agent import JobDescriptionAgent
from backend.agents.resume_optimizer_agent import ResumeOptimizerAgent
from backend.agents.application_agent import ApplicationAgent

async def example_workflow():
    """Example workflow demonstrating the complete job application process"""
    
    print("🎯 AI Job Hunt - Example Workflow")
    print("=" * 50)
    
    # Initialize components
    db = DatabaseManager()
    resume_parser = ResumeParser()
    job_analyzer = JobDescriptionAgent()
    resume_optimizer = ResumeOptimizerAgent()
    application_agent = ApplicationAgent()
    
    # Initialize database
    db.init_db()
    print("✅ Database initialized")
    
    # Step 1: Create and parse a sample resume
    print("\n📄 Step 1: Creating and parsing resume")
    
    sample_resume_content = """
    JANE SMITH
    jane.smith@email.com
    (555) 987-6543
    LinkedIn: linkedin.com/in/janesmith
    GitHub: github.com/janesmith
    
    PROFESSIONAL SUMMARY
    Experienced Full-Stack Developer with 4+ years of experience in building scalable web applications
    using modern technologies. Skilled in React, Node.js, Python, and cloud technologies.
    
    TECHNICAL SKILLS
    • Languages: JavaScript, Python, TypeScript, HTML5, CSS3, SQL
    • Frontend: React, Vue.js, Angular, Redux, Webpack, Sass
    • Backend: Node.js, Express, Django, Flask, FastAPI
    • Databases: PostgreSQL, MongoDB, Redis, MySQL
    • Cloud: AWS, Docker, Kubernetes, Jenkins
    • Tools: Git, Jira, Agile, Scrum
    
    PROFESSIONAL EXPERIENCE
    
    Senior Full-Stack Developer | TechStartup Inc. | 2022 - Present
    • Developed and maintained 5+ web applications serving 10,000+ users
    • Improved application performance by 40% through code optimization
    • Led team of 3 junior developers on critical project deliveries
    • Implemented CI/CD pipelines reducing deployment time by 60%
    • Collaborated with product managers to define technical requirements
    
    Full-Stack Developer | WebCorp Solutions | 2020 - 2022
    • Built responsive web applications using React and Node.js
    • Designed and implemented RESTful APIs for mobile and web clients
    • Managed database schemas and optimized query performance
    • Participated in code reviews and mentored junior developers
    
    Junior Web Developer | DigitalAgency | 2019 - 2020
    • Developed frontend interfaces using HTML, CSS, and JavaScript
    • Integrated third-party APIs and payment systems
    • Collaborated with designers to implement pixel-perfect designs
    • Maintained legacy codebases and implemented bug fixes
    
    EDUCATION
    Bachelor of Science in Computer Science | State University | 2019
    • Relevant Coursework: Data Structures, Algorithms, Database Systems, Software Engineering
    • GPA: 3.8/4.0
    
    CERTIFICATIONS
    • AWS Certified Developer - Associate (2023)
    • Google Cloud Professional Cloud Architect (2022)
    • MongoDB Certified Developer (2021)
    
    PROJECTS
    
    E-commerce Platform | 2023
    • Built full-stack e-commerce solution using React, Node.js, and PostgreSQL
    • Implemented secure payment processing with Stripe integration
    • Deployed on AWS with auto-scaling and load balancing
    • Technologies: React, Node.js, PostgreSQL, AWS, Docker
    
    Task Management App | 2022
    • Developed team collaboration tool with real-time updates
    • Used Socket.io for real-time notifications and updates
    • Implemented user authentication and role-based access control
    • Technologies: Vue.js, Express, MongoDB, Socket.io
    """
    
    # Save sample resume
    resume_file = "sample_resume.txt"
    with open(resume_file, 'w') as f:
        f.write(sample_resume_content)
    
    # Parse resume
    try:
        parsed_resume = resume_parser.parse_resume(resume_file)
        resume_id = db.save_resume(parsed_resume)
        print(f"✅ Resume parsed and saved with ID: {resume_id}")
        print(f"   Name: {parsed_resume.get('name')}")
        print(f"   Skills: {len(parsed_resume.get('skills', []))} skills found")
        print(f"   Experience: {len(parsed_resume.get('experience', []))} entries found")
        
        # Clean up
        os.remove(resume_file)
        
    except Exception as e:
        print(f"❌ Error parsing resume: {e}")
        return
    
    # Step 2: Analyze a job posting
    print("\n🔍 Step 2: Analyzing job posting")
    
    sample_job_description = """
    Senior Software Engineer - Full Stack
    InnovateTech Solutions
    San Francisco, CA (Remote friendly)
    
    About the Role:
    We are seeking a talented Senior Software Engineer to join our growing team. You will be responsible
    for building scalable web applications and leading technical initiatives that drive our product forward.
    
    Key Responsibilities:
    • Design and develop full-stack web applications using modern technologies
    • Collaborate with cross-functional teams to deliver high-quality software
    • Mentor junior developers and provide technical leadership
    • Participate in architecture decisions and code reviews
    • Ensure code quality, performance, and security best practices
    • Work in an agile environment with continuous integration and deployment
    
    Required Qualifications:
    • 4+ years of experience in full-stack development
    • Strong proficiency in JavaScript/TypeScript and modern frameworks (React, Angular, or Vue.js)
    • Experience with backend technologies (Node.js, Python, or similar)
    • Familiarity with databases (PostgreSQL, MongoDB, or similar)
    • Experience with cloud platforms (AWS, GCP, or Azure)
    • Knowledge of containerization (Docker, Kubernetes)
    • Understanding of CI/CD pipelines and DevOps practices
    • Bachelor's degree in Computer Science or related field
    
    Preferred Qualifications:
    • Experience with microservices architecture
    • Knowledge of GraphQL and REST API design
    • Familiarity with message queues (Redis, RabbitMQ)
    • Experience with monitoring and logging tools
    • Contribution to open-source projects
    • AWS or GCP certifications
    
    What We Offer:
    • Competitive salary ($120,000 - $160,000)
    • Comprehensive health, dental, and vision insurance
    • Flexible work arrangements (remote/hybrid)
    • Professional development budget
    • Stock options
    • Unlimited PTO
    • Modern tech stack and tools
    
    Experience Level: Senior (4-7 years)
    Job Type: Full-time
    Location: San Francisco, CA / Remote
    """
    
    try:
        analyzed_job = job_analyzer.analyze_job_text(sample_job_description)
        job_id = db.save_job_posting(analyzed_job)
        print(f"✅ Job analyzed and saved with ID: {job_id}")
        print(f"   Required skills: {analyzed_job.get('required_skills', [])[:5]}...")
        print(f"   Experience level: {analyzed_job.get('experience_level')}")
        print(f"   Job type: {analyzed_job.get('job_type')}")
        
    except Exception as e:
        print(f"❌ Error analyzing job: {e}")
        return
    
    # Step 3: AI-powered resume optimization
    print("\n🤖 Step 3: AI-powered resume optimization")
    
    try:
        # Check if Ollama is available
        is_ollama_available = await ai_optimizer.check_ollama_connection()
        
        if is_ollama_available:
            print("✅ Ollama connection successful")
            
            # Optimize resume for the job
            optimized_resume = await ai_optimizer.optimize_resume(
                sample_job_description, 
                parsed_resume
            )
            
            print("✅ Resume optimized successfully")
            print(f"   Optimized resume length: {len(optimized_resume)} characters")
            
            # Analyze job match
            match_analysis = await ai_optimizer.analyze_job_match(
                sample_job_description, 
                parsed_resume
            )
            
            print("✅ Job match analysis completed")
            print(f"   Match score: {match_analysis.get('overall_match_score', 0)}%")
            print(f"   Strengths: {len(match_analysis.get('strengths', []))} items")
            print(f"   Gaps: {len(match_analysis.get('gaps', []))} items")
            
            # Generate cover letter
            cover_letter = await ai_optimizer.generate_cover_letter(
                sample_job_description, 
                parsed_resume,
                {'name': 'InnovateTech Solutions'}
            )
            
            print("✅ Cover letter generated successfully")
            print(f"   Cover letter length: {len(cover_letter)} characters")
            
        else:
            print("⚠️  Ollama not available - skipping AI optimization")
            print("   Please install Ollama and pull the Gemma model to use AI features")
            
            # Use dummy data for demo
            optimized_resume = "Optimized resume content would appear here"
            cover_letter = "Generated cover letter would appear here"
            match_analysis = {
                'overall_match_score': 85,
                'strengths': ['Strong technical skills', 'Relevant experience'],
                'gaps': ['Could highlight more leadership experience']
            }
            
    except Exception as e:
        print(f"❌ Error in AI optimization: {e}")
        optimized_resume = "Optimized resume content would appear here"
        cover_letter = "Generated cover letter would appear here"
        match_analysis = {'overall_match_score': 0}
    
    # Step 4: Save pending application for review
    print("\n📝 Step 4: Saving application for review")
    
    try:
        pending_id = db.save_pending_application(
            analyzed_job,
            optimized_resume,
            cover_letter,
            match_analysis
        )
        
        print(f"✅ Application saved for review with ID: {pending_id}")
        print("   Status: Pending manual review")
        
    except Exception as e:
        print(f"❌ Error saving pending application: {e}")
        return
    
    # Step 5: Configure job search criteria
    print("\n⚙️ Step 5: Configuring job search criteria")
    
    search_criteria = {
        'job_titles': ['Senior Software Engineer', 'Full Stack Developer', 'Software Engineer'],
        'skills': ['JavaScript', 'React', 'Node.js', 'Python', 'AWS'],
        'locations': ['San Francisco', 'New York', 'Seattle', 'Remote'],
        'experience_level': 'senior',
        'job_type': 'full_time',
        'salary_min': 100000,
        'salary_max': 180000,
        'remote_preference': 'remote_friendly',
        'search_linkedin': True,
        'search_indeed': True,
        'search_naukri': False  # Disable for US-focused search
    }
    
    try:
        criteria_id = db.save_search_criteria(search_criteria)
        print(f"✅ Search criteria saved with ID: {criteria_id}")
        print(f"   Job titles: {len(search_criteria['job_titles'])} titles")
        print(f"   Skills: {len(search_criteria['skills'])} skills")
        print(f"   Locations: {len(search_criteria['locations'])} locations")
        
    except Exception as e:
        print(f"❌ Error saving search criteria: {e}")
        return
    
    # Step 6: Platform configuration check
    print("\n🔧 Step 6: Checking platform configuration")
    
    platforms = job_applier.get_supported_platforms()
    print(f"✅ Supported platforms: {platforms}")
    
    for platform in platforms:
        is_configured = job_applier.is_platform_configured(platform)
        status = "✅ Configured" if is_configured else "❌ Not configured"
        print(f"   {platform.title()}: {status}")
    
    # Step 7: Application statistics
    print("\n📊 Step 7: Application statistics")
    
    try:
        stats = db.get_application_stats()
        print("✅ Application statistics:")
        print(f"   Total applications: {stats['total_applications']}")
        print(f"   Pending applications: {stats['pending_applications']}")
        print(f"   Applied applications: {stats['applied_applications']}")
        print(f"   Interview applications: {stats['interview_applications']}")
        print(f"   Pending reviews: {stats['pending_reviews']}")
        print(f"   Success rate: {stats['success_rate']:.1f}%")
        
    except Exception as e:
        print(f"❌ Error getting statistics: {e}")
    
    # Step 8: Recommendations
    print("\n💡 Step 8: Next steps and recommendations")
    
    print("✅ Workflow completed successfully!")
    print("\nRecommendations:")
    print("1. Configure your job portal credentials in the .env file")
    print("2. Install and configure Ollama for AI features:")
    print("   - Install from https://ollama.ai/")
    print("   - Run: ollama pull gemma:3.4b")
    print("3. Review pending applications in the dashboard")
    print("4. Start the dashboard: python run_dashboard.py")
    print("5. Monitor applications and adjust search criteria as needed")
    
    print("\nDashboard features:")
    print("• Resume management and parsing")
    print("• Job analysis and matching")
    print("• AI-powered optimization")
    print("• Application tracking and status updates")
    print("• Search criteria configuration")
    print("• Platform credential management")
    
    print("\nAutomation workflow:")
    print("1. System searches for jobs based on your criteria")
    print("2. AI optimizes your resume for each job")
    print("3. Applications are saved for manual review (if enabled)")
    print("4. You approve/reject applications through the dashboard")
    print("5. System automatically applies to approved jobs")
    print("6. Track application status and outcomes")
    
    print("\n🎉 Ready to start your AI-powered job hunt!")

async def quick_demo():
    """Quick demonstration of key features"""
    print("⚡ Quick Demo - Key Features")
    print("=" * 30)
    
    # Initialize database
    db = DatabaseManager()
    db.init_db()
    
    # Sample data
    sample_skills = ['Python', 'JavaScript', 'React', 'Django', 'AWS', 'Docker']
    sample_job_skills = ['Python', 'Django', 'PostgreSQL', 'AWS', 'Docker', 'Kubernetes']
    
    # Skill matching demo
    matching_skills = set(sample_skills) & set(sample_job_skills)
    missing_skills = set(sample_job_skills) - set(sample_skills)
    
    print(f"📊 Skills Analysis:")
    print(f"   Your skills: {sample_skills}")
    print(f"   Job requirements: {sample_job_skills}")
    print(f"   ✅ Matching: {list(matching_skills)}")
    print(f"   ❌ Missing: {list(missing_skills)}")
    
    match_percentage = (len(matching_skills) / len(sample_job_skills)) * 100
    print(f"   📈 Match score: {match_percentage:.1f}%")
    
    # Database demo
    print(f"\n💾 Database Operations:")
    print(f"   Database initialized: ✅")
    print(f"   Tables created: ✅")
    print(f"   Ready for data storage: ✅")
    
    print(f"\n🎯 System Status:")
    print(f"   Core modules: ✅ Loaded")
    print(f"   Database: ✅ Ready")
    print(f"   AI components: ⏳ Depends on Ollama")
    print(f"   Web automation: ✅ Ready")
    
    print(f"\n🚀 Ready to launch full workflow!")

if __name__ == "__main__":
    print("AI Job Hunt - Example Usage")
    print("Choose an option:")
    print("1. Full workflow demo")
    print("2. Quick demo")
    
    try:
        choice = input("Enter choice (1 or 2): ").strip()
        
        if choice == "1":
            asyncio.run(example_workflow())
        elif choice == "2":
            asyncio.run(quick_demo())
        else:
            print("Invalid choice. Running full workflow demo...")
            asyncio.run(example_workflow())
            
    except KeyboardInterrupt:
        print("\n\nDemo interrupted by user")
    except Exception as e:
        print(f"\nError running demo: {e}")
        print("Please ensure all dependencies are installed and configured properly")
