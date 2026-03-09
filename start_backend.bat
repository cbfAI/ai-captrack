@echo off
cd /d p:\git\AICapTrack\backend
set PYTHONPATH=p:\git\AICapTrack\backend
set DATABASE_URL=sqlite:///./aicaptrack.db
uvicorn main:app --host 0.0.0.0 --port 8000 --reload
