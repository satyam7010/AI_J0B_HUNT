"""
AI Job Hunt - Unified Runner
This script provides a unified interface to run different components of the system.
"""

import os
import sys
import argparse
import asyncio
import subprocess
import webbrowser
import time
import threading
from pathlib import Path

# Add project root to Python path
sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))

def run_backend():
    """Run the backend API server"""
    print("Starting AI Job Hunt Backend Server...")
    print("API will be available at http://localhost:8000")
    print("API documentation will be available at http://localhost:8000/docs")
    
    # Open browser after a short delay
    threading.Thread(target=lambda: [time.sleep(2), webbrowser.open("http://localhost:8000/docs")]).start()
    
    # Run the backend
    subprocess.run(
        [sys.executable, "-m", "uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"],
        cwd=os.path.dirname(__file__),  # Run from the backend directory
        check=True
    )

def check_backend_running():
    """Check if the backend API is running"""
    import requests
    try:
        response = requests.get("http://localhost:8000/api")
        return True
    except:
        return False

def run_dashboard():
    """Run the Streamlit dashboard"""
    # Adjust import path for the relocated dashboard
    dashboard_script = os.path.join(os.path.dirname(os.path.dirname(__file__)), "frontend", "dashboard.py")
    
    print("Starting AI Job Hunt Dashboard...")
    
    # Check if backend is running
    if not check_backend_running():
        print("Backend API is not running. Starting it now...")
        # Start backend in a separate thread
        threading.Thread(target=run_backend).start()
        time.sleep(3)  # Give backend time to start
    
    print("Dashboard will be available at http://localhost:8501")
    
    # Run Streamlit
    import streamlit.web.cli as stcli
    dashboard_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), "frontend", "dashboard.py")
    sys.argv = ["streamlit", "run", str(dashboard_path), "--server.port=8501"]
    stcli.main()

def run_tests():
    """Run the test suite"""
    print("Running AI Job Hunt Tests...")
    subprocess.run(
        [sys.executable, "-m", "pytest", "tests"],
        cwd=os.path.dirname(__file__),  # Run from the backend directory
        check=True
    )

def run_automation():
    """Run the automation workflow"""
    print("Starting AI Job Hunt Automation...")
    # Import and run main automation function
    from services.application_engine import ApplicationEngine
    
    async def run():
        engine = ApplicationEngine()
        await engine.run_automation()
    
    asyncio.run(run())

def main():
    """Main entry point"""
    parser = argparse.ArgumentParser(description="AI Job Hunt - Unified Runner")
    parser.add_argument("component", choices=["backend", "dashboard", "tests", "automation", "all"],
                        help="Component to run")
    
    args = parser.parse_args()
    
    if args.component == "backend":
        run_backend()
    elif args.component == "dashboard":
        run_dashboard()
    elif args.component == "tests":
        run_tests()
    elif args.component == "automation":
        run_automation()
    elif args.component == "all":
        print("Running backend and dashboard...")
        backend_thread = threading.Thread(target=run_backend)
        backend_thread.daemon = True
        backend_thread.start()
        
        time.sleep(3)  # Give backend time to start
        run_dashboard()

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\nShutting down. Goodbye!")
        sys.exit(0)
