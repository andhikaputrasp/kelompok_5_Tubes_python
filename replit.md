# Manajemen Nilai Siswa

## Overview
A Flask-based student performance management system with CRUD operations and machine learning prediction capabilities. The application allows managing student data and predicting math scores using Linear Regression.

## Project Structure
- `kelompok_5.py` - Main Flask application
- `frontend/` - Jinja2 HTML templates (base.html, index.html, tambah.html, edit.html, predict.html)
- `static/` - Static assets (style.css)
- `StudentsPerformance.csv` - Student data storage

## Features
- Dashboard with student data table
- Add/Edit/Delete student records
- Gender filtering
- Math score prediction using Linear Regression

## Tech Stack
- Python 3.11
- Flask (web framework)
- Pandas (data processing)
- Scikit-learn (machine learning)
- Jinja2 (templating)
- Gunicorn (production server)

## Running the Application
Development: `python kelompok_5.py` (runs on port 5000)
Production: `gunicorn --bind=0.0.0.0:5000 --reuse-port kelompok_5:app_kel_5`

## Recent Changes
- 2025-12-27: Configured for Replit environment (host 0.0.0.0, port 5000)
- 2025-12-27: Created base.html template (was empty in import)
- 2025-12-27: Added gunicorn for production deployment
