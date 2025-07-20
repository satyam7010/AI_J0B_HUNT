"""
Entry point for the AI Job Hunt application
This ensures the Python import paths are set correctly
"""

import sys
import os
import uvicorn
import time
import threading
import webbrowser

# Add the project root to the Python path
sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))

def open_browser():
    """Open browser after a delay to ensure server is up"""
    time.sleep(2)  # Wait for server to start
    print("Opening API documentation in browser...")
    webbrowser.open("http://localhost:8000/docs")

if __name__ == "__main__":
    print("Starting AI Job Hunt Backend Server...")
    print("API will be available at http://localhost:8000")
    print("API documentation will be available at http://localhost:8000/docs")
    
    # Start the browser in a separate thread
    threading.Thread(target=open_browser).start()
    
    # Run the API server
    uvicorn.run("backend.main:app", host="0.0.0.0", port=8000, reload=True)
