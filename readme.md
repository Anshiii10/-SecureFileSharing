

# Secure File Sharing

This project implements a secure file-sharing system using FastAPI. It features two types of users: Ops Users and Client Users. Ops Users can upload specific file types, and Client Users can sign up, verify their emails, and download files through secure, encrypted URLs.

## Features

- **Ops User Operations**:
  - Login
  - Upload files (`.pptx`, `.docx`, `.xlsx`)

- **Client User Operations**:
  - Sign Up (returns an encrypted URL)
  - Email Verification (verification email sent to the registered email)
  - Login
  - Download files (secured via encrypted URL)
  - List all uploaded files

## Prerequisites

- Python 3.12.4
- MongoDB
- FastAPI
- Required Python packages 
    fastapi==0.88.0
    uvicorn==0.20.0
    pydantic==2.8.0
    pydantic-settings==2.0.2
    motor==3.1.1
    bson==0.5.10
    passlib==1.7.4
    python-jose==3.3.0
    email-validator==2.0.0
    httpx==0.23.1
    pytest==7.1.3
    python-dotenv==1.0.0


## Installation

1. Coding in VS Code

   

2. Create and activate a virtual environment:

   ```sh
   python -m venv venv
   venv\Scripts\activate  # For Windows
   # source venv/bin/activate  # For macOS/Linux
   ```

3. Install the required packages:

   
   pip install -r requirements.txt
   

4. Create a `.env` file in the root directory and add the following environment variables:

  
   MONGODB_URL=your_mongodb_url
   SECRET_KEY=123456
  

## Running the Application

1. Start the FastAPI server:

   
   uvicorn app.main:app --reload
   

2. Open your browser and navigate to `http://127.0.0.1:8000/docs` to access the Swagger UI and test the API endpoints.

## API Endpoints

### Auth

- **POST `/signup`**: Sign up a new Client User.
- **POST `/login`**: Login for both Ops and Client Users.

### Files

- **POST `/upload`**: Upload a file (Ops User only).
- **GET `/files`**: List all uploaded files (Client User only).
- **GET `/download/{file_id}`**: Download a file using an encrypted URL (Client User only).

### Examples

#### Sign Up


curl -X POST "http://127.0.0.1:8000/signup" -H "Content-Type: application/json" -d '{
  "email": "user@example.com",
  "password": "securepassword"
}'


#### Login


curl -X POST "http://127.0.0.1:8000/login" -H "Content-Type: application/json" -d '{
  "username": "user@example.com",
  "password": "securepassword"
}'


#### Upload File


curl -X POST "http://127.0.0.1:8000/upload" -H "Authorization: Bearer your_token" -F "file=@/path/to/your/file.pptx"


#### List Files


curl -X GET "http://127.0.0.1:8000/files" -H "Authorization: Bearer your_token"


#### Download File


curl -X GET "http://127.0.0.1:8000/download/{file_id}" -H "Authorization: Bearer your_token"


## Testing

To run tests, use the following command:


pytest


## Screenshots

Link-https://drive.google.com/drive/folders/132O3D3sFdRIpZkX8ENf5zi5Tk-hYXBLt?usp=sharing