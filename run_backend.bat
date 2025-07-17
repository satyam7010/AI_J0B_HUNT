@echo off
echo Starting AI Job Hunt Backend Server...
echo.
uvicorn backend.main:app --host 0.0.0.0 --port 8000 --reload
