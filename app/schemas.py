from pydantic import BaseModel, EmailStr
from typing import Optional

class UserCreate(BaseModel):
    username: str
    email: EmailStr
    password: str

class UserLogin(BaseModel):
    username: str
    password: str

class FileUpload(BaseModel):
    filename: str
    content_type: str

class Token(BaseModel):
    access_token: str
    token_type: str
