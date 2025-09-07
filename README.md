# Paper Space Resume Parser

## Notice
**This project is private and not intended for public use, modification, or distribution. It is for personal or authorized use only. Unauthorized use, copying, or distribution is strictly prohibited.**

## Overview
The Paper Space Resume Parser is a Python-based application built with **Streamlit**, **MongoDB**, and **Docker**. It extracts structured information (e.g., name, email, skills) from PDF or DOCX resumes using the `pyresparser` library, stores the parsed data in a MongoDB database, and provides options to export the data as JSON or CSV. The entire application runs in Docker containers for a reproducible environment.

## Features
- **Resume Parsing**: Extracts key details (name, email, skills, etc.) from PDF or DOCX resumes.
- **Data Storage**: Saves parsed resume data to a MongoDB database (`resume_db`, `resumes` collection).
- **File Upload**: Supports multiple resume uploads via a Streamlit web interface.
- **Data Export**: Allows exporting stored data as JSON or CSV files.
- **Containerized Deployment**: Uses Docker for consistent setup of Streamlit and MongoDB services.
- **Error Handling**: Manages file parsing errors and MongoDB connection issues.

## Project Structure
```
paper-space-resume-parser/
├── app.py                 # Streamlit application code
├── requirements.txt       # Python dependencies
├── Dockerfile            # Docker configuration for the app
├── docker-compose.yml    # Defines MongoDB and app services
├── README.md             # This documentation file
```

## Prerequisites
- **Docker**: With Docker Compose for containerized deployment.
- A valid PDF or DOCX resume file for testing.

## Tech Stack
- **Python**: Core language for the application and parsing logic.
- **Streamlit**: Web interface for uploading resumes and viewing/exporting data.
- **Pyresparser**: Library for extracting structured data from resumes.
- **MongoDB**: NoSQL database for storing parsed resume data.
- **Pymongo**: Python driver for MongoDB interactions.
- **Docker**: Containerization for reproducible environments.
- **Pandas**: For CSV export functionality.

## Setup Instructions
*Note: Setup is restricted to authorized users only.*

1. **Create the Project Directory**:
   ```bash
   mkdir paper-space-resume-parser
   cd paper-space-resume-parser
   ```

2. **Save the Required Files**:
   - **`app.py`**: The Streamlit application code (as provided).
   - **`requirements.txt`**:
     ```
     streamlit
     pyresparser
     pymongo
     pandas
     altair==4.2.2
     ```
   - **`Dockerfile`**:
     ```dockerfile
     FROM python:3.9-slim
     WORKDIR /app
     COPY requirements.txt .
     RUN pip install --no-cache-dir -r requirements.txt
     COPY app.py .
     EXPOSE 8501
     CMD ["streamlit", "run", "app.py", "--server.port=8501", "--server.address=0.0.0.0"]
     ```
   - **`docker-compose.yml`**:
     ```yaml
     version: '3'
     services:
       mongo:
         image: mongo:latest
         ports:
           - "27017:27017"
         volumes:
           - mongo-data:/data/db
       resume-parser:
         build:
           context: .
           dockerfile: Dockerfile
         ports:
           - "8501:8501"
         depends_on:
           - mongo
         volumes:
           - ./temp:/app/temp
     volumes:
       mongo-data:
     ```

3. **Build and Run with Docker Compose**:
   Navigate to the project directory:
   ```bash
   cd paper-space-resume-parser
   ```
   Build and start the containers:
   ```bash
   docker-compose up --build
   ```

4. **Access the Application**:
   - Streamlit app: `http://localhost:8501`
   - MongoDB: `mongodb://mongo:27017`

5. **Docker Cache**:
   Docker caches build layers for faster rebuilds if `requirements.txt` is unchanged. To force a rebuild:
   ```bash
   docker-compose build --no-cache
   ```

## Usage
*Note: Usage is restricted to authorized users only.*

1. Open `http://localhost:8501` in your browser.
2. Upload one or more PDF or DOCX resumes using the file uploader.
3. View the parsed data (e.g., name, email, skills) displayed on the page.
4. Click **Save to MongoDB** to store the parsed data in the `resumes` collection of the `resume_db` database.
5. Export stored data:
   - Select **JSON** or **CSV** from the export format dropdown.
   - Click **Export Data** to download the data.

### Verify MongoDB Data
Check stored data in MongoDB:
```bash
docker exec -it mongo mongosh
```
Run:
```javascript
use resume_db
db.resumes.find()
```

### Stop the Containers
Stop the containers:
```bash
docker-compose down
```
Clear MongoDB data (if needed):
```bash
docker-compose down -v
```

## Code Structure
- **`app.py`**:
  - **Streamlit Interface**: Handles resume uploads, displays parsed data, and provides export options.
  - **Resume Parsing**: Uses `pyresparser` to extract structured data from resumes.
  - **MongoDB Integration**: Stores parsed data in the `resumes` collection.
  - **Export Functionality**: Exports data as JSON or CSV using Pandas.
- **Temporary File Handling**: Saves uploaded resumes to a `temp` directory, processes them, and deletes them after parsing.
- **MongoDB Schema**: Stores resume data as documents with fields like `name`, `email`, `skills`, and `resume_file` (filename).

## Example Output
- **Parsed Resume Data** (displayed in Streamlit):
  ```
  Resume 1: sample_resume.pdf
  Name: John Doe
  Email: john.doe@example.com
  Skills: Python, Java, Data Analysis
  ...
  ```
- **MongoDB Document**:
  ```json
  {
    "resume_file": "sample_resume.pdf",
    "name": "John Doe",
    "email": "john.doe@example.com",
    "skills": ["Python", "Java", "Data Analysis"],
    ...
  }
  ```
- **CSV Export**:
  ```
  resume_file,name,email,skills
  sample_resume.pdf,John Doe,john.doe@example.com,"Python,Java,Data Analysis"
  ```

## Troubleshooting
- **Container Exits**: Check logs (`docker logs resume-parser`) for errors (e.g., missing `altair==4.2.2` in `requirements.txt`).
- **MongoDB Connection Issues**: Ensure the `mongo` service is running (`docker ps`) and the URI is `mongodb://mongo:27017`.
- **Connection Refused**: Verify port 8501 is free (`netstat -aon | findstr :8501`). Try `http://127.0.0.1:8501` or change to `8502:8501` in `docker-compose.yml`.
- **Resume Parsing Errors**: Use valid PDF/DOCX resumes. Test with a simple resume to avoid parsing issues.

## Limitations
- Dependent on `pyresparser` for resume parsing accuracy, which may vary with resume formats.
- Requires valid PDF or DOCX files.
- Limited error handling for invalid file types.
- MongoDB runs locally; cloud integration (e.g., MongoDB Atlas) requires URI updates.

## Improvements
- Add validation for file types before parsing.
- Support cloud-based MongoDB (e.g., MongoDB Atlas) by updating the URI in `app.py`.
- Enhance parsing with custom regex for specific resume formats.
- Add authentication to restrict access to the Streamlit app.

## License
This project is private and all rights are reserved. Unauthorized use, modification, or distribution is prohibited.

## Contact
This project was built as part of a hands-on Data Engineering learning journey. For questions or authorized collaboration, please contact the project owner.
