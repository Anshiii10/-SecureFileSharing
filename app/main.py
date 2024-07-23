from fastapi import FastAPI, Depends, HTTPException, status, File, UploadFile
from fastapi.security import OAuth2PasswordRequestForm
from typing import List
from .schemas import UserCreate, UserLogin, Token, FileUpload
from .crud import create_user, authenticate_user, create_file_metadata
from .auth import create_access_token, get_current_user
from .config import settings
from .models import User, FileMetadata
from .utils import generate_encrypted_url, send_verification_email
from bson import ObjectId
from pymongo import MongoClient

client = MongoClient(settings.mongodb_url)
db = client.file_sharing

app = FastAPI()

@app.post("/signup", response_model=Token)
async def signup(user: UserCreate):
    user_data = User(**user.dict(), hashed_password="", role="client", is_active=False)
    create_user(user_data)
    verification_url = generate_encrypted_url(user.email)
    send_verification_email(user.email, verification_url)
    return {"message": "Verification email sent. Please check your inbox."}

@app.post("/token", response_model=Token)
async def login(form_data: OAuth2PasswordRequestForm = Depends()):
    user = authenticate_user(form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token = create_access_token(data={"sub": user["username"]})
    return {"access_token": access_token, "token_type": "bearer"}

@app.post("/upload", response_model=FileMetadata)
async def upload_file(file: UploadFile = File(...), current_user: User = Depends(get_current_user)):
    if current_user.role != "ops":
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Operation not permitted.")
    if file.content_type not in ["application/vnd.openxmlformats-officedocument.presentationml.presentation", 
                                  "application/vnd.openxmlformats-officedocument.wordprocessingml.document",
                                  "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"]:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid file type.")
    file_meta = FileMetadata(filename=file.filename, content_type=file.content_type, uploader_id=str(current_user.id))
    create_file_metadata(file_meta)
    return file_meta

@app.get("/download/{file_id}")
async def download_file(file_id: str, current_user: User = Depends(get_current_user)):
    file = db.files.find_one({"_id": ObjectId(file_id)})
    if not file:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="File not found.")
    if current_user.role != "client":
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Operation not permitted.")
    download_url = generate_encrypted_url(file_id)
    db.files.update_one({"_id": ObjectId(file_id)}, {"$set": {"download_url": download_url, "encrypted": True}})
    return {"download-link": download_url, "message": "success"}

@app.get("/files", response_model=List[FileMetadata])
async def list_files(current_user: User = Depends(get_current_user)):
    if current_user.role != "client":
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Operation not permitted.")
    files = db.files.find({"uploader_id": str(current_user.id)})
    return list(files)
