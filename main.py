"""
AI Job Hunt - Main Launcher
"""
import os
import sys
import argparse
import subprocess
from pathlib import Path

def run_backend():
    """Start the backend API server"""
    print("\n=== Starting AI Job Hunt Backend Server ===\n")
    backend_path = Path(__file__).parent / "backend" / "run.py"
    cmd = [sys.executable, str(backend_path), "backend"]
    subprocess.run(cmd)

def run_dashboard():
    """Start the dashboard"""
    print("\n=== Starting AI Job Hunt Dashboard ===\n")
    dashboard_path = Path(__file__).parent / "frontend" / "run_dashboard.py"
    cmd = [sys.executable, str(dashboard_path)]
    subprocess.run(cmd)

def run_all():
    """Start both backend and dashboard"""
    print("\n=== Starting AI Job Hunt System ===\n")
    # Start backend in a separate process
    backend_path = Path(__file__).parent / "backend" / "run.py"
    backend_process = subprocess.Popen(
        [sys.executable, str(backend_path), "backend"],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE
    )
    
    # Start dashboard
    dashboard_path = Path(__file__).parent / "frontend" / "run_dashboard.py"
    subprocess.run([sys.executable, str(dashboard_path)])
    
    # Clean up backend process when dashboard exits
    backend_process.terminate()

def main():
    """Main entry point"""
    parser = argparse.ArgumentParser(description="AI Job Hunt System")
    parser.add_argument("component", choices=["backend", "dashboard", "all"], 
                        nargs="?", default="all",
                        help="Component to run (backend, dashboard, or all)")
    
    args = parser.parse_args()
    
    if args.component == "backend":
        run_backend()
    elif args.component == "dashboard":
        run_dashboard()
    else:
        run_all()

if __name__ == "__main__":
    main()
