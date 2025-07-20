"""
AI Job Hunt - Streamlit Dashboard Runner
"""

import os
import sys
import streamlit.web.cli as stcli
from pathlib import Path
import subprocess
import threading
import time
import webbrowser

def check_backend_running():
    """Check if the backend API is running"""
    import requests
    try:
        response = requests.get("http://localhost:8000/api")
        return True
    except:
        return False

def start_backend():
    """Start the backend API server"""
    print("Starting backend API server...")
    # Get the path to the backend run.py script
    backend_run_path = Path(__file__).parent.parent / "backend" / "run.py"
    
    # Start the backend process
    subprocess.Popen([sys.executable, str(backend_run_path), "backend"], 
                    stdout=subprocess.PIPE,
                    stderr=subprocess.PIPE)
    
    # Wait for the backend to start
    print("Waiting for backend API to start...")
    retries = 0
    while not check_backend_running() and retries < 10:
        time.sleep(1)
        retries += 1
    
    if retries >= 10:
        print("Warning: Backend API may not be running. Some dashboard features may not work.")
    else:
        print("Backend API started successfully!")

def open_browser():
    """Open browser after a delay to ensure dashboard is up"""
    time.sleep(2)  # Wait for dashboard to start
    print("Opening dashboard in browser...")
    webbrowser.open("http://localhost:8502")

def run_dashboard():
    """Run the Streamlit dashboard"""
    # Add the project root to the Python path
    sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))
    
    # Path to the dashboard script
    dashboard_script = Path(__file__).parent / "dashboard.py"
    
    if not dashboard_script.exists():
        print(f"Error: Dashboard script not found at {dashboard_script}")
        sys.exit(1)
    
    # Check if backend is running, start it if not
    if not check_backend_running():
        start_backend()
    
    print("Starting AI Job Hunt Dashboard...")
    print(f"Dashboard will be available at http://localhost:8502")
    
    # Open browser in a separate thread
    threading.Thread(target=open_browser).start()
    
    # Run Streamlit with the dashboard script
    sys.argv = ["streamlit", "run", str(dashboard_script), "--server.port=8502"]
    stcli.main()

if __name__ == "__main__":
    run_dashboard()
