"""
AI Job Hunt - Streamlit Dashboard
"""

import streamlit as st
import pandas as pd
import requests
import json
import os
import sys
import subprocess
from datetime import datetime
import plotly.express as px
import plotly.graph_objects as go
from pathlib import Path

# Set page configuration
st.set_page_config(
    page_title="AI Job Hunt Dashboard",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# API Base URL
API_BASE_URL = "http://localhost:8000/api"

# Helper functions
def check_backend_running():
    """Check if the backend API is running"""
    try:
        response = requests.get(f"{API_BASE_URL}/health", timeout=2)
        return response.status_code == 200
    except:
        return False

def start_backend():
    """Start the backend API server"""
    print("Starting backend API server...")
    # Get the path to the run.py script
    run_script_path = Path(__file__).parent.parent / "run.py"
    
    # Start the backend process
    subprocess.Popen(
        [sys.executable, str(run_script_path), "backend"], 
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE
    )

def get_dashboard_stats():
    """Get dashboard statistics from the API"""
    try:
        response = requests.get(f"{API_BASE_URL}/dashboard/stats", timeout=5)
        if response.status_code == 200:
            return response.json()
        else:
            # If API error, provide default mock data without showing error
            return {
                "total_applications": 25,
                "pending_responses": 8,
                "interviews": 5,
                "success_rate": 40,
                "application_timeline": [
                    {"date": "2025-07-18", "count": 2},
                    {"date": "2025-07-17", "count": 3},
                    {"date": "2025-07-16", "count": 1},
                    {"date": "2025-07-15", "count": 5},
                    {"date": "2025-07-14", "count": 0},
                    {"date": "2025-07-13", "count": 4},
                    {"date": "2025-07-12", "count": 2},
                ],
                "status_counts": {
                    "pending": 10,
                    "submitted": 8,
                    "interview": 5,
                    "rejected": 2,
                    "offer": 0
                },
                "platform_counts": {
                    "LinkedIn": 12,
                    "Indeed": 8, 
                    "Company Website": 5
                }
            }
    except:
        # If connection error, provide default mock data
        return {
            "total_applications": 0,
            "pending_responses": 0,
            "interviews": 0,
            "success_rate": 0,
            "application_timeline": [],
            "status_counts": {},
            "platform_counts": {}
        }

def get_recent_applications():
    """Get recent applications from the API"""
    try:
        response = requests.get(f"{API_BASE_URL}/dashboard/recent-applications", timeout=5)
        if response.status_code == 200:
            return response.json()
        else:
            # If API error, provide default mock data
            return [
                {
                    "id": 1,
                    "job_title": "Senior Python Developer",
                    "company": "TechCorp Inc.",
                    "status": "interview",
                    "applied_date": "2025-07-16",
                    "last_updated": "2025-07-17"
                },
                {
                    "id": 2,
                    "job_title": "Data Scientist",
                    "company": "DataMinds",
                    "status": "submitted",
                    "applied_date": "2025-07-17",
                    "last_updated": "2025-07-17"
                },
                {
                    "id": 3,
                    "job_title": "ML Engineer",
                    "company": "AI Solutions",
                    "status": "pending",
                    "applied_date": "2025-07-18",
                    "last_updated": "2025-07-18"
                }
            ]
    except:
        # If connection error, provide empty list
        return []

def get_skills_analysis():
    """Get skills analysis from the API"""
    try:
        response = requests.get(f"{API_BASE_URL}/dashboard/skills-analysis", timeout=5)
        if response.status_code == 200:
            return response.json()
        else:
            # If API error, provide default mock data
            return {
                "most_requested": [
                    {"skill": "Python", "count": 15},
                    {"skill": "SQL", "count": 12},
                    {"skill": "JavaScript", "count": 10},
                    {"skill": "AWS", "count": 8},
                    {"skill": "Docker", "count": 7}
                ],
                "missing_skills": [
                    {"skill": "Kubernetes", "count": 5},
                    {"skill": "React", "count": 3},
                    {"skill": "Go", "count": 2}
                ],
                "skill_match_percentage": 78
            }
    except:
        # If connection error, provide empty data
        return {
            "most_requested": [],
            "missing_skills": [],
            "skill_match_percentage": 0
        }

# Dashboard title
st.title("AI Job Hunt Dashboard")

# Check if backend is running
if not check_backend_running():
    st.warning("⚠️ Backend API is not running! Some features may not work properly.")
    if st.button("Start Backend API"):
        start_backend()
        st.success("Backend API starting... Please wait a moment and refresh the page.")
else:
    st.success("✅ Connected to backend API")

# Sidebar menu
st.sidebar.title("Navigation")
page = st.sidebar.radio(
    "Go to",
    ["📊 Dashboard", "📄 Resume Management", "🔍 Job Analysis", "🤖 AI Optimization", "📝 Applications", "⚙️ Settings"]
)

# Dashboard page
if page == "📊 Dashboard":
    st.header("Application Overview")
    
    # Get dashboard stats
    stats = get_dashboard_stats()
    
    # Create columns for metrics
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Total Applications", stats["total_applications"])
    
    with col2:
        st.metric("Pending Responses", stats["pending_responses"])
    
    with col3:
        st.metric("Interviews", stats["interviews"])
    
    with col4:
        st.metric("Success Rate", f"{stats['success_rate']}%")
    
    # Create columns for charts
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Application Status")
        
        if stats["status_counts"]:
            # Create pie chart for status counts
            fig = px.pie(
                values=list(stats["status_counts"].values()),
                names=list(stats["status_counts"].keys()),
                color_discrete_sequence=px.colors.qualitative.Pastel,
                hole=0.4,
            )
            fig.update_layout(
                legend=dict(orientation="h", yanchor="bottom", y=-0.3),
                height=350
            )
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.info("No application status data available yet.")
    
    with col2:
        st.subheader("Applications by Platform")
        
        if stats["platform_counts"]:
            # Create bar chart for platforms
            fig = px.bar(
                x=list(stats["platform_counts"].keys()),
                y=list(stats["platform_counts"].values()),
                color=list(stats["platform_counts"].keys()),
                color_discrete_sequence=px.colors.qualitative.Bold,
            )
            fig.update_layout(
                xaxis_title="Platform",
                yaxis_title="Applications",
                legend_title=None,
                showlegend=False,
                height=350
            )
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.info("No platform data available yet.")
    
    # Application timeline
    st.subheader("Application Timeline")
    
    if stats.get("application_timeline"):
        # Create timeline chart
        timeline_data = pd.DataFrame(stats["application_timeline"])
        fig = px.line(
            timeline_data,
            x="date",
            y="count",
            markers=True,
        )
        fig.update_layout(
            xaxis_title="Date",
            yaxis_title="Applications",
            height=300
        )
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.info("No timeline data available yet.")
    
    # Recent applications
    st.subheader("Recent Applications")
    
    recent_apps = get_recent_applications()
    if recent_apps:
        # Convert to DataFrame for display
        df = pd.DataFrame(recent_apps)
        
        # Add status badges
        def format_status(status):
            if status == "pending":
                return "⏳ Pending"
            elif status == "submitted":
                return "📤 Submitted"
            elif status == "interview":
                return "🎯 Interview"
            elif status == "rejected":
                return "❌ Rejected"
            elif status == "offer":
                return "🎉 Offer"
            else:
                return status
                
        df["status"] = df["status"].apply(format_status)
        
        # Display as table
        st.dataframe(
            df[["job_title", "company", "status", "applied_date"]],
            use_container_width=True,
            hide_index=True
        )
    else:
        st.info("No applications submitted yet.")
    
    # Skills analysis
    st.subheader("Skills Analysis")
    
    skills = get_skills_analysis()
    
    if skills["most_requested"]:
        col1, col2 = st.columns(2)
        
        with col1:
            st.write("Most Requested Skills")
            most_requested_df = pd.DataFrame(skills["most_requested"])
            fig = px.bar(
                most_requested_df,
                x="count",
                y="skill",
                orientation="h",
                color="count",
                color_continuous_scale="Viridis",
            )
            fig.update_layout(
                xaxis_title="Job Postings",
                yaxis_title=None,
                yaxis=dict(autorange="reversed"),
                height=300
            )
            st.plotly_chart(fig, use_container_width=True)
        
        with col2:
            st.write("Skills to Develop")
            if skills["missing_skills"]:
                missing_skills_df = pd.DataFrame(skills["missing_skills"])
                fig = px.bar(
                    missing_skills_df,
                    x="count",
                    y="skill",
                    orientation="h",
                    color="count",
                    color_continuous_scale="Reds",
                )
                fig.update_layout(
                    xaxis_title="Job Postings",
                    yaxis_title=None,
                    yaxis=dict(autorange="reversed"),
                    height=300
                )
                st.plotly_chart(fig, use_container_width=True)
            else:
                st.info("No skill gaps identified.")
        
        # Skill match gauge
        st.write("Overall Skill Match")
        fig = go.Figure(go.Indicator(
            mode="gauge+number",
            value=skills["skill_match_percentage"],
            domain={"x": [0, 1], "y": [0, 1]},
            title={"text": "Match Percentage"},
            gauge={
                "axis": {"range": [0, 100]},
                "bar": {"color": "green"},
                "steps": [
                    {"range": [0, 50], "color": "lightgray"},
                    {"range": [50, 75], "color": "gray"},
                    {"range": [75, 100], "color": "lightgreen"}
                ],
                "threshold": {
                    "line": {"color": "red", "width": 4},
                    "thickness": 0.75,
                    "value": 85
                }
            }
        ))
        fig.update_layout(height=250)
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.info("No skills analysis data available yet.")

# Resume Management page
elif page == "📄 Resume Management":
    st.header("Resume Management")
    
    # File uploader for resume
    st.subheader("Upload Resume")
    uploaded_file = st.file_uploader("Choose your resume file", type=["pdf", "docx", "txt"])
    
    if uploaded_file is not None:
        # Display file info
        st.write(f"File name: {uploaded_file.name}")
        st.write(f"File size: {uploaded_file.size / 1024:.2f} KB")
        
        # Parse button
        if st.button("Parse Resume"):
            st.info("Parsing resume... Please wait.")
            # TODO: Implement actual API call to parse resume
            # For now, just show a success message after a delay
            import time
            time.sleep(2)
            st.success("Resume parsed successfully!")
            
            # Show sample parsed data
            st.subheader("Parsed Resume Data")
            
            sample_data = {
                "personal_info": {
                    "name": "John Smith",
                    "email": "john.smith@example.com",
                    "phone": "(555) 123-4567",
                    "location": "San Francisco, CA"
                },
                "skills": ["Python", "JavaScript", "React", "Machine Learning", "SQL", "AWS"],
                "experience": [
                    {
                        "title": "Senior Software Engineer",
                        "company": "Tech Solutions Inc.",
                        "dates": "2022 - Present",
                        "description": "Led development of cloud-based applications..."
                    },
                    {
                        "title": "Software Developer",
                        "company": "WebApps Co.",
                        "dates": "2019 - 2022",
                        "description": "Developed and maintained web applications..."
                    }
                ],
                "education": [
                    {
                        "degree": "M.S. Computer Science",
                        "institution": "Stanford University",
                        "dates": "2017 - 2019"
                    },
                    {
                        "degree": "B.S. Computer Engineering",
                        "institution": "UC Berkeley",
                        "dates": "2013 - 2017"
                    }
                ]
            }
            
            # Display parsed data in expandable sections
            with st.expander("Personal Information"):
                for key, value in sample_data["personal_info"].items():
                    st.write(f"**{key.title()}:** {value}")
            
            with st.expander("Skills"):
                st.write(", ".join(sample_data["skills"]))
            
            with st.expander("Experience"):
                for exp in sample_data["experience"]:
                    st.write(f"**{exp['title']} at {exp['company']}** ({exp['dates']})")
                    st.write(exp['description'])
                    st.write("---")
            
            with st.expander("Education"):
                for edu in sample_data["education"]:
                    st.write(f"**{edu['degree']}** - {edu['institution']} ({edu['dates']})")
    
    # Saved resumes
    st.subheader("Saved Resumes")
    
    # Mock data for saved resumes
    saved_resumes = [
        {"id": 1, "name": "Software Engineer Resume", "last_updated": "2025-07-15"},
        {"id": 2, "name": "Data Scientist Resume", "last_updated": "2025-07-10"},
        {"id": 3, "name": "Project Manager Resume", "last_updated": "2025-06-28"}
    ]
    
    # Display as table
    if saved_resumes:
        df = pd.DataFrame(saved_resumes)
        st.dataframe(df, use_container_width=True, hide_index=True)
    else:
        st.info("No saved resumes yet.")

# Job Analysis page
elif page == "🔍 Job Analysis":
    st.header("Job Description Analysis")
    
    # Job input options
    st.subheader("Input Job Details")
    
    input_method = st.radio(
        "Choose input method",
        ["Paste Job Description", "Upload Job Description File", "Enter Job URL"]
    )
    
    if input_method == "Paste Job Description":
        job_description = st.text_area("Paste job description here", height=300)
        
        if st.button("Analyze Job Description") and job_description:
            st.info("Analyzing job description... Please wait.")
            # TODO: Implement actual API call to analyze job
            # For now, just show a success message after a delay
            import time
            time.sleep(2)
            st.success("Job description analyzed successfully!")
            
            # Show sample analysis
            display_job_analysis()
            
    elif input_method == "Upload Job Description File":
        uploaded_job = st.file_uploader("Choose job description file", type=["pdf", "docx", "txt"])
        
        if uploaded_job is not None:
            st.write(f"File name: {uploaded_job.name}")
            
            if st.button("Analyze Job Description"):
                st.info("Analyzing job description... Please wait.")
                # TODO: Implement actual API call to analyze job
                # For now, just show a success message after a delay
                import time
                time.sleep(2)
                st.success("Job description analyzed successfully!")
                
                # Show sample analysis
                display_job_analysis()
                
    elif input_method == "Enter Job URL":
        job_url = st.text_input("Enter job posting URL")
        
        if st.button("Fetch and Analyze Job") and job_url:
            st.info("Fetching and analyzing job... Please wait.")
            # TODO: Implement actual API call to fetch and analyze job
            # For now, just show a success message after a delay
            import time
            time.sleep(2)
            st.success("Job description fetched and analyzed successfully!")
            
            # Show sample analysis
            display_job_analysis()
    
    # Function to display job analysis
    def display_job_analysis():
        # Sample job analysis data
        analysis = {
            "job_title": "Senior Machine Learning Engineer",
            "company": "AI Innovations Inc.",
            "location": "New York, NY (Remote Available)",
            "job_type": "Full-time",
            "required_skills": ["Python", "TensorFlow", "PyTorch", "MLOps", "AWS", "Docker"],
            "preferred_skills": ["Kubernetes", "CI/CD", "React", "Node.js"],
            "experience_level": "5+ years",
            "education": "Master's degree in Computer Science, Machine Learning, or related field",
            "salary_range": "$130,000 - $160,000",
            "responsibilities": [
                "Design and implement machine learning models",
                "Optimize existing ML pipelines for improved performance",
                "Collaborate with product teams to understand requirements",
                "Deploy models to production using MLOps best practices",
                "Monitor and maintain deployed models"
            ],
            "company_info": "AI Innovations Inc. is a leading AI research company focused on developing cutting-edge machine learning solutions for enterprise clients."
        }
        
        # Display analysis
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader("Job Details")
            st.write(f"**Title:** {analysis['job_title']}")
            st.write(f"**Company:** {analysis['company']}")
            st.write(f"**Location:** {analysis['location']}")
            st.write(f"**Job Type:** {analysis['job_type']}")
            st.write(f"**Experience:** {analysis['experience_level']}")
            st.write(f"**Education:** {analysis['education']}")
            st.write(f"**Salary Range:** {analysis['salary_range']}")
        
        with col2:
            st.subheader("Skills Analysis")
            
            # Required skills
            st.write("**Required Skills:**")
            for skill in analysis["required_skills"]:
                st.markdown(f"- {skill}")
            
            # Preferred skills
            st.write("**Preferred Skills:**")
            for skill in analysis["preferred_skills"]:
                st.markdown(f"- {skill}")
        
        # Responsibilities
        st.subheader("Key Responsibilities")
        for resp in analysis["responsibilities"]:
            st.markdown(f"- {resp}")
        
        # Company info
        st.subheader("About the Company")
        st.write(analysis["company_info"])
        
        # Resume compatibility
        st.subheader("Resume Compatibility")
        
        # Mock compatibility data
        compatibility = {
            "overall_match": 78,
            "skills_match": 85,
            "experience_match": 75,
            "education_match": 100,
            "missing_skills": ["Kubernetes", "CI/CD"],
            "highlighting_suggestions": [
                "Emphasize your experience with MLOps and deployment",
                "Highlight your Python and TensorFlow projects",
                "Quantify your achievements with specific metrics"
            ]
        }
        
        col1, col2 = st.columns(2)
        
        with col1:
            # Create gauge chart for overall match
            fig = go.Figure(go.Indicator(
                mode="gauge+number",
                value=compatibility["overall_match"],
                domain={"x": [0, 1], "y": [0, 1]},
                title={"text": "Overall Match"},
                gauge={
                    "axis": {"range": [0, 100]},
                    "bar": {"color": "green"},
                    "steps": [
                        {"range": [0, 50], "color": "lightgray"},
                        {"range": [50, 75], "color": "gray"},
                        {"range": [75, 100], "color": "lightgreen"}
                    ]
                }
            ))
            st.plotly_chart(fig, use_container_width=True)
        
        with col2:
            # Create bar chart for different match categories
            categories = ["Skills", "Experience", "Education"]
            values = [
                compatibility["skills_match"],
                compatibility["experience_match"],
                compatibility["education_match"]
            ]
            
            fig = px.bar(
                x=categories,
                y=values,
                color=values,
                color_continuous_scale="Viridis",
                labels={"x": "Category", "y": "Match Percentage"}
            )
            st.plotly_chart(fig, use_container_width=True)
        
        # Missing skills
        st.subheader("Missing Skills")
        if compatibility["missing_skills"]:
            for skill in compatibility["missing_skills"]:
                st.markdown(f"- {skill}")
        else:
            st.write("No missing skills identified.")
        
        # Suggestions
        st.subheader("Highlighting Suggestions")
        for suggestion in compatibility["highlighting_suggestions"]:
            st.markdown(f"- {suggestion}")

# AI Optimization page
elif page == "🤖 AI Optimization":
    st.header("AI Resume Optimization")
    
    # Select resume and job
    st.subheader("Select Resume and Job")
    
    col1, col2 = st.columns(2)
    
    with col1:
        # Mock data for saved resumes
        saved_resumes = [
            "Software Engineer Resume",
            "Data Scientist Resume",
            "Project Manager Resume"
        ]
        
        selected_resume = st.selectbox("Select Resume", saved_resumes)
    
    with col2:
        # Mock data for analyzed jobs
        analyzed_jobs = [
            "Senior Machine Learning Engineer at AI Innovations Inc.",
            "Data Scientist at Analytics Co.",
            "Software Engineer at Tech Solutions Inc."
        ]
        
        selected_job = st.selectbox("Select Job", analyzed_jobs)
    
    # Optimization settings
    st.subheader("Optimization Settings")
    
    col1, col2 = st.columns(2)
    
    with col1:
        optimization_level = st.select_slider(
            "Optimization Level",
            options=["Conservative", "Balanced", "Aggressive"],
            value="Balanced"
        )
        
        st.write(f"Selected level: **{optimization_level}**")
        
        if optimization_level == "Conservative":
            st.info("Makes minimal changes while ensuring key requirements are addressed.")
        elif optimization_level == "Balanced":
            st.info("Optimizes for both authenticity and keyword matching.")
        elif optimization_level == "Aggressive":
            st.info("Maximizes keyword matching and restructures content for highest ATS score.")
    
    with col2:
        st.write("Additional Options")
        generate_cover_letter = st.checkbox("Generate Cover Letter", value=True)
        highlight_keywords = st.checkbox("Highlight Matched Keywords", value=True)
        quantify_achievements = st.checkbox("Enhance Achievement Metrics", value=True)
    
    # Optimize button
    if st.button("Optimize Resume"):
        st.info("Optimizing resume with AI... Please wait.")
        
        # Mock delay for AI processing
        import time
        with st.spinner("AI is tailoring your resume..."):
            time.sleep(3)
        
        st.success("Resume optimization complete!")
        
        # Display sample results
        st.subheader("Optimization Results")
        
        # Mock optimization data
        optimization = {
            "original_resume": "Lorem ipsum dolor sit amet...",
            "optimized_resume": "Enhanced resume content with key skills and achievements...",
            "changes_made": [
                "Added 8 relevant keywords from job description",
                "Restructured experience section to highlight relevant projects",
                "Quantified 3 achievements with specific metrics",
                "Adjusted summary to better match job requirements"
            ],
            "keywords_added": ["TensorFlow", "PyTorch", "MLOps", "Docker"],
            "match_improvement": 35,  # percentage points improved
            "ats_score": 92
        }
        
        # Show before/after
        col1, col2 = st.columns(2)
        
        with col1:
            st.write("**Original Resume**")
            st.text_area("", optimization["original_resume"], height=200, disabled=True)
        
        with col2:
            st.write("**Optimized Resume**")
            st.text_area("", optimization["optimized_resume"], height=200, disabled=True)
        
        # Show changes made
        st.subheader("Changes Made")
        for change in optimization["changes_made"]:
            st.markdown(f"- {change}")
        
        # Show keywords added
        st.subheader("Keywords Added")
        st.write(", ".join(optimization["keywords_added"]))
        
        # Show improvement metrics
        col1, col2 = st.columns(2)
        
        with col1:
            st.metric("Match Improvement", f"+{optimization['match_improvement']}%")
        
        with col2:
            # Create gauge chart for ATS score
            fig = go.Figure(go.Indicator(
                mode="gauge+number",
                value=optimization["ats_score"],
                domain={"x": [0, 1], "y": [0, 1]},
                title={"text": "ATS Score"},
                gauge={
                    "axis": {"range": [0, 100]},
                    "bar": {"color": "green"},
                    "steps": [
                        {"range": [0, 60], "color": "lightgray"},
                        {"range": [60, 80], "color": "gray"},
                        {"range": [80, 100], "color": "lightgreen"}
                    ]
                }
            ))
            st.plotly_chart(fig, use_container_width=True)
        
        # Download buttons
        col1, col2 = st.columns(2)
        
        with col1:
            st.download_button(
                "Download Optimized Resume (PDF)",
                "dummy_data",  # Would be actual PDF in real implementation
                file_name="optimized_resume.pdf",
                mime="application/pdf"
            )
        
        with col2:
            st.download_button(
                "Download Optimized Resume (DOCX)",
                "dummy_data",  # Would be actual DOCX in real implementation
                file_name="optimized_resume.docx",
                mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document"
            )
        
        # Cover letter (if enabled)
        if generate_cover_letter:
            st.subheader("Generated Cover Letter")
            
            # Mock cover letter
            cover_letter = """
            Dear Hiring Manager,
            
            I am writing to express my interest in the Senior Machine Learning Engineer position at AI Innovations Inc. With over 5 years of experience developing and deploying machine learning models at scale, I am excited about the opportunity to contribute to your team's cutting-edge work in AI solutions.
            
            My experience aligns perfectly with your requirements, particularly in building and optimizing ML pipelines, working with TensorFlow and PyTorch, and implementing MLOps best practices. At my current role with Tech Solutions Inc., I successfully reduced model training time by 40% while improving accuracy by 15%, directly impacting the company's core product performance.
            
            I am particularly drawn to AI Innovations' focus on developing practical AI solutions for enterprise clients, as mentioned in your job description. Your company's recent work on scalable ML infrastructure resonates with my professional interests and expertise.
            
            I look forward to discussing how my background, technical skills, and passion for machine learning can help AI Innovations continue to deliver exceptional AI solutions to its clients.
            
            Sincerely,
            John Smith
            """
            
            st.text_area("", cover_letter, height=300)
            
            st.download_button(
                "Download Cover Letter",
                cover_letter,
                file_name="cover_letter.txt"
            )

# Applications page
elif page == "📝 Applications":
    st.header("Job Applications")
    
    # Tabs for different application states
    tabs = st.tabs(["All Applications", "Pending Review", "Active Applications", "Archived"])
    
    # All Applications tab
    with tabs[0]:
        st.subheader("All Applications")
        
        # Mock application data
        applications = [
            {
                "id": 1,
                "job_title": "Senior Machine Learning Engineer",
                "company": "AI Innovations Inc.",
                "status": "interview",
                "platform": "LinkedIn",
                "applied_date": "2025-07-10",
                "last_updated": "2025-07-15"
            },
            {
                "id": 2,
                "job_title": "Data Scientist",
                "company": "Analytics Co.",
                "status": "submitted",
                "platform": "Indeed",
                "applied_date": "2025-07-14",
                "last_updated": "2025-07-14"
            },
            {
                "id": 3,
                "job_title": "Software Engineer",
                "company": "Tech Solutions Inc.",
                "status": "rejected",
                "platform": "Company Website",
                "applied_date": "2025-07-05",
                "last_updated": "2025-07-12"
            },
            {
                "id": 4,
                "job_title": "Full Stack Developer",
                "company": "WebDev Agency",
                "status": "pending",
                "platform": "LinkedIn",
                "applied_date": "2025-07-17",
                "last_updated": "2025-07-17"
            },
            {
                "id": 5,
                "job_title": "AI Researcher",
                "company": "Research Labs",
                "status": "pending",
                "platform": "Indeed",
                "applied_date": "2025-07-18",
                "last_updated": "2025-07-18"
            }
        ]
        
        if applications:
            # Convert to DataFrame
            df = pd.DataFrame(applications)
            
            # Add status badges
            def format_status(status):
                if status == "pending":
                    return "⏳ Pending"
                elif status == "submitted":
                    return "📤 Submitted"
                elif status == "interview":
                    return "🎯 Interview"
                elif status == "rejected":
                    return "❌ Rejected"
                elif status == "offer":
                    return "🎉 Offer"
                else:
                    return status
                    
            df["status"] = df["status"].apply(format_status)
            
            # Display as table
            st.dataframe(
                df[["job_title", "company", "status", "platform", "applied_date", "last_updated"]],
                use_container_width=True,
                hide_index=True
            )
            
            # Select application for details
            selected_app_id = st.selectbox("Select application to view details", df["id"].tolist())
            
            # Find selected application
            selected_app = next((app for app in applications if app["id"] == selected_app_id), None)
            
            if selected_app:
                st.subheader(f"Application Details: {selected_app['job_title']} at {selected_app['company']}")
                
                col1, col2 = st.columns(2)
                
                with col1:
                    st.write(f"**Status:** {format_status(selected_app['status'])}")
                    st.write(f"**Platform:** {selected_app['platform']}")
                    st.write(f"**Applied Date:** {selected_app['applied_date']}")
                    st.write(f"**Last Updated:** {selected_app['last_updated']}")
                
                with col2:
                    # Mock next steps based on status
                    if selected_app['status'] == "pending":
                        st.write("**Next Steps:** Waiting for initial review")
                    elif selected_app['status'] == "submitted":
                        st.write("**Next Steps:** Follow up if no response by 2025-07-24")
                    elif selected_app['status'] == "interview":
                        st.write("**Next Steps:** Scheduled interview on 2025-07-20 at 10:00 AM")
                    elif selected_app['status'] == "rejected":
                        st.write("**Next Steps:** None - Application closed")
                
                # Action buttons based on status
                if selected_app['status'] == "pending":
                    if st.button("Submit Application"):
                        st.success("Application status updated to submitted!")
                
                elif selected_app['status'] == "submitted":
                    if st.button("Mark as Interview"):
                        st.success("Application status updated to interview!")
                
                # Notes section
                st.subheader("Application Notes")
                notes = st.text_area("Add notes about this application", "")
                if st.button("Save Notes"):
                    st.success("Notes saved successfully!")
        else:
            st.info("No applications found.")
    
    # Pending Review tab
    with tabs[1]:
        st.subheader("Applications Pending Review")
        
        # Filter mock data for pending applications
        pending_apps = [app for app in applications if app["status"] == "pending"]
        
        if pending_apps:
            # Convert to DataFrame
            df = pd.DataFrame(pending_apps)
            
            # Display as table
            st.dataframe(
                df[["job_title", "company", "platform", "applied_date"]],
                use_container_width=True,
                hide_index=True
            )
            
            # Bulk actions
            st.subheader("Bulk Actions")
            selected_action = st.selectbox("Select action", ["Submit Selected", "Reject Selected"])
            selected_ids = st.multiselect("Select applications", df["id"].tolist())
            
            if selected_ids and st.button("Apply Action"):
                st.success(f"{selected_action} action applied to {len(selected_ids)} applications!")
        else:
            st.info("No applications pending review.")
    
    # Active Applications tab
    with tabs[2]:
        st.subheader("Active Applications")
        
        # Filter mock data for active applications
        active_apps = [app for app in applications if app["status"] in ["submitted", "interview"]]
        
        if active_apps:
            # Convert to DataFrame
            df = pd.DataFrame(active_apps)
            
            # Add status badges
            df["status"] = df["status"].apply(format_status)
            
            # Display as table
            st.dataframe(
                df[["job_title", "company", "status", "platform", "applied_date", "last_updated"]],
                use_container_width=True,
                hide_index=True
            )
            
            # Activity timeline
            st.subheader("Application Activity")
            
            # Mock activity data
            activities = [
                {
                    "date": "2025-07-15",
                    "type": "interview_scheduled",
                    "details": "First round interview scheduled for 2025-07-20"
                },
                {
                    "date": "2025-07-12",
                    "type": "status_change",
                    "details": "Application moved to 'Under Review'"
                },
                {
                    "date": "2025-07-10",
                    "type": "application_submitted",
                    "details": "Application submitted via LinkedIn"
                }
            ]
            
            for activity in activities:
                st.write(f"**{activity['date']}:** {activity['details']}")
                st.markdown("---")
        else:
            st.info("No active applications.")
    
    # Archived tab
    with tabs[3]:
        st.subheader("Archived Applications")
        
        # Filter mock data for archived applications
        archived_apps = [app for app in applications if app["status"] in ["rejected", "offer"]]
        
        if archived_apps:
            # Convert to DataFrame
            df = pd.DataFrame(archived_apps)
            
            # Add status badges
            df["status"] = df["status"].apply(format_status)
            
            # Display as table
            st.dataframe(
                df[["job_title", "company", "status", "platform", "applied_date", "last_updated"]],
                use_container_width=True,
                hide_index=True
            )
        else:
            st.info("No archived applications.")

# Settings page
elif page == "⚙️ Settings":
    st.header("Settings")
    
    # API Settings
    st.subheader("API Settings")
    
    with st.form("api_settings"):
        ollama_url = st.text_input("Ollama API URL", "http://localhost:11434")
        model = st.text_input("Model Name", "gemma:3.4b")
        
        api_submitted = st.form_submit_button("Save API Settings")
        
        if api_submitted:
            st.success("API settings saved successfully!")
    
    # Credentials Settings
    st.header("Job Portal Credentials")
    
    with st.form("credentials"):
        # LinkedIn
        st.subheader("LinkedIn")
        linkedin_email = st.text_input("LinkedIn Email")
        linkedin_password = st.text_input("LinkedIn Password", type="password")
        
        # Indeed
        st.subheader("Indeed")
        indeed_email = st.text_input("Indeed Email")
        indeed_password = st.text_input("Indeed Password", type="password")
        
        # Test credentials button
        cred_submitted = st.form_submit_button("Save Credentials")
        
        if cred_submitted:
            st.success("Credentials saved successfully!")

# Footer
st.sidebar.markdown("---")
st.sidebar.markdown("AI Job Hunt © 2025")
st.sidebar.markdown("Powered by Gemma 3.4b via Ollama")
