Paper-space-resume-parser Project
This project is a resume parser built with Python, Streamlit, MongoDB, and Docker. It extracts information (name, email, skills, etc.) from PDF or DOCX resumes and stores it in MongoDB, all running in Docker containers.
Prerequisites

Docker (with Docker Compose)
A resume file (PDF or DOCX) for testing

Project Structure
paper-space-resume-parser/
├── app.py              # Streamlit application
├── requirements.txt    # Python dependencies
├── Dockerfile          # Docker configuration for the app
├── docker-compose.yml  # Defines MongoDB and app services
├── README.md           # This file

Setup Instructions
1. Create the Project Directory
mkdir paper-space-resume-parser
cd paper-space-resume-parser

2. Save the Required Files
Save the following files in the project directory:

app.py: The Streamlit application code.
requirements.txt: Python dependencies (includes altair==4.2.2 for Streamlit compatibility).
Dockerfile: Docker configuration for the app.
docker-compose.yml: Defines services for MongoDB and the app.

3. Build and Run with Docker Compose
Navigate to the project directory:
cd path

Build and start the containers:
docker-compose up --build


The MongoDB container is available at mongo:27017 (used by app.py).
The Streamlit app is accessible at http://localhost:8501.
Docker caches build layers for faster rebuilds if requirements.txt is unchanged.

4. Usage

Open your browser at http://localhost:8501.
Upload a PDF or DOCX resume.
Click "Parse Resume" to extract data (name, email, skills, etc.).
Click "Save to MongoDB" to store the data in the resumes collection of the resume_db database.

5. Verify MongoDB Data
Check stored data:
docker exec -it mongo mongosh

Run:
use resume_db
db.resumes.find()

6. Stop the Containers
Stop the containers:
docker-compose down

Clear MongoDB data:
docker-compose down -v

7. Using Docker Cache

Docker caches build layers (e.g., pip install) for faster rebuilds if requirements.txt is unchanged.
To force a rebuild without cache:docker-compose build --no-cache



Troubleshooting

Container Exits: Check docker logs resume-parser for errors (e.g., missing altair). Ensure requirements.txt includes altair==4.2.2.
MongoDB Connection Issues: Verify the mongo service is running (docker ps) and the URI in app.py is mongodb://mongo:27017.
Connection Refused: Ensure port 8501 is free (netstat -aon | findstr :8501). Try http://127.0.0.1:8501 or change to 8502:8501 in docker-compose.yml.
Resume Parsing Errors: Use a valid PDF or DOCX resume. Test with a simple resume.
Command Errors: Run docker-compose commands from the project directory.

Improvements

Add error handling for invalid file types.
Use MongoDB Atlas for a cloud database by updating the URI in app.py.
Enhance parsing with custom regex for specific resume formats.


